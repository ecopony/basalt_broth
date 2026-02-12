# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
# ]
# ///
# ABOUTME: Fetches all GIS layers for the study area and reprojects to EPSG:2913.
# ABOUTME: Hawthorne to Division, SE 20th to Cesar Chavez (SE 39th).

import json
import os
import subprocess
import requests

TARGET_CRS = "EPSG:2913"

# Canonical study area extent in EPSG:2913 (Oregon North State Plane, ft).
# This is the single source of truth — matches clip_dem.py.
STUDY_EXTENT_2913 = {
    "xmin": 7650146,
    "ymin": 675893,
    "xmax": 7658210,
    "ymax": 680660,
}

# WGS84 query bbox — intentionally slightly oversized so the ArcGIS spatial
# query returns all features that touch the study area.  The actual clip to
# a clean EPSG:2913 rectangle happens in ogr2ogr with -clipdst.
QUERY_BBOX_WGS84 = {
    "xmin": -122.655,
    "ymin": 45.500,
    "xmax": -122.620,
    "ymax": 45.515,
}

CLIP_EXTENT = (
    STUDY_EXTENT_2913["xmin"],
    STUDY_EXTENT_2913["ymin"],
    STUDY_EXTENT_2913["xmax"],
    STUDY_EXTENT_2913["ymax"],
)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def reproject_geojson(in_path, out_path, target_crs):
    """Reproject a GeoJSON file using ogr2ogr and clip to study area."""
    subprocess.run(
        [
            "ogr2ogr", "-f", "GeoJSON",
            "-t_srs", target_crs,
            "-clipdst", *[str(v) for v in CLIP_EXTENT],
            out_path, in_path,
        ],
        check=True,
    )


def fetch_arcgis_layer(url, out_name, out_dir, method="post"):
    """Fetch all features from an ArcGIS REST service layer as GeoJSON with pagination."""
    os.makedirs(out_dir, exist_ok=True)
    all_features = []
    offset = 0
    batch = 2000

    while True:
        params = {
            "where": "1=1",
            "geometry": json.dumps(QUERY_BBOX_WGS84),
            "geometryType": "esriGeometryEnvelope",
            "inSR": "4326",
            "spatialRel": "esriSpatialRelIntersects",
            "outFields": "*",
            "returnGeometry": "true",
            "f": "geojson",
            "resultRecordCount": batch,
            "resultOffset": offset,
        }

        if method == "post":
            resp = requests.post(url, data=params, timeout=60)
        else:
            resp = requests.get(url, params=params, timeout=60)

        resp.raise_for_status()
        data = resp.json()

        if "error" in data:
            print(f"  ERROR: {data['error']}")
            return None

        features = data.get("features", [])
        if not features:
            break

        all_features.extend(features)
        print(f"  Fetched {len(features)} (total: {len(all_features)})")

        if len(features) < batch:
            break
        offset += batch

    result = {"type": "FeatureCollection", "features": all_features}

    # Write WGS84 temp file, then reproject
    tmp_path = os.path.join(out_dir, f"{out_name}_wgs84.geojson")
    out_path = os.path.join(out_dir, f"{out_name}.geojson")
    with open(tmp_path, "w") as f:
        json.dump(result, f)

    reproject_geojson(tmp_path, out_path, TARGET_CRS)
    os.remove(tmp_path)

    print(f"  Saved {len(all_features)} features to {out_path} ({TARGET_CRS})")
    return out_path


def main():
    swsp_url = "https://www.portlandmaps.com/arcgis/rest/services/Public/Stormwater_System_Plan/MapServer"
    sewer_url = "https://www.portlandmaps.com/arcgis/rest/services/Public/Utilities_Sewer/MapServer"
    trees_url = "https://services.arcgis.com/quVN97tn06YNGj9s/arcgis/rest/services/Street_Tree_Inventory_Second_Edition_2024/FeatureServer/297/query"
    buildings_url = "https://www.portlandmaps.com/arcgis/rest/services/Public/Basemap_Color_Buildings/MapServer/0/query"

    # New layer URLs
    streets_url = "https://www.portlandmaps.com/arcgis/rest/services/Public/Street_Centerlines/MapServer"
    zoning_url = "https://www.portlandmaps.com/arcgis/rest/services/Public/Zoning/MapServer"

    stormwater_dir = os.path.join(DATA_DIR, "stormwater")
    sewer_dir = os.path.join(DATA_DIR, "sewer")
    trees_dir = os.path.join(DATA_DIR, "trees")
    impervious_dir = os.path.join(DATA_DIR, "impervious")
    streets_dir = os.path.join(DATA_DIR, "streets")
    zoning_dir = os.path.join(DATA_DIR, "zoning")

    # Stormwater System Plan layers
    # Note: Layer 5 (depth to groundwater) and Layer 11 (slope) are RASTER layers
    # and cannot be queried as features. They require separate raster download.
    swsp_layers = {
        "hydrologic_soil_groups": 2,
        # "depth_to_groundwater": 5,  # RASTER - needs separate handling via exportImage
        "holgate_lake_groundwater": 7,
        "regional_geology": 12,
        "depth_to_bedrock": 13,
        "combined_sewer_basins": 16,
    }

    for name, layer_id in swsp_layers.items():
        print(f"Fetching {name}...")
        fetch_arcgis_layer(f"{swsp_url}/{layer_id}/query", name, stormwater_dir, method="get")

    # Sewer layers
    sewer_layers = {
        "storm_nodes": 6,
        "storm_pipes": 7,
        "inlets": 19,
    }

    for name, layer_id in sewer_layers.items():
        print(f"Fetching {name}...")
        fetch_arcgis_layer(f"{sewer_url}/{layer_id}/query", name, sewer_dir, method="get")

    # Street trees
    print("Fetching street_trees...")
    fetch_arcgis_layer(trees_url, "street_trees", trees_dir, method="post")

    # Building footprints
    print("Fetching building_footprints...")
    fetch_arcgis_layer(buildings_url, "building_footprints", impervious_dir, method="post")

    # Street centerlines (CRITICAL for network segmentation)
    # Layer 0 = Geocoding Streets from Street_Centerlines MapServer
    # Has STREETNAME, FTYPE, PREFIX, SUFFIX, TYPE, address ranges
    print("Fetching streets...")
    fetch_arcgis_layer(f"{streets_url}/0/query", "streets", streets_dir, method="get")

    # Zoning (for placement constraints)
    # Layer 0 = Base zoning
    print("Fetching zoning...")
    fetch_arcgis_layer(f"{zoning_url}/0/query", "zoning", zoning_dir, method="get")


if __name__ == "__main__":
    main()
