# Green Infrastructure Siting Methods: Literature Review

## Executive Summary

This literature review surveys established and emerging methods for siting green infrastructure (GI), with a focus on bioswales and stormwater management. The review covers GIS-based suitability analysis, multi-criteria decision analysis (MCDA), optimization algorithms, agent-based modeling, and fuzzy logic approaches. Key findings indicate that while GIS-MCDA is the dominant paradigm, there are significant opportunities for novel contributions in dynamic simulation-based siting.

---

## 1. Established Siting Methods

### 1.1 EPA Best Management Practices (BMPs) Siting Tool

The EPA's [Best Management Practices (BMPs) Siting Tool](https://www.epa.gov/water-research/best-management-practices-bmps-siting-tool) identifies potential suitable locations for implementing different types of BMPs or low impact development (LID) controls.

**BMP Categories:**
- **Point BMPs:** Capture upstream drainage at specific locations using detention, infiltration, evaporation, settling, and transformation
- **Linear BMPs:** Narrow linear shapes adjacent to stream channels providing filtration, nutrient uptake, and stream shading
- **Area BMPs:** Land-based management practices affecting impervious area and land cover

**Technical Requirements:**
- Runs on ArcGIS platform
- Requires knowledge of stormwater management and BMPs
- Generates spatial maps indicating BMP types and placement locations based on feasibility criteria

### 1.2 EPA SUSTAIN (System Urban Stormwater Treatment and Analysis Integration)

