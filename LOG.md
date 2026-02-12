# Project Log

Running log of decisions, discoveries, and progress for the Basalt Broth project. Intended as raw material for the Medium blog series (https://medium.com/@edinspace).

---

## 2026-02-02 — Project Kickoff

### Starting point
Had an initial brainstorming conversation with Claude about using agent-based modeling in NetLogo to optimize bioswale placement in Portland, OR. Identified a real research gap: nobody has combined dynamic ABM water flow simulation with real GIS data for bioswale siting. Existing work is either static GIS overlay analysis (EPA BST, AHP methods) or ABMs focused on social adoption and maintenance — not physical placement optimization.

### Key decisions made
- **Study area:** Colonial Heights neighborhood, SE Portland. Starting small with a neighborhood I know, then expand. Roughly bounded by Powell Blvd, 26th Ave, Holgate Blvd, and 33rd Ave.
- **Storm events:** Design storms (2-yr, 10-yr, 25-yr return periods) rather than historical time series. Matches how BES actually sizes infrastructure.
- **Flow routing:** Simplified D8 (each cell drains to steepest downhill neighbor). Good enough for relative site comparison without the complexity of Manning's equation.
- **Optimization:** BehaviorSpace parameter sweeps first (NetLogo's built-in tool). Upgrade to genetic algorithm if the search space gets too large.
- **Output format:** Medium blog series documenting the build process and findings.

### Data landscape
Did a deep dive into available GIS data. The situation is surprisingly good — almost everything is free and open:
- 1m LiDAR DEM from USGS 3DEP
- SSURGO soils (hydrologic soil groups, infiltration rates, depth to water table)
- Storm sewer network from Portland open data
- Street tree inventory (species, size, condition)
- Portland BES Stormwater System Plan MapServer — pre-computed layers for slope, soil groups, groundwater depth, geology
- DOGAMI surficial geology and geohazard maps
- Portland BES 2025 SWMM Appendix A for design storm parameters

Interesting discovery: Oregon is NOT covered by NOAA Atlas 14 (the modern precipitation frequency standard). Portland BES has their own locally-calibrated design storms instead, which is actually better for this project — same assumptions BES uses for real infrastructure.

Two gaps to solve: no ready-made impervious surface layer (will derive from building footprints + streets), and no public standalone dataset of existing GSI facility locations (may need to request from BES or dig through collection system attributes).

### Ideas for later
- Street trees / leaf litter as a factor — canopy intercepts rain but fallen leaves clog bioswale inlets. Seasonal angle could be compelling.
- Underlying geology and sinkhole risk — should we avoid infiltrating into certain formations? DOGAMI data could support a "don't bioswale here" constraint layer.

### What's next
- Start pulling GIS data for the Colonial Heights area
- Get NetLogo set up with the GIS extension
- Build the basic terrain model — load DEM, visualize elevation, get D8 flow routing working

---

## 2026-02-02 — First Data Pull

### Portland ArcGIS REST API layers
Wrote a Python script (`data/fetch_portland_layers.py`) to query Portland's ArcGIS REST services for the Colonial Heights bounding box. Successfully pulled 8 vector layers:

| Layer | Features | Source |
|-------|----------|--------|
| hydrologic_soil_groups | 17 polygons | Stormwater System Plan MapServer |
| regional_geology | 3 polygons | Stormwater System Plan MapServer |
| depth_to_bedrock | 34 polygons | Stormwater System Plan MapServer |
| combined_sewer_basins | 4 polygons | Stormwater System Plan MapServer |
| storm_nodes | 160 points | Utilities Sewer MapServer |
| storm_pipes | 55 lines | Utilities Sewer MapServer |
| inlets | 693 points | Utilities Sewer MapServer |

Two layers failed — `percent_slope` and `depth_to_groundwater` — because they're raster layers that don't support vector feature queries. We'll derive slope from the DEM ourselves (higher resolution anyway).

### DEM acquisition — the long road
First attempt: DOGAMI LiDAR tile `LDQ-45122E6` (5.1 GB zip). Contains multiple LiDAR collections (2005, 2009, 2014). Extracted the 2014 OLC Metro bare earth raster. Problem: only 12% valid pixels in our study area. Colonial Heights sits at the edge of the tile's LiDAR flight coverage.

Lesson learned: DOGAMI LDQ tiles contain raw LiDAR-derived DEMs that may have coverage gaps. The USGS 3DEP products are gap-filled and seamless — better for this kind of work.

Second attempt: USGS 3DEP 1m DEM via the S3 bucket. The TNM Access API returned zero results (broken/underpopulated for 1m data), but the S3 bucket at `prd-tnm.s3.amazonaws.com` has a predictable structure:
```
StagedProducts/Elevation/1m/Projects/{project_name}/TIFF/USGS_1M_{utm_zone}_x{e}y{n}_{project}.tif
```

Found `OR_OLCMetro_2019_A19` — the 2019 Oregon LiDAR Consortium Metro collection. Tiles are 10km x 10km in UTM Zone 10N. First downloaded the wrong tile (x52y503 — off by one, too far south). The tile naming convention puts the *upper edge* at the named northing × 10000.

Final result: `USGS_1M_10_x52y504_OR_OLCMetro_2019_A19.tif`, clipped to Colonial Heights as `colonial_heights_dem.tif`:
- **1,572 × 2,118 pixels at 1m resolution**
- **Elevation range: 16.2 ft to 59.5 ft** (~5m to 18m)
- **100% valid coverage**
- UTM Zone 10N (EPSG:26910)
- 13 MB compressed

Gotcha: GDAL caches raster statistics in `.aux.xml` sidecar files. When you overwrite a raster with the same filename, stale stats persist. Spent time confused by "12% valid" that was actually from the old DOGAMI clip. Always delete `.aux.xml` when reprocessing.

### Data inventory so far
- `data/dem/colonial_heights_dem.tif` — 1m bare earth DEM (2019 LiDAR)
- `data/dem/USGS_1M_10_x52y504_OR_OLCMetro_2019.tif` — full 10km tile (kept as source)
- `data/stormwater/*.geojson` — soil groups, geology, bedrock depth, sewer basins
- `data/sewer/*.geojson` — storm nodes, pipes, inlets
- `data/LDQ-45122E6.zip` — DOGAMI raw LiDAR (can delete, superseded by USGS)

### Still needed
- Building footprints (for impervious surface proxy)
- Street trees layer
- Existing GSI facility locations (for validation)
- SSURGO soil data (for infiltration rates — the MapServer soil groups are coarse)
- BES design storm tables (from SWMM Appendix A)

---

## 2026-02-02 — Study Area Change & CRS Standardization

### Expanded study area
Switched from Colonial Heights to a larger corridor: **Hawthorne Blvd to Division St (N–S), SE 20th Ave to Cesar Chavez / SE 39th Ave (E–W)**. More interesting urban variety — mix of commercial strips, residential blocks, and different street typologies.

Canonical study area extent defined in EPSG:2913: `(7650146, 675893) – (7658210, 680660)` ft.

### The QGIS alignment saga
Spent significant time debugging apparent spatial misalignment between the DEM and vector layers in QGIS. Layers appeared shifted ~2–3 blocks west relative to the OpenStreetMap basemap. Tried multiple CRS settings, reprojections, and basemap layers before realizing the actual issue: the DEM and vector layers had been fetched with *different* bounding boxes. The data was correctly georeferenced — it was just clipped to different extents. Lesson: when layers look offset, check the data extents before chasing CRS transformation issues.

### Choosing a project CRS
The DEM was initially in EPSG:4326 (WGS84, decimal degrees) which is awkward for distance/area calculations. Switched everything to **EPSG:2913 — Oregon North State Plane (NAD83/HARN, international feet)**. This is what Portland city agencies (BES, PBOT) use for infrastructure work, so our coordinates will match their systems natively.

Reprojected the DEM with `gdalwarp` at 3-foot pixel resolution.

### The tilted bounding box problem
First DEM clip had a diagonal nodata strip across the top — the bounding box wasn't a clean rectangle. Root cause: we defined the study area as a WGS84 rectangle and then reprojected to EPSG:2913. A rectangle in one CRS is a slightly rotated quadrilateral in another. The fix:

1. **Define the study area extent in EPSG:2913** (the target CRS), not WGS84.
2. **Clip in EPSG:2913** using `-te` (rasters) or `-clipdst` (vectors) — this clips *after* reprojection, producing clean axis-aligned rectangles.
3. **Over-fetch in WGS84** when querying web APIs that require it, then clip to the EPSG:2913 rectangle.

This also revealed a coverage gap: the study area straddled the northern edge of the USGS 3DEP tile (y504). That tile's north boundary is horizontal in UTM but diagonal in EPSG:2913, clipping through our study area. Downloaded the adjacent tile to the north (y505). `clip_dem.py` now mosaics all source tiles in one `gdalwarp` pass: UTM → EPSG:2913, clipped to the canonical extent.

Final DEM: 2,688 × 1,589 pixels, 3ft resolution, elevation 11.5–55.5 ft, **100% valid coverage**.

### Unified data refetch
Rewrote the data fetch script as `data/refetch_layers.py` to:
1. Query ArcGIS with an oversized WGS84 bbox (to catch all intersecting features)
2. Reproject and clip to the canonical EPSG:2913 rectangle via `ogr2ogr -clipdst`
3. Fetch building footprints and street trees (previously missing)

Final data pull results:

| Layer | Features | Directory |
|-------|----------|-----------|
| hydrologic_soil_groups | 12 | stormwater/ |
| holgate_lake_groundwater | 0 | stormwater/ |
| regional_geology | 8 | stormwater/ |
| depth_to_bedrock | 24 | stormwater/ |
| combined_sewer_basins | 3 | stormwater/ |
| storm_nodes | 511 | sewer/ |
| storm_pipes | 141 | sewer/ |
| inlets | 1,499 | sewer/ |
| street_trees | 10,626 | trees/ |
| building_footprints | 8,087 | impervious/ |

All files in EPSG:2913 clipped to the same rectangle as the DEM. `holgate_lake_groundwater` returned 0 features — that feature doesn't intersect this study area.

### Data inventory (current)
- `data/dem/study_area_dem.tif` — 1m DEM in EPSG:2913 (3ft pixels, 2019 LiDAR, 100% valid)
- `data/dem/USGS_1M_10_x52y504_OR_OLCMetro_2019.tif` — source tile (south)
- `data/dem/USGS_1M_10_x52y505_OR_OLCMetro_2019.tif` — source tile (north)
- `data/stormwater/*.geojson` — soil groups, geology, bedrock depth, sewer basins (EPSG:2913)
- `data/sewer/*.geojson` — storm nodes, pipes, inlets (EPSG:2913)
- `data/trees/street_trees.geojson` — 10,626 trees with species, DBH, condition (EPSG:2913)
- `data/impervious/building_footprints.geojson` — 8,087 buildings with type, year built (EPSG:2913)

### Scripts
- `data/clip_dem.py` — Mosaics USGS tiles, reprojects UTM→EPSG:2913, clips to study area. Run with `uv run data/clip_dem.py`.
- `data/refetch_layers.py` — Fetches vector layers from ArcGIS REST, reprojects and clips to EPSG:2913. Run with `uv run data/refetch_layers.py`.

### Still needed
- **Street/road impervious surfaces** — Building footprints alone don't capture streets, sidewalks, parking lots, driveways. Options to investigate: street centerlines + buffer by road class, taxlot inverse (gaps = right-of-way), Portland BES impervious layer (they calculate stormwater fees from impervious area — may have a high-res layer), or NLCD impervious raster (probably too coarse at 30m).
- Existing GSI facility locations (for validation)
- SSURGO soil data (for infiltration rates — the MapServer soil groups are coarse)
- BES design storm tables (from SWMM Appendix A)

---

## 2026-02-03 — NetLogo Setup

### Installation
NetLogo 7.0.3 installed to `~/tools/NetLogo 7.0.3/`. This version uses `.nlogox` format (XML) instead of the old plain-text `.nlogo` format.

### GIS extension limitations
The bundled GIS extension has significant format constraints:
- **Rasters:** Only ESRI ASCII Grid (`.asc`). GeoTIFF not supported.
- **Projections:** Limited set. Our EPSG:2913 (`Lambert_Conformal_Conic`) is NOT supported — NetLogo wants `Lambert_Conformal_Conic_2SP`. UTM (Transverse_Mercator) works.

**Solution:** Keep EPSG:2913 as canonical CRS for analysis. Convert to UTM Zone 10N (EPSG:26910) + ASCII Grid for NetLogo consumption.

```bash
gdalwarp -t_srs EPSG:26910 -tr 1 1 -r bilinear input.tif output_utm.tif
gdal_translate -of AAIGrid output_utm.tif output_utm.asc
```

### First successful DEM load
Created `netlogo/test_dem.nlogox` — minimal model that loads the DEM and colors patches by elevation. Works. Elevation range confirmed: 11.6 to 55.5 ft.

### Documentation
- Created `NETLOGO_FORMAT.md` with file format reference and GIS extension notes
- Referenced from `CLAUDE.md`

### D8 flow routing
Added D8 flow direction calculation — each patch identifies its steepest downhill neighbor. Then calculated flow accumulation (how many upstream cells drain through each patch). The flow accumulation pattern clearly shows the street grid — streets are engineered to collect and channel runoff, and the DEM captures that.

### Water agent simulation
Added water "droplets" that spawn randomly and flow downhill following the D8 routing. They collect along the same channels visible in the flow accumulation view, validating that the routing works. Water disappears when it reaches a sink (no downhill neighbor — represents storm drains or infiltration).

**Current model capabilities:**
- Load DEM from ASCII grid
- D8 flow direction calculation
- Flow accumulation calculation
- Visualization modes: elevation, flow accumulation, flow arrows
- Water agent simulation with adjustable rain intensity

**Next steps:**
- Add bioswale agents that intercept water
- Load building footprints as impervious layer
- Track runoff volume captured vs. escaped
- Make water pond at sinks instead of disappearing

---

## 2026-02-04 — New Data Sources

### Downloaded from Portland Maps
- **Curbs** (`data/curbs/Curbs.geojson`) — Line data of all curbs in the city. Defines actual drainage channels along streets; curb cuts are where bioswales receive runoff.
- **Collection System Lines** (`data/collection_system_lines/Collection_System_Lines.geojson`) — Includes all sewer/stormwater infrastructure. May contain bioswale/green street facility data — need to investigate UNITTYPE values once re-downloaded.

Note: First download was missing some features. Re-downloading.

---

## 2026-02-10 — Data Gap Analysis & Processing Pipeline

### Data gap audit
Reviewed all source data against FIS input requirements. Found three issues:

1. **HSG 39% null coverage** — MUSYM `50C` (Urban Land) covers 39% of study area with `HydrolGrp = None`. SSURGO doesn't assign hydrologic properties to heavily developed areas. Per USDA/NRCS guidance (NEH Chapter 7) and TR-55, assign HSG D to Urban Land (compacted soils perform worse than native classification). DATA_PLAN.md originally marked HSG as "Ready" — updated to document the gap and workaround.

2. **Groundwater raster is RGB** — `depth_to_groundwater.tif` is a 3-band symbolized map image, not numeric depth data. Already documented in DATA_PLAN.md with workaround (assume >5ft clearance for SE Portland).

3. **Impervious surface source found** — NOAA C-CAP 2021 provides 1m resolution impervious surface data for all of Oregon (416 MB). Downloaded, clipped to study area, reprojected to EPSG:2913. Result: 60.5% of study area is impervious. This replaces the planned approach of buffering street centerlines by road class.

### New scripts and derived data

**`data/clip_impervious.py`** — Unzips C-CAP Oregon raster, clips to study extent, reprojects to EPSG:2913 at 3ft pixels.

**`data/calc_flow.py`** — Computes from DEM:
- `derived/slope.tif` — 0.0–23.2 degrees (median 0.66°)
- `derived/flow_direction.tif` — D8 direction index (0-7, -1=sink)
- `derived/flow_accumulation.tif` — 1–12,091 upstream cells
- `derived/twi.tif` — Topographic Wetness Index 2.1–17.4

**`data/extract_attributes.py`** — Buffers each of 834 street segments by 50ft, samples all rasters, spatial-joins HSG, computes inlet distance. Output: `derived/segment_attributes.geojson` (832 segments, 2 skipped as <20ft).

Per-segment attribute ranges:
| Attribute | Min | Median | Max |
|-----------|-----|--------|-----|
| slope_deg | 0.3 | 1.0 | 2.3 |
| impervious_pct | 3.1 | 70.3 | 100.0 |
| twi | 6.5 | 7.0 | 7.8 |
| flow_accum | 6.2 | 18.6 | 297.9 |
| inlet_dist_ft | 10.1 | 107.0 | 371.0 |
| HSG | B: 786 segments | | D: 46 segments |

### GDAL Python bindings
Installed `gdal==3.12.1` Python package to match system GDAL. Required for raster I/O in processing scripts. Rasterio has numpy binary incompatibility (built against older numpy) — not usable without reinstall.

### Next steps
- ~~Implement two-stage FIS in scikit-fuzzy~~ Done (2026-02-10) — used vectorized numpy instead
- ~~Validate against 176 existing GSI facilities~~ Done (2026-02-10)

---

## 2026-02-10 — Two-Stage FIS Implementation & Validation

### FIS implementation
Implemented the two-stage Fuzzy Inference System in `data/fis_suitability.py`. Adapted from BRAT's cascaded architecture but implemented as vectorized numpy operations over the full 2688×1589 raster grid (4.3M cells) rather than using scikit-fuzzy. This runs in seconds and keeps dependencies minimal (numpy + gdal + scipy).

**Key design decision: raster-based, not segment-based.** The earlier `extract_attributes.py` averaged raster values over 50ft street segment buffers, which collapsed TWI from a 2.1–17.4 range down to 6.5–7.8. Operating at cell level preserves the full variance and produces spatial maps for both visualization and NetLogo consumption.

**Stage 1 — Physical Suitability** (slope × HSG → suitability 0-1):
- 16 rules with trapezoidal membership functions
- Suitability range: 0.10–0.70, mean 0.585
- Most cells ≈0.60–0.70 (ideal slope + HSG B); HSG D patches drop to ≈0.30

**Stage 2 — Capture Priority** (suitability × impervious fraction × TWI → priority 0-1):
- 48 rules across 4 suitability × 4 impervious × 3 TWI categories
- Priority range: 0.10–0.775, mean 0.435
- Priority max doesn't reach 0.90 because no HSG A soils in study area caps suitability at 0.70

**Preprocessing steps built in:**
- Rasterized HSG polygons → `derived/hsg_raster.tif` (96.3% B, 3.7% D)
- Computed 11×11 box mean of binary impervious → `derived/impervious_fraction.tif` (mean 0.605, median 0.653)
- Groundwater skipped (RGB raster, not numeric) — constant safe value for SE Portland

**Defuzzification:** Weighted-average (Sugeno-style approximation of Mamdani centroid). Each rule's firing strength = min of antecedent memberships. All vectorized.

### Outputs
| File | Description |
|------|-------------|
| `derived/hsg_raster.tif` | Rasterized HSG (1-4) |
| `derived/impervious_fraction.tif` | 11×11 box mean of impervious |
| `derived/fis_suitability.tif` | Stage 1 physical suitability (0-1) |
| `derived/fis_priority.tif` | Stage 2 capture priority (0-1) |
| `derived/fis_suitability_utm.asc` | Stage 1 in ASCII Grid for NetLogo (EPSG:26910) |
| `derived/fis_priority_utm.asc` | Stage 2 in ASCII Grid for NetLogo (EPSG:26910) |
| `derived/fis_priority_color.tif` | RGB color-mapped priority for quick visualization |

### Visual inspection
Opened priority raster in QGIS with red-yellow-green color ramp and GSI facility overlay. Key observations:
- Streets light up as high-priority corridors (green) — correct, bioswales go in right-of-way
- Residential block interiors are orange/red (lower impervious fraction)
- Parks and open spaces correctly flagged as low priority
- GSI facilities (black lines) overwhelmingly sit on or adjacent to green corridors
- Spatial pattern dominated by impervious fraction because suitability is uniformly high (96% HSG B, gentle slopes). This is physically valid — in a uniformly suitable area, runoff generation drives placement.

### Statistical validation
Validated against 176 GSI facilities in the study area. Five complementary tests:

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Mann-Whitney U | p = 3.1×10⁻¹¹ | Facilities in significantly higher-priority areas |
| Rank-biserial r | 0.287 | Medium effect size |
| K-S test | D = 0.279, p = 1.8×10⁻¹² | Facility CDF shifted right |
| AUC-ROC | 0.645 | Above random; modest because presence-only data |
| **Boyce Index** | **B = 0.915** (p = 0.0002) | Near-perfect monotonic preference for high-priority areas |
| Mean percentile | 64th | 14 points above random (50th) |
| Top-quartile enrichment | 38.6% | vs. 25% expected |

The **Boyce Index is the headline metric** — it's specifically designed for presence-only suitability validation (Hirzel et al. 2006). The P/E ratio increases monotonically from 0.09 in the lowest-priority bin to 1.84 in the highest, meaning facilities are progressively more concentrated in areas the FIS rates highly.

The AUC of 0.645 is modest but expected: AUC requires true negatives (sites considered and rejected), which we don't have. It also can't account for non-physical siting factors (land ownership, politics, project bundling).

### Technical notes
- Used `ogr.GetDriverByName("MEM")` instead of deprecated `"Memory"` for GDAL 3.11+
- `np.trapezoid()` replaces deprecated `np.trapz()` in newer numpy
- Integral-image (summed area table) approach for box mean — O(n) instead of O(n×k²)

### Next steps
- ~~Integrate FIS outputs into NetLogo ABM (load ASCII grids as patch variables)~~ Done (2026-02-11)
- ~~Add bioswale agents that use priority scores for placement decisions~~ Done (2026-02-11)
- Explore whether larger smoothing window (e.g., 33×33 = block-scale) improves validation metrics

---

## 2026-02-11 — FIS Integration into NetLogo ABM

### Bioswale agents and water-bioswale interaction
Integrated the FIS outputs (`fis_suitability_utm.asc`, `fis_priority_utm.asc`) into the NetLogo model. Setup now loads all three GIS layers (DEM + two FIS rasters). The different source resolutions (DEM at 1.0m, FIS at ~0.914m) are handled transparently by `gis:apply-raster`, which samples each raster at patch centers.

**New agent type: bioswales** — placed on the highest FIS-priority patches. Properties:
- `capacity` (10 units) — max water storage
- `infiltration-rate` (`suitability × 0.5`) — drainage per tick, simulating percolation into soil
- `captures` — lifetime counter

**Water-bioswale interaction in `go` loop:**
1. Water moves downhill (existing D8 routing)
2. Bioswale capture: water on a bioswale patch gets absorbed if capacity remains (mid-flow interception, not just at sinks)
3. Sink escape: water at sinks without bioswale capture dies as "escaped"
4. Bioswale infiltration: stored water drains at `infiltration-rate` per tick, giving bioswales renewable capacity

**New interface elements:**
- Suitability / Priority visualization buttons (red→green HSB gradient via `approximate-hsb`)
- Place Bioswales / Remove buttons
- `num-bioswales` slider (10–500), `bioswale-spacing` slider (2–30 patches)
- Monitors: Captured, Escaped, Capture %, Bioswales, Water
- Capture Rate time-series plot

### Resolution bump: ~9.3m → 5m per patch
Original world was 269×159 patches (~9.3m/patch). Increased to 500×305 patches (~5m/patch). This gives 2–3 patches across a street width — enough to distinguish sides. Setup time was not noticeably different (152K patches is well within NetLogo's comfort zone). Could push to 2.5m (1000×610 = 600K patches) if finer resolution needed.

### Flow-direction-aware bioswale spacing
Initial bioswale placement just took the top N patches by priority — resulted in clumping because spatially correlated priority scores produce adjacent high-value patches. Real bioswales are spaced ~one per block along each side of a street, but paired bioswales across the street from each other are common.

**Solution: two-tier spacing using flow direction as a proxy for "side of street."**
- Computed `flow-heading` for each patch (heading toward its `flow-to` neighbor)
- Hard minimum gap of 3 patches (~15m) — no two bioswales this close regardless
- Full spacing (default 10 patches / ~50m) enforced only when flow headings are within 90° (same side of street)
- Patches with flow headings >90° apart (opposite sides) bypass full spacing — they serve independent drainage paths

This works because patches on opposite sides of a street drain toward opposite gutters (~180° difference), while same-side patches drain in the same direction (~0° difference). Caveat: if the DEM doesn't capture the street crown cross-slope, both sides may show longitudinal flow, and the algorithm falls back to conservative uniform spacing.

### Bug fix
Changed `flow-to != nobody` to `is-patch? flow-to` throughout. Patch variables default to `0` (not `nobody`) after `clear-all`, so `!= nobody` incorrectly included nodata patches. The existing code worked by coincidence (nodata patches never had water on them), but `is-patch?` is the correct check per NetLogo semantics.

### Current model capabilities
- Load DEM + FIS suitability + FIS priority from ASCII grids
- D8 flow direction and accumulation
- Visualization modes: elevation, flow accumulation, flow arrows, suitability, priority
- Bioswale placement with FIS-priority ranking and flow-direction-aware spacing
- Water simulation with bioswale capture, sink escape, and infiltration
- Real-time metrics: capture count, escape count, capture %, time-series plot

### Next steps
- Validate bioswale placement patterns against Portland BES facility locations
- Add storm event profiles (design storms with temporal distribution, not just uniform random rain)
- Consider loading street centerlines to improve flow routing (streets as preferential flow paths)
- Explore computational scaling — can we go to 2.5m resolution? 1m?
