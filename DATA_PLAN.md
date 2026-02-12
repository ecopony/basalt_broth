# Data Acquisition Plan

**Date:** 2026-02-04
**Status:** ✅ Core Acquisition Complete
**Study Area:** Hawthorne-Division corridor, SE Portland (EPSG:2913)

---

## Overview

This document tracks the data layers required for the Street Segment Rating Pipeline. It serves as:
1. An inventory of what we have
2. A gap analysis of what we need
3. Acquisition instructions for each missing layer
4. Processing notes for data preparation

---

## Executive Summary

**Core data acquisition is complete.** All critical layers for the pipeline have been fetched:
- ✅ Street centerlines (834 segments with pre-built network topology)
- ✅ GSI facilities (176 for validation)
- ✅ Zoning (111 polygons)
- ✅ Soils, geology, sewer infrastructure

**Remaining gaps are enhancement layers** (SSURGO Ksat, tree canopy raster, design storm tables) that improve model accuracy but don't block initial development.

---

## Current Data Inventory

All data clipped to canonical study extent in EPSG:2913:
```
xmin: 7650146    ymin: 675893
xmax: 7658210    ymax: 680660
```

### Raster Data

| Layer | File | Resolution | CRS | Status |
|-------|------|------------|-----|--------|
| DEM | `dem/study_area_dem.tif` | 3 ft | EPSG:2913 | ✅ Ready |
| DEM (NetLogo) | `dem/study_area_dem_utm.asc` | 1 m | EPSG:26910 | ✅ Ready |
| Groundwater Depth | `stormwater/depth_to_groundwater.tif` | 3 ft | EPSG:2913 | ⚠️ Partial (see notes) |
| Impervious Surface | `impervious/impervious.tif` | 3 ft | EPSG:2913 | ✅ Ready |

**DEM Details:**
- Source: USGS 3DEP 1-meter LiDAR (OR_OLCMetro_2019)
- Dimensions: 2,688 × 1,589 pixels
- Elevation range: 11.5 – 55.5 ft
- Coverage: 100% valid

### Vector Data

| Layer | File | Features | Purpose | Status |
|-------|------|----------|---------|--------|
| **Streets** | `streets/streets.geojson` | **834** | Network segmentation | ✅ Ready |
| **GSI Facilities** | `validation/gsi_facilities.geojson` | **176** | Validation dataset | ✅ Ready |
| **Zoning** | `zoning/zoning.geojson` | **111** | Placement constraints | ✅ Ready |
| Hydrologic Soil Groups | `stormwater/hydrologic_soil_groups.geojson` | 9 | Infiltration capacity (HSG A-D) | ⚠️ 39% null (see notes) |
| Depth to Bedrock | `stormwater/depth_to_bedrock.geojson` | 24 | Constraint layer | ✅ Ready |
| Regional Geology | `stormwater/regional_geology.geojson` | 8 | Constraint layer | ✅ Ready |
| Combined Sewer Basins | `stormwater/combined_sewer_basins.geojson` | 3 | CSO benefit zones | ✅ Ready |
| Storm Nodes | `sewer/storm_nodes.geojson` | 511 | Sink identification | ✅ Ready |
| Storm Pipes | `sewer/storm_pipes.geojson` | 141 | Network context | ✅ Ready |
| Inlets | `sewer/inlets.geojson` | 1,499 | Existing infrastructure | ✅ Ready |
| Building Footprints | `impervious/building_footprints.geojson` | 8,088 | Building polygons | ✅ Ready |
| Street Trees | `trees/street_trees.geojson` | 10,626 | Canopy benefit | ✅ Ready |
| Curbs | `curbs/Curbs.geojson` | 117,809 | Drainage channels | ✅ Ready |
| Collection System Lines | `collection_system_lines/shp/` | 360,170 | Sewer network (shapefile) | ✅ Ready |

---

## Completed Acquisitions

### Streets ✅ COMPLETE
**Purpose:** Network segmentation skeleton — the foundation of the entire pipeline

| Attribute | Value |
|-----------|-------|
| Source | Portland Street_Centerlines MapServer |
| URL | Layer 0 of `Public/Street_Centerlines/MapServer` |
| Features | **834 street segments** |
| Format | GeoJSON (EPSG:2913) |
| File | `data/streets/streets.geojson` |

