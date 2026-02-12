# Research Plan: Multi-Method Bioswale Placement Optimization

**Date:** 2026-02-04
**Status:** Research Complete - Implementation Ready

---

## Executive Summary

This document outlines a **scientifically validated** research plan for developing a bioswale placement optimization system for Portland, OR. The approach has been validated through extensive literature review (see `research/RESEARCH_SYNTHESIS.md`).

### Validated Approach

1. **Fuzzy Inference System (FIS)** for suitability scoring - validated by BRAT's 89.97% accuracy against 8,060 beaver dams
2. **Hybrid flow routing** for urban areas - modified D8 + TWI + discrete inlet capture
3. **Street segment analysis** with graph theory centrality metrics
4. **Validation against Portland's 3,000+ GSI facilities**
5. **Equity as explicit optimization objective** - addresses documented gap in current practice

### Novel Contribution (Confirmed)

No existing ABM combines dynamic water flow simulation with real GIS data for bioswale placement optimization. This project fills that gap with an accessible NetLogo implementation.

---

## Literature Review Summary

### Research Completed: 2026-02-04

Four parallel research investigations were conducted:

| Research Area | Key Finding | Document |
|---------------|-------------|----------|
| **BRAT FIS Methodology** | Two-stage cascaded FIS with trapezoidal membership functions; scikit-fuzzy implementation | `research/brat_fis_research.md` |
| **Urban Drainage Networks** | D8 has significant urban limitations; use hybrid approach with TWI and inlet capture | `research/urban_drainage_network_research.md` |
| **Portland BES Methods** | Clear siting criteria (3:1 slope, 5ft groundwater, <5% clay); 3,000+ facilities for validation | `research/portland_bes_methods_research.md` |
| **GI Siting Literature** | No ABM exists for dynamic water simulation + GI siting; equity is major gap | `research/gi_siting_literature_research.md` |

### What the Research Validates

1. **FIS is appropriate** - handles fuzzy boundaries, non-linear interactions, expert knowledge encoding
2. **Portland has excellent validation data** - 3,000+ facilities with monitoring, 2025 retrospective paper
3. **Standard siting criteria are well-established** - can use Portland BES thresholds directly
4. **Strahler ordering works** for network simplification (not siting decisions)
5. **Equity is an explicit gap** - only 11% of GI plans define it

### Critical Adjustments from Original Plan

| Original Assumption | Research Finding | Adjustment |
|---------------------|------------------|------------|
| D8 flow accumulation sufficient | D8 fails in flat urban areas, ignores pipes/curbs | Use hybrid: modified D8 + TWI + inlet capture |
| Strahler ordering for siting | Strahler is for network simplification only | Use for efficiency, not as siting criterion |
| Streets fully analogous to streams | Partial analogy - pipes cross ridges, discrete inlets | Respect infrastructure discontinuities |
| FIS approach is novel | FIS established (BRAT 2017) | Adapt proven architecture |

---

## Validated Methodology

### Two-Stage Fuzzy Inference System

**Architecture (adapted from BRAT):**

```
Stage 1: Physical Suitability FIS
┌─────────────────────────────────────────────────────────────┐
│  Inputs:                                                    │
│    - Slope (flat/moderate/steep/unsuitable)                │
│    - Soil infiltration rate (excellent/good/marginal/poor) │
│    - Groundwater depth (safe/adequate/marginal/unsuitable)  │
│                                                             │
│  Output: Infiltration Score (0-100)                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
Stage 2: Capture Potential FIS
┌─────────────────────────────────────────────────────────────┐
│  Inputs:                                                    │
│    - Infiltration Score (from Stage 1)                      │
│    - Upstream impervious area (low/moderate/high/very high) │
│    - Flow accumulation / TWI (minimal/low/moderate/high)    │
│    - Distance to storm drain (near/moderate/far)            │
│                                                             │
│  Output: Bioswale Priority (Unsuitable → Optimal)           │
└─────────────────────────────────────────────────────────────┘
```

**Technical Details:**
- **Membership functions:** Trapezoidal (gradual transitions at boundaries)
- **Inference type:** Mamdani
- **Defuzzification:** Centroid (center of gravity)
- **Implementation:** Python scikit-fuzzy library

### Siting Constraints (from Portland BES)

| Parameter | Requirement | Source |
|-----------|-------------|--------|
| Maximum slope | 3:1 (ideal 4:1) | Portland SWMM 2025 |
| Longitudinal slope | 1-6% | Portland SWMM |
| Groundwater clearance | 5 ft minimum | Portland SWMM, EPA |
| Maximum clay content | 5% | Portland SWMM |
| Infiltration rate | 1.0-6.0 in/hr | Minnesota Manual |

