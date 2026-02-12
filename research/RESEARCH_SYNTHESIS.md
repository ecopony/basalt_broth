# Research Synthesis: Bioswale Placement Optimization

**Date:** 2026-02-04
**Status:** Research Complete - Ready for Implementation Planning

---

## Executive Summary

This document synthesizes findings from four parallel research investigations conducted to establish scientific grounding for the Basalt Broth bioswale placement optimization model. The research validates our core approach while identifying critical methodological adjustments needed.

### Key Conclusions

1. **Fuzzy Inference Systems are appropriate** for bioswale siting - BRAT's 89.97% accuracy against 8,060 beaver dams demonstrates FIS validity for environmental siting
2. **Portland provides excellent validation data** - 3,000+ GSI facilities with performance monitoring, analogous to BRAT's validation approach
3. **The project represents a genuine novel contribution** - No published ABM combines dynamic water simulation with GI siting optimization
4. **D8 flow routing requires urban modifications** - Standard flow accumulation has significant limitations; need to account for streets, curbs, and discrete inlet capture
5. **Equity is an explicit gap** in current GI practice - only 11% of plans define it; opportunity for meaningful contribution

---

## Research Sources

| Document | Focus | Key Contribution |
|----------|-------|------------------|
| `brat_fis_research.md` | BRAT methodology deep-dive | FIS architecture, validation approach, transferability assessment |
| `urban_drainage_network_research.md` | Strahler ordering validity | D8 limitations, alternative approaches, graph theory methods |
| `portland_bes_methods_research.md` | Portland's actual practices | Siting criteria, GIS layers, performance data, lessons learned |
| `gi_siting_literature_research.md` | Established methods survey | MCDA approaches, optimization algorithms, research gaps |

---

## Validated Methodology Components

### 1. Fuzzy Inference System Architecture

**Source:** BRAT FIS Research

BRAT uses a **two-stage cascaded FIS**:
- Stage 1: Physical suitability (vegetation → dam-building capacity)
- Stage 2: Combined capacity (Stage 1 output + hydrology → final rating)

**For Bioswale Siting:**
- Stage 1: Physical suitability (slope + soil + groundwater → infiltration score)
- Stage 2: Capture potential (Stage 1 + impervious area + flow accumulation → priority rating)

**Technical Implementation:**
- **Membership functions:** Trapezoidal (gradual transitions)
- **Inference:** Mamdani-type
- **Defuzzification:** Centroid (center of gravity)
- **Library:** scikit-fuzzy (Python)

### 2. Standard Siting Constraints

**Source:** Portland BES Methods + GI Literature

| Parameter | Requirement | Source |
|-----------|-------------|--------|
| Maximum slope | 3:1 (ideal 4:1) | Portland BES SWMM |
| Longitudinal slope | 1-6% | Portland BES |
| Groundwater clearance | 5 ft minimum | Portland BES, EPA |
| Maximum clay content | 5% | Portland BES |
| Infiltration rate | 1.0-6.0 in/hr | Minnesota Stormwater Manual |
| Rain garden depth (clay) | 6 inches max | Portland BES |

### 3. Hydrologic Soil Groups

**Source:** GI Literature + USDA/NRCS

| Group | Infiltration Rate | Runoff Potential | Suitability |
|-------|------------------|------------------|-------------|
| A | >0.30 in/hr | Low | Excellent |
| B | 0.15-0.30 in/hr | Moderate | Good |
| C | 0.05-0.15 in/hr | Moderate-High | Marginal |
| D | <0.05 in/hr | High | Poor (needs engineering) |

### 4. Validation Approach

**Source:** BRAT FIS Research + Portland BES

BRAT validated against 8,060 documented beaver dam locations in Utah, achieving 89.97% accuracy.

**For Basalt Broth:**
- Portland has 3,000+ GSI facilities (bioswales, rain gardens, green streets)
- 2025 MDPI paper: "The First Thirty Years of Green Stormwater Infrastructure in Portland"
- Performance data available: 80-85% peak flow reduction, 94% TSS removal

---

## Critical Methodological Adjustments

### 1. D8 Flow Routing Limitations in Urban Areas

**Source:** Urban Drainage Network Research

**Problem:** Standard D8 flow accumulation assumes water follows topography. In urban areas:
- Pipes can move water across ridges (independent of surface slope)
- Curbs/gutters redirect flow before natural low points
- Discrete inlet points create discontinuities
- Flat graded areas cause D8 algorithm failure

**Solution - Hybrid Approach:**
1. Use **modified D8** with streets as preferential flow paths
2. Calculate **Topographic Wetness Index (TWI)** for accumulation hotspots: `TWI = ln(a / tan(b))`
3. Model **discrete inlet capture** rather than continuous flow assumption
4. Integrate pipe network data where available

### 2. Strahler Ordering Scope

**Source:** Urban Drainage Network Research

**Finding:** Strahler ordering HAS been successfully applied to urban sewer networks, but for **network simplification**, not siting decisions.

**Application:**
- Use Strahler ordering to simplify network for computational efficiency
- Use **graph theory centrality metrics** (edge betweenness) for identifying critical intervention locations
- Do NOT rely on Strahler order as a siting criterion