**Key Discovery:** Streets have **pre-built network topology**:
- `PDX_F_NODE` — From node ID
- `PDX_T_NODE` — To node ID
- `FULL_NAME` — Complete street name (e.g., "SE 23RD AVE")
- `STREETNAME`, `PREFIX`, `FTYPE`, `SUFFIX` — Name components
- `TYPE` — Road type code
- `CFCC` — Census Feature Class Code

**Implication:** No custom segmentation needed — Portland's GIS team already split streets at intersections. We can use the node IDs directly for network analysis.

---

### GSI Facilities ✅ COMPLETE
**Purpose:** Validation dataset — compare model recommendations against Portland's existing facilities

| Attribute | Value |
|-----------|-------|
| Source | Collection System Lines shapefile |
| Filter | `SYMBOL_GRO = 'GREEN STREET FACILITY'` |
| City-wide Count | 2,975 green street + 74 roadside treatment = **3,049 total** |
| Study Area Count | **176 facilities** |
| Format | GeoJSON (EPSG:2913) |
| File | `data/validation/gsi_facilities.geojson` |

**Study Area GSI Summary:**
- All 176 are GREEN STREET FACILITY type
- Installation dates: 2004-05-18 to 2020-09-28
- By decade: 2000s (7), 2010s (115), 2020s (9)

**Note:** No BES data request needed — facility data was embedded in the publicly available Collection System Lines dataset, discovered by filtering on `SYMBOL_GRO` attribute.

---

### Zoning ✅ COMPLETE
**Purpose:** Placement constraints — some zones prohibit or restrict GSI

| Attribute | Value |
|-----------|-------|
| Source | Portland Zoning MapServer |
| Features | **111 polygons** |
| Format | GeoJSON (EPSG:2913) |
| File | `data/zoning/zoning.geojson` |

---

### Groundwater Depth ⚠️ PARTIAL
**Purpose:** Constraint layer — bioswales require minimum 5 ft clearance to seasonal high groundwater

| Attribute | Value |
|-----------|-------|
| Source | Portland BES Stormwater System Plan MapServer |
| URL | Layer 5 (RASTER layer, not vector) |
| Format | GeoTIFF (exported as RGBA image) |
| File | `data/stormwater/depth_to_groundwater.tif` |
| Status | ⚠️ Downloaded but requires color classification |

**Limitation:** Layer 5 is a raster layer. ArcGIS export returns a symbolized image with colored pixels representing depth categories, not raw depth values.

**Depth Categories (from legend):**
| Category | Depth (ft) | Bioswale Suitability |
|----------|------------|---------------------|
| < 20 | 0-20 ft | ⚠️ Needs review (could include <5 ft) |
| 20-40 | 20-40 ft | ✅ OK |
| 40-60 | 40-60 ft | ✅ OK |
| 60-80 | 60-80 ft | ✅ OK |
| 80-100 | 80-100 ft | ✅ OK |
| > 100 | 100+ ft | ✅ OK |

**Workaround:** For initial development, assume study area is OK (SE Portland urban infill is typically >20 ft to groundwater). Can refine later with color classification if needed.

---

### Hydrologic Soil Groups ⚠️ 39% NULL
**Purpose:** FIS Stage 1 input — soil infiltration capacity

| Attribute | Value |
|-----------|-------|
| Source | Portland BES Stormwater System Plan MapServer Layer 2 |
| Features | **9 polygons** |
| File | `data/stormwater/hydrologic_soil_groups.geojson` |
| Status | ⚠️ 39% of study area has null HydrolGrp |

**Issue:** MUSYM `50C` (Urban Land) covers ~15.8M sqft (39.1% of the study area) and has `HydrolGrp = None`. SSURGO classifies heavily developed areas as "Urban Land" with no hydrologic properties because the natural soil profile is considered disturbed. The remaining 60.9% is all HSG B (Latourell silt loam variants):

| MUSYM | Soil Type | HydrolGrp | Area (sqft) | % of Study Area |
|-------|-----------|-----------|-------------|-----------------|
| 51B | Latourell silt loam, 3-8% slopes | B | 13,927,732 | 34.4% |
| 51A | Latourell silt loam, 0-3% slopes | B | 10,430,030 | 25.7% |
| 50C | Urban Land | None | 15,848,339 | 39.1% |
| 51C | Latourell silt loam, 8-15% slopes | B | 297,237 | 0.7% |

