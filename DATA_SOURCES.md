# Data Sources

GIS and reference data for the Colonial Heights study area (SE Portland, OR). Almost everything listed here is free and open.

## DEM / Elevation

**USGS 3DEP 1-Meter DEM**
- Resolution: **1 meter** (LiDAR-derived bare-earth surface)
- Format: GeoTIFF / Cloud Optimized GeoTIFF
- CRS: UTM Zone 10N, NAD83, elevations in meters (NAVD88)
- Download: https://apps.nationalmap.gov/downloader/ — zoom to Portland, select "Elevation Products (3DEP)" > "1 meter DEM"
- Also available via OpenTopography (clip to custom AOI): https://portal.opentopography.org/raster?opentopoID=OTNED.012021.4269.3
- Cost: Free, no account required

## Soils

**SSURGO — Soil Survey Geographic Database (Multnomah County)**
- Key attributes: Hydrologic soil group (A/B/C/D), saturated hydraulic conductivity (Ksat), depth to water table, depth to restrictive layer, drainage class
- Format: Shapefile + Access database tables (vector polygons at ~1:24,000 scale)
- Download: https://websoilsurvey.nrcs.usda.gov/app/ — draw AOI around Colonial Heights
- Cost: Free

**gSSURGO — Gridded SSURGO (Oregon statewide)**
- Same data rasterized at 10m resolution — easier to work with in GIS
- Format: Esri File Geodatabase
- Download: https://www.nrcs.usda.gov/resources/data-and-reports/gridded-soil-survey-geographic-gssurgo-database
- Cost: Free

## Storm Sewer Network

**Collection System Lines** (pipes, channels, and facilities)
- Download: https://gis-pdx.opendata.arcgis.com/datasets/collection-system-lines
- Format: Shapefile, GeoJSON, CSV, KML
- Key fields for filtering:
  - `SYSTEM`: "STORM" vs "SEWER" (sanitary)
  - `SYMBOL_GRO`: Includes "GREEN STREET FACILITY", "STORM GRAVITY MAIN", etc.
  - `OWNRSHIP`: "BES" (Portland), "CLAK" (Clackamas), etc.
- **Green infrastructure**: Filter by `SYMBOL_GRO = "GREEN STREET FACILITY"` to find existing bioswales/GSI

**Collection System Points** (manholes, junctions)
- Download: https://gis-pdx.opendata.arcgis.com/datasets/collection-system-points
- Format: Shapefile, GeoJSON, CSV, KML

**Storm Sewer Detail (REST API)** — richer than flat downloads
- Endpoint: https://www.portlandmaps.com/arcgis/rest/services/Public/Utilities_Sewer/MapServer
- Key sublayers: Storm Nodes (6), Storm Pipes (7), Surface Water (9), Inlet (19), Inlet Leads (20)
- Queryable by bounding box, exportable as JSON/GeoJSON

## Stormwater System Plan Layers (Portland BES)

Pre-computed layers directly relevant to bioswale siting feasibility.

- Endpoint: https://www.portlandmaps.com/arcgis/rest/services/Public/Stormwater_System_Plan/MapServer
- Key sublayers:
  - Layer 2: **Dominant Hydrologic Soil Groups (HSG)** — infiltration capacity
  - Layer 5: **Depth to Seasonal High Groundwater (USGS)**
  - Layer 7: **Holgate Lake Supplemental Depth to Groundwater** — Colonial Heights is near this area
  - Layer 11: **Percent Slope**
  - Layer 12: **Regional Geology**
  - Layer 13: **Depth to Lithic Bedrock**
  - Layer 14: **Depth to Fragipan**
  - Layer 16: **Combined Sewer Basins** — CSO areas benefit most from GSI
- Format: ArcGIS REST (queryable, exportable as JSON/GeoJSON)
- Cost: Free

## Impervious Surfaces

**NOAA C-CAP 2021 High-Resolution Impervious Surface** ✅ IN USE
- Resolution: **1 meter** (derived from 30cm aerial imagery via Ecopia AI classification + expert review)
- Format: GeoTIFF (binary: 0=pervious, 1=impervious)
- Coverage: All of Oregon (416 MB zip)
- Download: https://coastalimagery.blob.core.windows.net/ccap-landcover/CCAP_bulk_download/High_Resolution_Land_Cover/Phase_1_Initial_Layers/Impervious/index.html
- Cost: Free (restriction: may not be used for ML training for 5 years from creation)

Other sources considered:
1. **Building Footprints** — https://gis-pdx.opendata.arcgis.com/datasets/building-footprints — buildings only, misses streets/sidewalks/parking
2. **NLCD Impervious Surface** — 30m resolution (too coarse for parcel-level siting)
3. **Portland BES stormwater billing data** — per-parcel impervious area, but not publicly downloadable

## Existing Green Infrastructure Locations (for validation)

