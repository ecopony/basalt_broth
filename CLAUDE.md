# Basalt Broth — Bioswale Placement Optimization (Portland, OR)

## Project Summary

Agent-based model (ABM) in NetLogo that simulates stormwater runoff across Portland's real terrain and infrastructure using GIS data, then optimizes where bioswales would have the greatest impact. This is novel — no published ABM exists for bioswale placement optimization, and no NetLogo model exists for green infrastructure siting.

## Core Architecture

**Platform:** NetLogo 7 with GIS extension. See `NETLOGO_FORMAT.md` for file format details and GIS extension limitations.

### Agent Types

- **Water parcels** — Spawn from rainfall, flow downhill over impervious surfaces following DEM, accumulate pollutants, get intercepted by bioswales or enter storm drains
- **Bioswales** — Candidate placements with capacity/infiltration rates derived from soil type and sizing. Capture and process water agents
- **Optimization agents** — Explore candidate placements, evaluate metrics, iteratively improve configurations

### GIS Data Layers

- DEM / slope (flow direction and accumulation)
- Impervious surfaces (roads, parking lots, rooftops)
- Storm sewer network
- Existing bioswale locations (~3,000+ facilities, used for validation)
- Soil permeability / hydrologic soil groups
- Land use / zoning (placement constraints)
- Precipitation data (storm events)

### Data Sources

- City of Portland Open Data Portal: gis-pdx.opendata.arcgis.com
- Oregon Metro RLIS: 200+ spatial layers
- Portland BES: green infrastructure facility locations and performance data
- USGS/USDA: DEM, SSURGO soil surveys, hydrologic data
- Oregon DEQ: water quality, CSO records

## Optimization Objectives (Multi-Objective)

1. Runoff volume reduction
2. Pollutant removal effectiveness (bioswales can achieve >90% TSS removal, 50-80% runoff volume reduction)
3. Construction and maintenance cost
4. Equitable distribution across neighborhoods (environmental justice)
5. Climate scenario resilience (current vs. projected rainfall)

## Validation Strategy

Compare model-recommended placements against Portland's existing 3,000+ facility locations. Assess whether the model identifies similar high-value sites and surfaces new candidate locations.

## Key Bioswale Siting Constraints

- Max slope: 3:1
- Max soil clay content: 5%
- Min 5-foot clearance to groundwater table
- Infiltration rate requirements vary by soil type

## What Makes This Novel

- First ABM combining dynamic water flow simulation with real GIS for bioswale placement
- Existing work is either static GIS overlay (EPA BST, AHP methods) or ABM focused on adoption/maintenance — not physical siting
- NetLogo provides accessibility and reproducibility vs. heavyweight tools (SWMM, SUSTAIN, etc.)
- Portland's 30-year GSI track record enables unique validation opportunity

## Research Context

**Status: Literature review complete (2026-02-04)**. See `research/RESEARCH_SYNTHESIS.md` for full findings.

Prior ABM work in green infrastructure:
- G-SSA (2021): social adoption dynamics, not physical placement
- Detention basin maintenance ABM (2023): maintenance optimization
- NJIT dynamic GI optimization (2024): permeable pavement maintenance
- ASCE GI Plans ABM (2024): regulatory interplay modeling

None model dynamic runoff to drive placement decisions. **Novel contribution confirmed.**

## Validated Methodology

Based on literature review, the project uses:

### Two-Stage Fuzzy Inference System (adapted from BRAT)
- **Stage 1**: Physical suitability (slope + soil + groundwater → infiltration score)
- **Stage 2**: Capture potential (infiltration + impervious + TWI → priority rating)
- **Implementation**: Python scikit-fuzzy, Mamdani inference, centroid defuzzification
- **Validation target**: ~90% accuracy (BRAT achieved 89.97% against 8,060 beaver dams)

### Hybrid Flow Routing (urban-adapted)
Standard D8 flow accumulation has significant limitations in urban areas (pipes cross ridges, curbs redirect flow, discrete inlet capture). Use instead:
- Modified D8 with streets as preferential flow paths
- Topographic Wetness Index (TWI) for accumulation hotspots
- Discrete inlet capture model
- Pipe network integration where data available

