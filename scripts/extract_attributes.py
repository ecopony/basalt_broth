# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "gdal"]
# ///
# ABOUTME: Extracts per-segment attributes for each of the 834 street segments.
# ABOUTME: Buffers each segment, samples rasters, does spatial joins. Outputs GeoJSON.

import json
import os
import numpy as np
from osgeo import gdal, ogr, osr

gdal.UseExceptions()

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

# Input paths
STREETS_PATH = os.path.join(DATA_DIR, "streets", "streets.geojson")
HSG_PATH = os.path.join(DATA_DIR, "stormwater", "hydrologic_soil_groups.geojson")
INLETS_PATH = os.path.join(DATA_DIR, "sewer", "inlets.geojson")

# Raster inputs
RASTERS = {
    "slope_deg": os.path.join(DATA_DIR, "derived", "slope.tif"),
    "flow_accum": os.path.join(DATA_DIR, "derived", "flow_accumulation.tif"),
    "twi": os.path.join(DATA_DIR, "derived", "twi.tif"),
    "impervious": os.path.join(DATA_DIR, "impervious", "impervious.tif"),
}

# Output
OUTPUT_PATH = os.path.join(DATA_DIR, "derived", "segment_attributes.geojson")

# Buffer distance (feet) — captures street + fronting properties
BUFFER_DIST = 50


class RasterReader:
    """Reads a GeoTIFF into a numpy array with coordinate mapping."""

    def __init__(self, path):
        ds = gdal.Open(path)
        self.array = ds.GetRasterBand(1).ReadAsArray().astype(np.float64)
        gt = ds.GetGeoTransform()
        self.x_origin = gt[0]
        self.y_origin = gt[3]
        self.pixel_w = gt[1]
        self.pixel_h = gt[5]  # negative
        self.rows, self.cols = self.array.shape
        ds = None

    def sample_polygon(self, geom):
        """Extract mean value of all pixels inside a polygon geometry."""
        env = geom.GetEnvelope()  # (minX, maxX, minY, maxY)
        # Convert envelope to pixel coordinates
        col_min = max(0, int((env[0] - self.x_origin) / self.pixel_w))
        col_max = min(self.cols, int((env[1] - self.x_origin) / self.pixel_w) + 1)
        row_min = max(0, int((env[3] - self.y_origin) / self.pixel_h))
        row_max = min(self.rows, int((env[2] - self.y_origin) / self.pixel_h) + 1)

        if col_min >= col_max or row_min >= row_max:
            return np.nan

        # Create a small in-memory raster for the mask
        sub_w = col_max - col_min
        sub_h = row_max - row_min

        mem_driver = gdal.GetDriverByName("MEM")
        mask_ds = mem_driver.Create("", sub_w, sub_h, 1, gdal.GDT_Byte)
        mask_gt = (
            self.x_origin + col_min * self.pixel_w,
            self.pixel_w,
            0,
            self.y_origin + row_min * self.pixel_h,
            0,
            self.pixel_h,
        )
        mask_ds.SetGeoTransform(mask_gt)

        # Create temporary vector layer with the polygon
        mem_vec_driver = ogr.GetDriverByName("Memory")
        mem_vec_ds = mem_vec_driver.CreateDataSource("")
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(2913)
        mem_layer = mem_vec_ds.CreateLayer("poly", srs, ogr.wkbPolygon)
        feat_defn = mem_layer.GetLayerDefn()
        feat = ogr.Feature(feat_defn)
        feat.SetGeometry(geom)
        mem_layer.CreateFeature(feat)

        # Rasterize the polygon onto the mask
        gdal.RasterizeLayer(mask_ds, [1], mem_layer, burn_values=[1])
        mask = mask_ds.GetRasterBand(1).ReadAsArray()

        # Extract values where mask == 1
        sub_array = self.array[row_min:row_max, col_min:col_max]
        values = sub_array[mask == 1]

        mask_ds = None
        mem_vec_ds = None

        if len(values) == 0:
            return np.nan
        return float(np.mean(values))


def load_inlets():
    """Load inlet points as (x, y) array."""
    ds = ogr.Open(INLETS_PATH)
    layer = ds.GetLayer()
    points = []
    for feat in layer:
        geom = feat.GetGeometryRef()
        points.append((geom.GetX(), geom.GetY()))
    ds = None
    return np.array(points)