### Hydrologic Soil Groups

| Group | Infiltration | Runoff Potential | FIS Category |
|-------|--------------|------------------|--------------|
| A | >0.30 in/hr | Low | Excellent |
| B | 0.15-0.30 in/hr | Moderate | Good |
| C | 0.05-0.15 in/hr | Moderate-High | Marginal |
| D | <0.05 in/hr | High | Poor |

### Hybrid Flow Routing (Urban-Adapted)

Standard D8 flow accumulation fails in urban areas because:
- Pipes move water across topographic ridges
- Curbs redirect flow before natural low points
- Discrete inlet points create discontinuities
- Flat graded areas cause algorithm failure

**Solution:**
1. **Modified D8** with streets as preferential flow paths
2. **Topographic Wetness Index (TWI)** for accumulation hotspots: `TWI = ln(a / tan(b))`
3. **Discrete inlet capture** model (water agents intercepted at inlet locations)
4. **Pipe network integration** where data available

---

## Data Layers Required

| Layer | Source | Status | Purpose |
|-------|--------|--------|---------|
| DEM | USGS 3DEP 1m | Acquired | Flow routing, slope |
| Street centerlines | Portland Open Data | Acquired | Network skeleton |
| Hydrologic soil groups | BES MapServer | Acquired | Infiltration suitability |
| Depth to groundwater | BES MapServer | Acquired | Constraint layer |
| Impervious surfaces | Portland Open Data | Acquired | Runoff generation |
| Storm inlets | Portland Utilities | Need to verify | Discrete capture points |
| GSI facilities | Portland BES | Need to request | Validation dataset |

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Raw GIS Data                            │
│   (DEM, streets, soils, groundwater, impervious, inlets)   │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│           Step 1: Network Preparation                       │
│   - Split streets at intersections                          │
│   - Assign segment IDs                                      │
│   - Calculate Strahler order (for simplification only)      │
│   - Associate inlet locations to segments                   │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│           Step 2: Hybrid Flow Analysis                      │
│   - Modified D8 with street-as-channel routing              │
│   - Calculate TWI for accumulation hotspots                 │
│   - Delineate contributing area per segment                 │
│   - Identify inlet capture zones                            │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│           Step 3: Attribute Extraction                      │
│   - Buffer each segment (15m, 50m)                          │
│   - Zonal stats: soil group, groundwater depth              │
│   - Impervious % in contributing area                       │
│   - Slope calculation per segment                           │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│           Step 4: Two-Stage FIS                             │
│                                                             │
│   Stage 1: slope + soil + groundwater → infiltration_score  │
│   Stage 2: infiltration + impervious + TWI → priority       │
│                                                             │
│   Output: 5 categories (Unsuitable → Optimal)               │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│           Step 5: Equity Overlay                            │
│   - Environmental justice indicators by census tract        │
│   - Heat island vulnerability                               │
│   - Historical infrastructure investment                    │
│   - Produce equity-adjusted priority scores                 │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│           Step 6: Output & Validation                       │
│   - Write GeoPackage with segment ratings                   │
│   - Compare against Portland's 3,000+ GSI locations         │
│   - Calculate agreement metrics (target: ~90%)              │
│   - Generate maps for documentation                         │
└─────────────────────────────────────────────────────────────┘
```

---

## NetLogo ABM Integration

The pipeline produces segment ratings. NetLogo validates with dynamic simulation:

1. **Load segment ratings** as patch attributes
2. **Water agents** spawn from rainfall on impervious surfaces
3. **Flow routing** follows modified D8 / street channels
4. **Inlet capture** - water agents intercepted at drain locations
5. **Bioswale interception** - placed at candidate locations, capture passing water
6. **Optimization loop** - compare configurations, maximize capture efficiency

This combines **static analysis efficiency** (pipeline processes entire city) with **simulation validation** (confirms dynamic behavior).

---

## Research Tasks

### Phase 1: Research (COMPLETE)
- [x] BRAT FIS methodology research
- [x] Urban drainage network analysis methods
- [x] Portland BES siting criteria research
- [x] GI siting literature survey
- [x] Research synthesis document

### Phase 2: Data Preparation
- [x] DEM acquisition and processing
- [x] Vector layer fetch and CRS standardization
- [ ] Street network segmentation script
- [ ] Storm inlet location verification
- [ ] Request GSI facilities dataset from Portland BES

### Phase 3: Hydrologic Processing
- [ ] Modified D8 flow direction (street-aware)
- [ ] TWI calculation
- [ ] Contributing area delineation per segment
- [ ] Inlet capture zone modeling

### Phase 4: FIS Implementation
- [ ] Install and test scikit-fuzzy
- [ ] Implement Stage 1 FIS (physical suitability)
- [ ] Implement Stage 2 FIS (capture potential)
- [ ] Calibrate membership functions against Portland BES criteria

### Phase 5: Equity Integration
- [ ] Acquire census tract EJ indicators
- [ ] Heat island data for study area
- [ ] Develop equity weighting methodology
- [ ] Integrate into priority scoring

### Phase 6: NetLogo Model
- [ ] Load segment ratings into NetLogo
- [ ] Water agent implementation with hybrid routing
- [ ] Bioswale agent capture mechanics
- [ ] BehaviorSpace optimization runs

### Phase 7: Validation & Documentation
- [ ] Compare model vs. existing GSI locations (target ~90% agreement)
- [ ] Sensitivity analysis on FIS parameters
- [ ] Medium blog series
- [ ] GitHub repository documentation

---

## Key Design Decisions (Updated)

### Why FIS over Simple Weighted Overlay?
- **Handles non-linear interactions** - "IF slope IS steep THEN unsuitable" overrides other factors
- **Gradual boundaries** - 5.9% slope vs 6.1% slope shouldn't be binary
- **Encodes expert knowledge** - Engineering criteria as interpretable rules
- **Proven** - BRAT achieved 89.97% accuracy with this approach

### Why Hybrid Flow Routing?
- **D8 alone fails** in urban areas (flat terrain, pipes crossing ridges)
- **TWI captures accumulation** without requiring perfect flow routing
- **Discrete inlet model** matches actual urban hydrology
- **Street-as-channel** respects curb/gutter reality

### Why Include Equity?
- **Major documented gap** - only 11% of GI plans define equity
- **Portland already prioritizes** East Portland for underserved communities
- **Novel contribution** - most optimization focuses only on hydrology/cost
- **Aligns with project goals** - not just efficient, but just

---

## Validation Strategy

### Benchmark
BRAT achieved **89.97% accuracy** validating against 8,060 beaver dam locations.

### Portland Validation Dataset
- 3,000+ GSI facilities (bioswales, rain gardens, green streets)
- Performance monitoring data available
- 2025 MDPI paper: "The First Thirty Years of Green Stormwater Infrastructure in Portland"

### Validation Metrics
1. **Spatial agreement** - Do high-rated segments contain existing facilities?
2. **Ranking correlation** - Do existing facilities cluster in higher-priority segments?
3. **False negative analysis** - Do low-rated segments with facilities indicate model gaps?
4. **Novel site identification** - Can model identify high-potential unbuilt sites?

---

## Sources & Key References

### Core Methodology
- Macfarlane et al. (2017) - [Modeling riverscapes for beaver dams](https://www.sciencedirect.com/science/article/abs/pii/S0169555X15302166)
- [BRAT Documentation](https://brat.riverscapes.net/)
- [scikit-fuzzy](https://scikit-fuzzy.readthedocs.io/)

### Urban Hydrology
- [MDPI Water (2025) - Strahler for sewer networks](https://www.mdpi.com/2073-4441/17/7/990)
- [Water Resources Research (2022) - Network theory for drainage](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2022WR032277)

### Portland Sources
- [Portland SWMM 2025](https://www.portland.gov/bes/stormwater/2025-stormwater-management-manual)
- [MDPI Sustainability (2025) - 30 Years of Portland GSI](https://www.mdpi.com/2071-1050/17/15/7159)

### GI Siting
- [EPA BMPs Siting Tool](https://www.epa.gov/water-research/best-management-practices-bmps-siting-tool)
- [NACTO Bioswales Guide](https://nacto.org/publication/urban-street-design-guide/street-design-elements/stormwater-management/bioswales/)

### Environmental Justice
- [Taylor & Francis (2021) - EJ in GI Planning](https://www.tandfonline.com/doi/full/10.1080/1523908X.2021.1945916)

---

## Next Steps

1. **Request GSI data from Portland BES** - Email for existing facility locations
2. **Prototype scikit-fuzzy FIS** - Implement Stage 1 with Portland BES thresholds
3. **Street segmentation script** - Split network at intersections
4. **TWI calculation** - Alternative to pure D8 for accumulation
5. **Equity indicator acquisition** - Census tract EJ data for study area

---

*Research plan updated: 2026-02-04*
*Status: Research Complete - Ready for Implementation*