**Collection System Lines** — contains green street facilities
- Same dataset as storm sewer pipes (see above)
- Filter: `SYMBOL_GRO = "GREEN STREET FACILITY"` or `DETAIL_SYM = "GREEN STREET FACILITY"`
- Includes bioswales, stormwater planters, and other GSI
- Example: OBJECTID 260046 is a green street facility at APN564-APN565 (installed 2011)

Additional resources:
1. **Collection System Points** — may include GSI facility nodes coded by type
2. **BES data request** — for comprehensive internal GIS database of all ~3,000+ GSI facilities
3. **BES Stormwater info**: https://www.portland.gov/bes/stormwater
4. **BES facility monitoring reports**: https://www.portland.gov/bes/stormwater/stormwater-facility-monitoring

## Street Trees

**Street Tree Inventory — Active Records**
- Point dataset with species, size, condition
- Download: https://gis-pdx.opendata.arcgis.com/datasets/PDX::street-tree-inventory-active-records/about
- Format: Shapefile, GeoJSON, CSV, KML
- Cost: Free

## Tree Canopy

**Oregon Metro RLIS Canopy 2019**
- LiDAR-derived tree canopy coverage
- Download: https://rlisdiscovery.oregonmetro.gov/datasets/b6da4ea243df4ba492d47860964cf2b5
- Cost: Free

## Zoning / Land Use

**City of Portland Zoning**
- Download: https://gis-pdx.opendata.arcgis.com/datasets/zoning/about
- Format: Shapefile, GeoJSON, CSV, KML
- Cost: Free

## Geology

**DOGAMI Surficial Geology (Greater Portland)**
- Open-File Report O-12-02: LiDAR-based surficial geologic map
- Format: Esri File Geodatabase + map plate PDF
- Download: https://d3itl75cn7661p.cloudfront.net/dogami/ofr/p-O-12-02.htm
- Cost: Free

**OGDC-8 — Oregon Geologic Data Compilation, Release 8**
- Statewide geodatabase with most current geologic mapping
- Format: Esri File Geodatabase
- Download: https://www.oregon.gov/dogami/pubs/Pages/dds/p-OGDC-8.aspx
- Cost: Free

## Geohazards

**DOGAMI HazVu Viewer** — landslide, liquefaction, flood, earthquake shaking
- Viewer: https://gis.dogami.oregon.gov/maps/hazvu/
- Downloadable GIS layers from DOGAMI GIS page

**SLIDO — Statewide Landslide Information Database for Oregon**
- Mapped landslide deposits and scarps
- Accessible via HazVu and as downloadable data

## Precipitation / Design Storms

**Important: Oregon is NOT covered by NOAA Atlas 14.** Use Portland BES local data instead.

**Portland BES 2025 Stormwater Management Manual (SWMM)**
- Appendix A contains Portland-specific design storm tables:
  - Table A-14: 24-hour design rainfall depths by return period (2-yr, 5-yr, 10-yr, 25-yr, etc.)
  - Portland-modified NRCS 24-Hour Type 1A hyetograph (10-minute time steps over 24 hours)
  - Water quality design storm: 1.61 inches / 24 hours
- Manual: https://www.portland.gov/bes/stormwater/swmm
- Appendix A download: https://www.portland.gov/bes/documents/stormwater-management-manual-2024-updates-appendix-stormwater-design-methods/download
- Design details / CAD files: https://www.portland.gov/bes/stormwater/2025-stormwater-management-manual/design-details-and-cad-support-files
- Cost: Free

**NOAA Atlas 2, Volume 10 (Oregon)** — older (1973) but still the federal reference
- Point estimates: https://hdsc.nws.noaa.gov/pfds/other/or_pfds.html — enter ~45.50N, 122.63W for Colonial Heights
- Full document: https://repository.library.noaa.gov/view/noaa/22621
- Cost: Free

**ODOT Regional Precipitation-Frequency Study** — more modern regional estimates
- Report: https://www.oregon.gov/ODOT/Programs/ResearchDocuments/SPR656_Rainfall_Analysis_Final_Report_web.pdf

**Portland BES Rainfall Gauge Data** (observed, historical)
- https://www.portland.gov/bes/rainfall-data-portland

## Oregon Metro RLIS (Bulk)

200+ spatial layers for the Portland metro region. Most are free under Open Database License.
- Discovery portal: https://rlisdiscovery.oregonmetro.gov/
- Bulk download (popular layers): https://rlisdiscovery.oregonmetro.gov/datasets/a7369e312baa435eab410a7015f819ec
- Tax lot ownership data requires paid license; geometry is free

## Known Gaps

1. ~~**Impervious surfaces**~~ — ✅ Resolved. Using NOAA C-CAP 2021 (1m resolution).
2. **NOAA Atlas 14** — does not cover Oregon. BES SWMM Appendix A is the authoritative local source.
3. **SSURGO Ksat values** — `soils/` directory is empty. Hydrologic soil groups acquired but 39% is Urban Land (null HSG). Full SSURGO download from Web Soil Survey needed for continuous infiltration rates.