**Why it's null:** SSURGO classifies heavily developed areas as "Urban Land" — a miscellaneous area, not a soil. USDA surveyors can't characterize soil beneath pavement and buildings, so no hydrologic properties are assigned. The underlying native soil (Latourell silt loam) is still present, but its infiltration capacity is degraded by compaction, grading, and fill material.

**Workaround:** Assign **HSG D** (worst infiltration, <0.05 in/hr) to `50C` Urban Land areas. This follows USDA/NRCS standard guidance (NEH Part 630 Chapter 7) and TR-55 urban hydrology methodology, which both prescribe HSG D for developed Urban Land. The rationale is that urban soils are compacted and perform far worse than their native classification — assigning the native HSG B would overestimate infiltration capacity.

This is also beneficial for the model: HSG D areas generate the most runoff and are therefore the highest-priority candidates for bioswale intervention. The FIS will correctly score these areas as having poor natural infiltration.

**Better fix:** Download full SSURGO from Web Soil Survey (see Remaining Data Gaps → SSURGO below). The component tables list secondary components (e.g., "60% Urban Land, 40% Latourell silt loam") with Ksat values for the native soil fraction, providing a more nuanced infiltration estimate than categorical HSG alone.

---

## Remaining Data Gaps

### Priority: High (Improves FIS Accuracy)

#### SSURGO Soil Data (Ksat Values)
**Purpose:** Infiltration rate for Soil FIS — current hydrologic soil groups are categorical only

| Attribute | Value |
|-----------|-------|
| Source | USDA Web Soil Survey |
| URL | https://websoilsurvey.nrcs.usda.gov/app/ |
| Format | Shapefile + Access database |
| Target File | `data/soils/ssurgo_ksat.geojson` |
| Acquisition | Manual download (interactive AOI selection) |

**Processing Required:**
1. Draw AOI around study area in Web Soil Survey
2. Download spatial + tabular data
3. Join tables: `mupolygon` → `component` → `chorizon` → `ksat_r`
4. Convert Ksat from micrometers/second to inches/hour
5. Clip to study extent, reproject to EPSG:2913

---

#### Impervious Surface ✅ COMPLETE
**Purpose:** Runoff calculation — FIS Stage 2 input (upstream impervious %)

| Attribute | Value |
|-----------|-------|
| Source | NOAA C-CAP 2021 High-Resolution Impervious Surface |
| Resolution | **1 meter** (derived from 30cm aerial imagery via AI classification + expert review) |
| Coverage | All of Oregon including Portland metro |
| Format | GeoTIFF (416 MB for full state) |
| Download | https://coastalimagery.blob.core.windows.net/ccap-landcover/CCAP_bulk_download/High_Resolution_Land_Cover/Phase_1_Initial_Layers/Impervious/index.html |
| File | `data/impervious/impervious.tif` |
| Status | ✅ Downloaded, clipped, reprojected to EPSG:2913 (3ft pixels, 2688x1589, binary 0/1) |

**Result:** 60.5% of study area is impervious. Median segment impervious is 70.3%. Arterials (Hawthorne, Powell) reach 100%.

**Background:** Originally planned to derive impervious surfaces by buffering street centerlines by road class and combining with building footprints. NOAA C-CAP provided wall-to-wall 1m impervious coverage instead — no derivation needed.

**Note:** Portland BES also has per-parcel impervious area measurements (used for stormwater billing) but that dataset is not publicly downloadable. Would require a direct data request.

---

### Priority: Medium (Enhances Model)

#### Tree Canopy Raster
**Purpose:** Interception benefit — reduces effective rainfall

| Attribute | Value |
|-----------|-------|
| Source | Oregon Metro RLIS |
| URL | https://rlisdiscovery.oregonmetro.gov/ |
| Target File | `data/canopy/tree_canopy.tif` |
| Acquisition | Manual download, clip to extent |

**Note:** We have street tree points (10,626). Raster adds private/non-street trees.

---

#### Design Storm Parameters
**Purpose:** Sizing calculations — bioswale capacity for target capture

| Attribute | Value |
|-----------|-------|
| Source | Portland BES SWMM Appendix A |
| URL | https://www.portland.gov/bes/stormwater/swmm |
| Target File | `data/reference/design_storms.json` |
| Acquisition | Manual extraction from PDF |

**Key Values:**
- 2-year storm: ~2.4 inches / 24 hours
- Water quality storm: 1.61 inches / 24 hours