def nearest_inlet_distance(geom, inlet_points):
    """Distance from segment midpoint to nearest inlet (feet)."""
    # Use segment centroid
    centroid = geom.Centroid()
    cx, cy = centroid.GetX(), centroid.GetY()
    dists = np.sqrt((inlet_points[:, 0] - cx) ** 2 + (inlet_points[:, 1] - cy) ** 2)
    return float(np.min(dists))


def assign_hsg(geom):
    """Spatial join: determine HSG for a segment based on its midpoint."""
    ds = ogr.Open(HSG_PATH)
    layer = ds.GetLayer()
    centroid = geom.Centroid()

    for feat in layer:
        poly = feat.GetGeometryRef()
        if poly.Contains(centroid):
            hsg = feat.GetField("HydrolGrp")
            musym = feat.GetField("MUSYM")
            ds = None
            if hsg is None:
                # Urban Land (MUSYM 50C) — assign HSG D per USDA guidance
                return "D", musym
            return hsg, musym

    ds = None
    return "D", "unknown"  # default if outside all polygons


def main():
    print("Loading rasters...")
    readers = {}
    for name, path in RASTERS.items():
        readers[name] = RasterReader(path)
        print(f"  {name}: {readers[name].cols}x{readers[name].rows}")

    print("Loading inlets...")
    inlet_points = load_inlets()
    print(f"  {len(inlet_points)} inlet points")

    print("Processing street segments...")
    ds = ogr.Open(STREETS_PATH)
    layer = ds.GetLayer()
    n_features = layer.GetFeatureCount()

    results = []
    for i, feat in enumerate(layer):
        geom = feat.GetGeometryRef()
        buffered = geom.Buffer(BUFFER_DIST)
        seg_length = geom.Length()

        # Skip very short segments (< 20 ft) — likely slivers
        if seg_length < 20:
            continue

        # Sample rasters within buffer
        attrs = {}
        for name, reader in readers.items():
            attrs[name] = reader.sample_polygon(buffered)

        # Soil group
        hsg, musym = assign_hsg(geom)

        # Distance to nearest inlet
        inlet_dist = nearest_inlet_distance(geom, inlet_points)

        # Build result
        result = {
            "objectid": feat.GetField("OBJECTID"),
            "full_name": feat.GetField("FULL_NAME"),
            "cfcc": feat.GetField("CFCC"),
            "length_ft": round(seg_length, 1),
            "slope_deg": round(attrs["slope_deg"], 3) if not np.isnan(attrs["slope_deg"]) else None,
            "flow_accum": round(attrs["flow_accum"], 1) if not np.isnan(attrs["flow_accum"]) else None,
            "twi": round(attrs["twi"], 2) if not np.isnan(attrs["twi"]) else None,
            "impervious_pct": round(attrs["impervious"] * 100, 1) if not np.isnan(attrs["impervious"]) else None,
            "hsg": hsg,
            "musym": musym,
            "inlet_dist_ft": round(inlet_dist, 1),
        }
        results.append((geom.ExportToJson(), result))

        if (i + 1) % 100 == 0:
            print(f"  {i + 1}/{n_features}...")

    ds = None
    print(f"  {len(results)} segments processed ({n_features - len(results)} skipped as <20ft)")

    # Write GeoJSON
    print("Writing output...")
    features = []
    for geom_json, attrs in results:
        features.append({
            "type": "Feature",
            "geometry": json.loads(geom_json),
            "properties": attrs,
        })

    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(geojson, f)

    print(f"\nSaved {len(features)} segments to {OUTPUT_PATH}")

    # Summary stats
    print("\nAttribute summary:")
    for key in ["slope_deg", "flow_accum", "twi", "impervious_pct", "inlet_dist_ft"]:
        vals = [r[key] for _, r in results if r[key] is not None]
        if vals:
            arr = np.array(vals)
            print(f"  {key}: min={arr.min():.1f}  median={np.median(arr):.1f}  max={arr.max():.1f}")

    hsg_counts = {}
    for _, r in results:
        hsg_counts[r["hsg"]] = hsg_counts.get(r["hsg"], 0) + 1
    print(f"  HSG distribution: {dict(sorted(hsg_counts.items()))}")


if __name__ == "__main__":
    main()