### Key Research Findings
- **FIS is appropriate**: handles fuzzy boundaries, non-linear interactions, expert knowledge
- **Portland has 3,000+ facilities** for validation (analogous to BRAT's 8,060 dams)
- **Equity is explicit gap**: only 11% of GI plans define it - opportunity for contribution
- **Strahler ordering**: valid for network simplification, NOT for siting decisions

## Study Area

**Hawthorne-Division corridor, SE Portland** — bounded by SE Hawthorne Blvd (north), SE Division St (south), SE 20th Ave (west), and Cesar Chavez Blvd / SE 39th Ave (east).

**Canonical study area extent (EPSG:2913, Oregon North State Plane, ft):**
```
xmin: 7650146    ymin: 675893
xmax: 7658210    ymax: 680660
```
This is ~8,064 × 4,767 ft (~2,458 × 1,453 m). All clipping happens in EPSG:2913 — see Projection Rules below.

The area sits on the western slope descending toward the Willamette, with elevation ranging from 12 ft to 55 ft. Mix of residential lots with varying impervious cover. Drains into the combined sewer system that historically contributed to CSO events. BES has been actively deploying green infrastructure in SE Portland, so there should be existing facilities nearby for validation.

## Projection Rules

**Project CRS: EPSG:2913** — NAD83(HARN) / Oregon North (international feet). This is what Portland city agencies use.

Three rules to avoid distorted bounding boxes:

1. **Define the study area extent in the target CRS (EPSG:2913), not in WGS84.** A rectangle in WGS84 is a slightly rotated quadrilateral in any projected CRS. If you clip in WGS84 and then reproject, you get tilted edges and nodata wedges in corners.
2. **Use `-te` (rasters) or `-clipdst` (vectors) with EPSG:2913 coordinates.** This clips *after* reprojection, giving clean axis-aligned rectangles.
3. **Over-fetch in WGS84, then clip in EPSG:2913.** When querying web APIs that require WGS84 (ArcGIS REST), use a slightly oversized WGS84 bbox to ensure full coverage, then clip the results to the EPSG:2913 rectangle.

The canonical extent lives in `scripts/clip_dem.py` and `scripts/refetch_layers.py` as `STUDY_EXTENT_2913`.

## Open Questions / Decisions Needed

- [x] Scope: ~~single watershed vs. city-wide?~~ Hawthorne-Division corridor, SE Portland (Hawthorne to Division, SE 20th to Cesar Chavez)
- [x] Storm event modeling: ~~design storms vs. historical time series?~~ Design storms (2-yr, 10-yr, 25-yr return periods). Standard BES sizing practice. Can add historical time series later.
- [x] Optimization approach: ~~genetic algorithm, simulated annealing, or NetLogo BehaviorSpace parameter sweeps?~~ BehaviorSpace parameter sweeps to start (built-in, fast iteration). Upgrade to genetic algorithm if search space gets too large.
- [x] Level of hydrologic fidelity: ~~simplified flow vs. full Manning's equation?~~ Simplified D8 flow routing (each cell drains to steepest downhill neighbor). Sufficient for relative site comparison. Can layer in Manning's equation later if needed.
- [x] Target output: ~~academic paper, planning tool, or both?~~ Series of Medium blog posts (https://medium.com/@edinspace). Document the build process and findings as we go.
- [ ] How to handle computational scaling (NetLogo performance with large GIS datasets)?
- [x] ~~Exact study area bounding box~~ — Hawthorne to Division, SE 20th to Cesar Chavez. See canonical EPSG:2913 extent above.

## Future Enhancements (Backlog)

- **Street trees / leaf litter** — Tree canopy intercepts rainfall (reducing effective precipitation on the ground) but fallen leaves clog bioswale inlets and reduce infiltration capacity. Portland has a street tree inventory dataset. Seasonal modeling of leaf-fall could be a compelling addition.
- **Underlying geology / sinkhole risk** — Not all locations are safe to infiltrate into. Karst-like conditions, expansive clays, or shallow bedrock could make bioswale infiltration counterproductive or dangerous. USGS surficial geology maps and DOGAMI (Oregon Dept of Geology and Mineral Industries) hazard data could inform a "don't infiltrate here" constraint layer.