### 3. Streets as Flow Conduits

**Source:** Urban Drainage Network Research

The "streets as streams" analogy is **partially valid**:

| Valid | Not Valid |
|-------|-----------|
| Curbs function like stream banks | Pipes cross topographic boundaries |
| Intersections are confluences | Flow accumulation is discontinuous |
| Contributing drainage areas exist | Self-similarity/fractality doesn't hold |
| Hierarchical structure exists | Watershed boundaries are infrastructure-defined |

**Recommendation:** Use street network for segment-based analysis, but respect discrete inlet capture and pipe routing where data exists.

---

## Novel Contribution Confirmed

**Source:** GI Siting Literature

### What Exists

| Approach | Examples | Limitation |
|----------|----------|------------|
| Static GIS overlay | EPA BST, AHP/MCDA | No dynamic simulation |
| Optimization + SWMM | GIP-SWMM, OSTRICH-SWMM, Rhodium-SWMM | Heavyweight, requires expertise |
| ABM for adoption | G-SSA (2021) | Models social dynamics, not physical siting |
| ABM for maintenance | Detention basin ABM (2023), NJIT (2024) | Post-installation focus |

### What's Missing

**No published ABM combines:**
- Dynamic water flow simulation
- Real GIS data layers
- Physical bioswale siting optimization
- Accessible platform (NetLogo vs. SWMM)

**Basalt Broth fills this gap.**

---

## Equity Considerations

**Source:** GI Literature + Portland BES

### Current State
- Only 11% of GI plans define equity
- Only 14% define justice
- 80% focus on hazard management
- <10% address causes of uneven distributions

### Portland's Approach
- East Portland explicitly prioritized (heat/pollution disparities)
- Portland Clean Energy Fund: $44-61M annually, 50%+ to underserved communities

### Recommendation
Include equity metrics as explicit optimization objective:
- Environmental justice indicators by census tract
- Historical infrastructure investment patterns
- Heat island vulnerability
- Access to existing green space

---

## Implementation Path

### Phase 1: Data Pipeline (Python/GDAL)

1. **Street network segmentation** at intersections
2. **Hybrid flow routing**: Modified D8 + TWI + inlet locations
3. **Attribute extraction**: Soil, slope, groundwater, impervious surface
4. **FIS implementation** in scikit-fuzzy

### Phase 2: NetLogo ABM

1. **Load segment ratings** from pipeline
2. **Water agents** spawn from rainfall, flow via modified routing
3. **Bioswale agents** intercept water at candidate locations
4. **Optimization agents** explore placement configurations

### Phase 3: Validation

1. Compare model ratings against Portland's 3,000+ existing facilities
2. Calculate agreement metrics (like BRAT's 89.97% target)
3. Sensitivity analysis on FIS parameters

---

## Key References by Topic

### BRAT/FIS Methodology
- Macfarlane et al. (2017) - [Modeling the capacity of riverscapes to support beaver dams](https://www.sciencedirect.com/science/article/abs/pii/S0169555X15302166)
- [BRAT Documentation](https://brat.riverscapes.net/)
- [scikit-fuzzy Library](https://scikit-fuzzy.readthedocs.io/)

### Urban Drainage Networks
- [MDPI Water (2025) - Strahler ordering for sewer networks](https://www.mdpi.com/2073-4441/17/7/990)
- [Water Resources Research (2022) - Complex network theory for drainage](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2022WR032277)

### Portland BES
- [Portland Stormwater Management Manual](https://www.portland.gov/bes/stormwater/2025-stormwater-management-manual)
- [MDPI Sustainability (2025) - 30 Years of Portland GSI](https://www.mdpi.com/2071-1050/17/15/7159)

### GI Siting Methods
- [EPA BMPs Siting Tool](https://www.epa.gov/water-research/best-management-practices-bmps-siting-tool)
- [NACTO Bioswales Design Guide](https://nacto.org/publication/urban-street-design-guide/street-design-elements/stormwater-management/bioswales/)
- [Rhodium-SWMM (GitHub)](https://github.com/NastaranT/rhodium-swmm)

### Environmental Justice
- [Taylor & Francis (2021) - EJ Implications of GI Siting](https://www.tandfonline.com/doi/full/10.1080/1523908X.2021.1945916)

---

## Summary: What Changed from Original Plan

| Original Assumption | Research Finding | Adjustment |
|---------------------|------------------|------------|
| D8 flow accumulation is sufficient | D8 has significant urban limitations | Use hybrid: modified D8 + TWI + inlet capture |
| Strahler ordering for siting | Strahler is for network simplification | Use for efficiency, not siting criteria |
| Streets fully analogous to streams | Partial analogy only | Respect discrete inlets and pipe routing |
| FIS approach is novel | FIS is established (BRAT) | Adapt proven architecture, not invent |
| Validation against existing facilities | BRAT achieved 89.97% accuracy | Target similar accuracy benchmark |
| Equity as nice-to-have | Major gap in literature | Make explicit optimization objective |

---

*Research synthesis completed: 2026-02-04*
*Project: Basalt Broth - Bioswale Placement Optimization for Portland, OR*