[SUSTAIN](https://www.epa.gov/water-research/system-urban-stormwater-treatment-and-analysis-integration-sustain) was EPA's more comprehensive tool for regional GSI suitability analysis.

**Methodology:**
- GIS-based overlay analysis
- Layers geo-based information (slope, distance to streams, soil composition)
- Analyzes spatial coincidence to determine suitability for different GI types
- Provides source code and ArcGIS toolbox

**Status:** No longer actively maintained by EPA as of 2016.

### 1.3 GIS Overlay / Weighted Suitability Analysis

The most common approach for LID site selection uses GIS to develop site suitability rankings through weighted overlay analysis.

**Standard Methodology:**
1. Convert criterion data to suitability values
2. Assign weights to each criterion and attributes
3. Combine suitability values and weights
4. Create spatial maps

**Common Input Layers:**
- Slope/topography
- Soil type / hydrologic soil group
- Groundwater depth
- Land use / zoning
- Impervious surface coverage
- Distance to storm drains
- Distance to streams/waterways

---

## 2. Multi-Criteria Decision Analysis (MCDA) Approaches

### 2.1 Analytic Hierarchy Process (AHP)

AHP is the most widely used method for assigning weights in GI siting decisions. Research from [MDPI](https://www.mdpi.com/2071-1050/14/9/5170) and [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0301479719303842) demonstrates extensive application.

**Process:**
1. Identify overall goal
2. Choose evaluation criteria
3. Select stakeholders for weighting
4. Conduct pairwise comparisons between factors
5. Establish weighted values and ranks

**Common Criteria Categories (from AHP studies):**
- **Technical criteria** (highest weight, ~0.37): slope, soil infiltration, drainage capacity
- **Environmental criteria**: water quality improvement, groundwater recharge
- **Economic criteria**: installation costs, annual maintenance
- **Social criteria** (lowest weight, ~0.11): aesthetic benefits, public safety

### 2.2 AHP-TOPSIS Combined Method

[Research from MDPI](https://www.mdpi.com/2073-4441/13/17/2422) demonstrates combining AHP with TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution):
- AHP assigns weights to criteria
- TOPSIS ranks alternatives by geometric distance from ideal/anti-ideal solutions
- Effective for integrating and quantifying stakeholder priorities

### 2.3 MCDA for LID Site Selection

A 2024 comparative analysis in the [Journal of Environmental Management](https://www.sciencedirect.com/science/article/pii/S0301479724001981) identifies three main methods for LID site selection:

1. **Index-based methods** - Simple scoring approaches
2. **GIS-based MCDA** - Weighted overlay with spatial analysis
3. **Multi-criteria models and tools** - Integrated decision support systems

The study evaluates these approaches across ten different criteria to identify strengths and limitations.

---

## 3. Common Input Variables for Suitability Analysis

### 3.1 Physical Site Constraints

**Slope Requirements:**
- Ideal side slopes: 4:1
- Maximum slope: 3:1
- Longitudinal slope: 1-2% (minimum surface channel slope)
- If slope exceeds 4%, use check dams or berms
- Source: [NACTO Urban Street Design Guide](https://nacto.org/publication/urban-street-design-guide/street-design-elements/stormwater-management/bioswales/)

**Soil Infiltration:**
- Filter media minimum: 1.0 in/hr
- Filter media maximum: 6 in/hr
- Engineered soil mixture: 5-10 in/hr
- Maximum clay content: 5%
- Source: [Minnesota Stormwater Manual](https://stormwater.pca.state.mn.us/design_criteria_for_bioretention)

**Groundwater Clearance:**
- Minimum 5-foot clearance from bottom of bioswale to high groundwater table (most sources)
- 3-foot minimum (REQUIRED), 5-foot (RECOMMENDED) separation from seasonally saturated soils or bedrock
- Source: [Caltrans Design Guidance](https://dot.ca.gov/-/media/dot-media/programs/design/documents/2_dg-biofiltration_swale_ada.pdf)

### 3.2 Hydrologic Soil Groups

From [USDA/NRCS standards](https://efotg.sc.egov.usda.gov/references/Delete/2017-11-11/hydrogroups.htm):

| Group | Infiltration Rate | Runoff Potential | Characteristics |
|-------|------------------|------------------|-----------------|
| A | >0.30 in/hr | Low | Deep, well-drained sands/gravels |
| B | 0.15-0.30 in/hr | Moderate | Moderately well-drained, medium texture |
| C | 0.05-0.15 in/hr | Moderate-High | Slow infiltration, fine texture |
| D | <0.05 in/hr | High | Clay soils, high water table, shallow bedrock |

**Dual classes (A/D, B/D, C/D):** Soils that would be in better group if adequately drained.

### 3.3 Land Use and Infrastructure Factors

- Impervious surface percentage
- Proximity to existing storm drains
- Location within floodplain
- Existing utilities (conflicts)
- Pedestrian safety considerations
- Zoning constraints
- Right-of-way availability

---

## 4. Fuzzy Logic in GI Siting

### 4.1 Fuzzy Logic Applications Found

Fuzzy logic has been applied to green infrastructure and stormwater management, though less extensively than crisp MCDA methods.

**Infiltration Trench Siting (2014):**
[PubMed research](https://pubmed.ncbi.nlm.nih.gov/24937491/) applied fuzzy logic for siting infiltration trenches for highway runoff control:
- Combined site suitability maps with groundwater vulnerability maps
- Used fuzzy AND operator for superposition
- Balanced qualification criteria for low contamination risk with optimal BMP site selection

**Fuzzy AHP Integration:**
[ResearchGate studies](https://www.researchgate.net/publication/341752891_Barriers_to_green_roof_installation_An_integrated_fuzzy-based_MCDM_approach) have used fuzzy AHP integrated with VIKOR for evaluating LID strategies including bioretention cells, green roofs, and permeable pavement.

**Fuzzy Logic Control for Stormwater:**
[ScienceDirect research](https://www.sciencedirect.com/science/article/abs/pii/S0048969720324487) developed SWMM_FLC, a data-driven real-time control tool based on fuzzy logic control (FLC) and genetic algorithms for flooding mitigation.

### 4.2 Fuzzy vs. Crisp Threshold Approaches

**Crisp Threshold Limitations:**
- Hard boundaries (e.g., "slope must be <15%") create artificial discontinuities
- Real-world suitability is gradual, not binary
- Small measurement errors can flip classifications

**Fuzzy Logic Advantages:**
- Membership functions capture gradual suitability transitions
- Better handles uncertainty in input data
- Can incorporate expert knowledge naturally
- Allows for "somewhat suitable" classifications

**Research Gap:** Limited application of fuzzy inference systems specifically for bioswale siting. Most fuzzy applications focus on real-time control rather than spatial siting decisions.

---

## 5. Optimization Approaches

### 5.1 Genetic Algorithms (GA) and NSGA-II

**NSGA-II (Non-dominated Sorting Genetic Algorithm II):**
The most commonly used algorithm in the green infrastructure field according to [IWA Publishing review](https://iwaponline.com/aqua/article/73/6/1135/102593/A-critical-review-on-optimization-and).

**Key Applications:**
- [GIP-SWMM](https://www.sciencedirect.com/science/article/abs/pii/S0301479720313347): Green Infrastructure Placement Tool coupled with SWMM
- Supports GI placement from city blocks to large watersheds
- Creates optimal grey-green infrastructure layout ratios

**Performance Results:**
- Optimizing size, location, and connection of GI facilities increases runoff reduction by 13.4-24.5%
- Peak flow reduction of 3.3-18%
- Source: [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0022169423015147)

### 5.2 OSTRICH-SWMM

[OSTRICH-SWMM](https://www.sciencedirect.com/science/article/abs/pii/S1364815218307515) is an open-source multi-objective optimization tool connecting SWMM with the Optimization Software Toolkit for Research Involving Computational Heuristics.

**Algorithms Compared:**
- Asynchronous Parallel Dynamically Dimensioned Search
- Simulated Annealing
- Real-Coded Genetic Algorithm

### 5.3 Rhodium-SWMM

[Rhodium-SWMM](https://www.sciencedirect.com/science/article/abs/pii/S1364815223000579) is an open-source Python library for green infrastructure placement under deep uncertainty.

**Key Features:**
- Connects SWMM to Rhodium (Many-Objective Robust Decision Making)
- Addresses deep uncertainties in GI planning
- Provides generalizable, flexible interface for any SWMM input file
- Can define SWMM parameters as uncertainties or decision levers
- Source code available on [GitHub](https://github.com/NastaranT/rhodium-swmm)

### 5.4 Simulated Annealing

[Meta-heuristic review](https://iwaponline.com/aqua/article/73/6/1135/102593/A-critical-review-on-optimization-and) identifies simulated annealing as one of the most suitable techniques for multi-objective GI optimization.

**Applications:**
- Optimal location and sizing of stormwater tanks
- Coupled with dynamic rainfall-runoff simulators
- Effective for escaping local optima in complex search spaces

### 5.5 Common Optimization Framework

**Objective Functions:**
- Minimize construction/maintenance costs
- Maximize runoff volume reduction
- Maximize pollutant removal
- Minimize flood risk

**Decision Variables:**
- Types of green infrastructure
- Sizes of installations
- Locations/placement
- Storage volumes (detention tanks)

**Constraints:**
- Budget limits
- Space availability
- Physical site constraints
- Regulatory requirements

---

## 6. Agent-Based Models (ABM) for Green Infrastructure

### 6.1 Existing ABM Applications

**G-SSA (Green Stormwater Infrastructure Social Spatial Adoption) Model:**
[Research from PubMed](https://pubmed.ncbi.nlm.nih.gov/34346118/) describes a cellular automata agent-based model that simulates private property owner behavior responding to GSI incentives.

**Model Features:**
- Small-world social networks
- Opinion dissemination
- Diffusion of innovation concepts
- Simulates years of GSI program implementation

**Inputs:**
- Demographic information
- Site constraints
- GSI practice types and costs
- Financial incentive structures

**Key Finding:** ABM for GI focuses on *adoption dynamics*, not physical placement decisions.

### 6.2 Gap: No ABM for Physical Siting

Current ABM work in green infrastructure covers:
- Social adoption dynamics (G-SSA)
- Maintenance optimization for detention basins
- Regulatory interplay modeling
- Permeable pavement maintenance (NJIT 2024)

**What's Missing:** No published ABM combines dynamic water flow simulation with real GIS data for bioswale placement optimization. This is the novel contribution opportunity for the Basalt Broth project.

---

## 7. D8 Flow Direction and Hydrologic Modeling

### 7.1 D8 Algorithm

The [D8 method](https://pro.arcgis.com/en/pro-app/latest/tool-reference/spatial-analyst/how-flow-direction-works.htm) is the standard approach for modeling flow direction from DEMs:

**How It Works:**
- Each cell flows to steepest downslope neighbor (8 possible directions)
- Flow direction coded numerically (1-255)
- Forms basis for flow accumulation and watershed delineation

**Preprocessing Required:**
- DEM must be hydrologically corrected
- Fill depressions (spurious sinks)
- Remove flat areas

### 7.2 Alternative Approaches

- **Rho8:** Stochastic variant with random component
- **D-infinity:** Allows flow to split between cells
- **Multiple Flow Direction (MFD):** Distributes flow proportionally

---

## 8. Environmental Justice and Equity

### 8.1 Current Gaps in Equity-Focused Siting

[Research from Taylor & Francis](https://www.tandfonline.com/doi/full/10.1080/1523908X.2021.1945916) highlights significant shortcomings:
- Only 11% of GI plans define equity
- Only 14% define justice
- 80% focus on hazard management, <10% address causes of uneven distributions

**Key Issues:**
- GI's inequitable distribution can magnify environmental injustices
- Non-inclusion of minoritized communities in planning decisions
- Politics focused on stormwater management over justice

### 8.2 Emerging Solutions

**iPlan-GreenS2:** An [open-source tool](https://ascelibrary.org/doi/10.1061/JOEEDU.EEENG-7586) that integrates geological, environmental, and sociodemographic factors for equitable GSI siting.

**Recommendations:**
- Clear definitions of equity and justice needed
- Engagement with causes of inequality and displacement
- Transform GI planning through focus on inclusion

---

## 9. Climate Change and Uncertainty

### 9.1 Performance Under Climate Uncertainty

[Research from Frontiers](https://www.frontiersin.org/articles/10.3389/fbuil.2018.00071) identifies four major sources of uncertainty:

1. Non-additive effects of individual BMPs at catchment scale
2. Spatial configuration of fine-scale land use changes
3. Performance changes due to climate change
4. Noise levels in urban flow monitoring

### 9.2 Scenario-Based Planning

[ScienceDirect research](https://www.sciencedirect.com/science/article/abs/pii/S0305048318314312) on optimizing GI under precipitation uncertainty demonstrates:
- GI effectiveness decreases with increasing rainfall return periods
- Cost-benefit ratios decrease as return periods increase
- Scenario-based approaches identify robust solutions across multiple futures

---

## 10. Bioswale Performance Data

### 10.1 Pollutant Removal Efficiency

From [International Journal of Scientific and Research Archives](https://ijsra.net/sites/default/files/IJSRA-2020-0045.pdf):

| Pollutant | Removal Rate |
|-----------|-------------|
| TSS (Total Suspended Solids) | >90% |
| Runoff Volume | 50-80% reduction |
| Heavy Metals | Significant reduction |
| Nutrients | Variable, depends on vegetation |

**TSS Removal by Distance:**
- 50-80% removed within first 10m of swale length
- Performance highly dependent on inlet TSS concentration

### 10.2 Key Design Factors Affecting Performance

From [Minnesota Stormwater Manual](https://stormwater.pca.state.mn.us/index.php/Information_on_pollutant_removal_by_BMPs):

- **Vegetation:** Native, deep-rooted species outperform turfgrass
- **Media composition:** Sand/compost/loam blend for infiltration and adsorption
- **Geometry:** Maximize water residence time
- **Maintenance:** Media clogging reduces long-term performance

---

## 11. Research Gaps and Opportunities

### 11.1 Identified Gaps in Literature

**From systematic reviews:**
1. **Geographic bias:** Limited studies in Asia, South America, warmer climates
2. **Economic valuation:** Rare and inconsistent practices
3. **Social equity:** Inadequate consideration in siting decisions
4. **Post-implementation monitoring:** Lack of empirical outcome measurement
5. **Under-researched GI types:** Green roofs, wetlands, sports areas

### 11.2 Methodological Gaps

1. **Static vs. Dynamic Analysis:** Most siting tools use static GIS overlay; no dynamic runoff simulation for siting
2. **Optimization-Simulation Integration:** Few tools truly integrate hydrologic simulation with optimization
3. **Accessibility:** SWMM-based tools require significant expertise; no NetLogo-based approaches
4. **Agent-Based Physical Siting:** No ABM combines dynamic water flow with GI placement optimization

### 11.3 Novel Contribution Opportunity

The Basalt Broth project addresses multiple gaps:

| Gap | Project Approach |
|-----|-----------------|
| Static analysis | Dynamic water agent simulation |
| No ABM for physical siting | Water parcels + optimization agents |
| Heavyweight tools (SWMM, SUSTAIN) | NetLogo accessibility |
| Limited validation | Portland's 3,000+ existing facilities |
| Equity gaps | Multi-objective with EJ criteria |

---

## 12. Key References by Category

### EPA Tools and Guidance
- [EPA BMPs Siting Tool](https://www.epa.gov/water-research/best-management-practices-bmps-siting-tool)
- [EPA SUSTAIN](https://www.epa.gov/water-research/system-urban-stormwater-treatment-and-analysis-integration-sustain)
- [EPA Green Infrastructure Design Strategies](https://www.epa.gov/green-infrastructure/green-infrastructure-design-strategies)

### MCDA and AHP
- [Green Infrastructure Planning Principles: AHP (MDPI)](https://www.mdpi.com/2071-1050/14/9/5170)
- [AHP-TOPSIS for Stormwater Adaptation (MDPI)](https://www.mdpi.com/2073-4441/13/17/2422)
- [LID Site Selection Comparative Analysis (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S0301479724001981)

### Optimization Tools
- [GIP-SWMM (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S0301479720313347)
- [OSTRICH-SWMM (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S1364815218307515)
- [Rhodium-SWMM (GitHub)](https://github.com/NastaranT/rhodium-swmm)

### Agent-Based Models
- [G-SSA Model (PubMed)](https://pubmed.ncbi.nlm.nih.gov/34346118/)
- [Critical Review on GI Optimization (IWA Publishing)](https://iwaponline.com/aqua/article/73/6/1135/102593/A-critical-review-on-optimization-and)

### Design Standards
- [Bioswales - NACTO](https://nacto.org/publication/urban-street-design-guide/street-design-elements/stormwater-management/bioswales/)
- [Minnesota Stormwater Manual - Bioretention Design](https://stormwater.pca.state.mn.us/design_criteria_for_bioretention)
- [Caltrans Biofiltration Swale Design](https://dot.ca.gov/-/media/dot-media/programs/design/documents/2_dg-biofiltration_swale_ada.pdf)

### Environmental Justice
- [EJ Implications of GI Siting (Taylor & Francis)](https://www.tandfonline.com/doi/full/10.1080/1523908X.2021.1945916)
- [Georgetown Climate Center GI Toolkit - Equity](https://www.georgetownclimate.org/adaptation/toolkits/green-infrastructure-toolkit/equity-and-environmental-justice.html)

### Research Reviews
- [GI Systematic Literature Review (Taylor & Francis)](https://www.tandfonline.com/doi/full/10.1080/1331677X.2021.1893202)
- [GI Planning Principles Review (MDPI Land)](https://www.mdpi.com/2076-3417/15/15/8516)

---

## 13. Conclusions

### Summary of Siting Method Landscape

1. **Dominant Paradigm:** GIS-based weighted overlay with AHP/MCDA for criteria weighting
2. **Optimization Trend:** NSGA-II + SWMM coupling increasingly common
3. **ABM Gap:** No dynamic simulation-based ABM for physical GI siting exists
4. **Fuzzy Logic:** Underutilized for siting; mainly applied to real-time control
5. **Equity:** Major gap in current practice despite recognized importance

### Implications for Basalt Broth Project

The literature review confirms that the proposed ABM approach in NetLogo represents a genuine novel contribution:
- No existing model combines dynamic water flow simulation with optimization for bioswale placement
- NetLogo offers accessibility advantages over SWMM-based tools
- Portland's existing GI network provides unique validation opportunity
- Multi-objective optimization with equity criteria addresses documented gaps

### Recommended Project Approach

Based on this review, the Basalt Broth model should:
1. Use **D8 flow direction** for water agent routing (standard, validated approach)
2. Incorporate **standard siting constraints** (slope <3:1, infiltration >1 in/hr, groundwater >5 ft)
3. Apply **hydrologic soil group** classifications for infiltration parameters
4. Include **equity metrics** as optimization objective (novel contribution)
5. Consider **fuzzy membership functions** for suitability (gradual transitions vs. hard thresholds)
6. Validate against **Portland's existing facilities** (unique opportunity)

---

*Literature review completed: February 4, 2026*
*Project: Basalt Broth - Bioswale Placement Optimization for Portland, OR*