---

## Data Processing Scripts

### Existing Scripts

| Script | Purpose | Status |
|--------|---------|--------|
| `scripts/clip_dem.py` | Mosaic and clip DEM tiles | ✅ Complete |
| `scripts/refetch_layers.py` | Fetch vector layers from ArcGIS REST | ✅ Complete & Updated |

### Scripts to Create

| Script | Purpose | Priority |
|--------|---------|----------|
| `scripts/process_ssurgo.py` | Join SSURGO tables, extract Ksat | 🟠 High |
| `scripts/clip_impervious.py` | Unzip/clip C-CAP impervious raster to study area | ✅ Complete |
| `scripts/calc_flow.py` | Slope, D8 flow direction, flow accumulation, TWI | ✅ Complete |
| `scripts/extract_attributes.py` | Zonal stats per segment (slope, TWI, impervious, HSG, inlet dist) | ✅ Complete |

**Note:** `segment_streets.py` is likely NOT needed — streets already have pre-built network topology via `PDX_F_NODE` / `PDX_T_NODE` attributes.

---

## File Organization

```
data/
├── dem/
│   ├── study_area_dem.tif           # Master DEM (EPSG:2913)
│   ├── study_area_dem_utm.tif       # NetLogo version (EPSG:26910)
│   ├── study_area_dem_utm.asc       # NetLogo ASCII grid
│   └── USGS_1M_*.tif                # Source tiles
│
├── streets/
│   └── streets.geojson              # ✅ 834 segments with network topology
│
├── stormwater/
│   ├── hydrologic_soil_groups.geojson
│   ├── depth_to_bedrock.geojson
│   ├── depth_to_groundwater.tif     # ⚠️ Raster (color-coded categories)
│   ├── regional_geology.geojson
│   └── combined_sewer_basins.geojson
│
├── sewer/
│   ├── storm_nodes.geojson
│   ├── storm_pipes.geojson
│   └── inlets.geojson
│
├── impervious/
│   ├── building_footprints.geojson
│   └── impervious.tif               # ✅ NOAA C-CAP 2021, binary (0/1), 3ft pixels
│
├── trees/
│   └── street_trees.geojson
│
├── curbs/
│   └── Curbs.geojson
│
├── zoning/
│   └── zoning.geojson               # ✅ 111 polygons
│
├── collection_system_lines/
│   ├── shp/                         # Full shapefile (360K features)
│   └── Collection_System_Lines.geojson
│
├── validation/
│   └── gsi_facilities.geojson       # ✅ 176 facilities
│
├── derived/                          # ✅ Computed from DEM
│   ├── slope.tif                    # Degrees, 0.0–23.2
│   ├── flow_direction.tif           # D8 direction index (0-7, -1=sink)
│   ├── flow_accumulation.tif        # Upstream cell count, 1–12,091
│   ├── twi.tif                      # Topographic Wetness Index, 2.1–17.4
│   └── segment_attributes.geojson   # ✅ 832 segments with all FIS inputs
│
├── soils/                            # TODO
│   └── ssurgo_ksat.geojson
│
├── canopy/                           # TODO
│   └── tree_canopy.tif
│
└── reference/                        # TODO
    └── design_storms.json
```

---

## Next Steps

1. ~~**Flow Analysis** — Calculate D8 flow direction and accumulation from DEM~~ ✅ Done (2026-02-10)
2. **Network Analysis** — Use street node IDs to build network graph
3. ~~**Attribute Extraction** — Extract soil, slope, impervious values per segment~~ ✅ Done (2026-02-10)
4. **FIS Development** — Implement fuzzy inference system for suitability rating
5. **Validation** — Compare model outputs against 176 existing GSI facilities

---

## References

- [Portland Street_Centerlines MapServer](https://www.portlandmaps.com/arcgis/rest/services/Public/Street_Centerlines/MapServer)
- [Portland Open Data Portal](https://gis-pdx.opendata.arcgis.com/)
- [BES Stormwater System Plan MapServer](https://www.portlandmaps.com/arcgis/rest/services/Public/Stormwater_System_Plan/MapServer)
- [Web Soil Survey](https://websoilsurvey.nrcs.usda.gov/app/)
- [Oregon Metro RLIS](https://rlisdiscovery.oregonmetro.gov/)
- [BES Stormwater Management Manual](https://www.portland.gov/bes/stormwater/swmm)
