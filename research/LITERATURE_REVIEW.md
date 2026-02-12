# Literature Review: Agent-Based Modeling for Bioswale Placement Optimization Using GIS and Fuzzy Inference

## Abstract

Urban stormwater management has become a critical challenge as cities contend with aging combined sewer systems, increasing impervious surface coverage, and climate-driven intensification of precipitation events. Green stormwater infrastructure (GSI)—bioswales, rain gardens, permeable pavement, and related practices—offers a decentralized alternative to conventional grey infrastructure by managing runoff at its source through infiltration, evapotranspiration, and filtration. However, deciding *where* to place GSI facilities remains a largely static exercise dominated by GIS overlay analysis and expert judgment. This review surveys the current landscape of GSI siting methodologies, identifies significant gaps in dynamic simulation and equitable planning, and argues that agent-based modeling (ABM) combined with fuzzy inference systems (FIS) represents a promising and unexplored approach to bioswale placement optimization.

---

## 1. Introduction

The problem of urban stormwater is fundamentally spatial. Rainfall strikes impervious surfaces—rooftops, roads, parking lots—and becomes runoff that must go somewhere. In cities with combined sewer systems, that runoff mixes with sanitary sewage and, during heavy storms, overwhelms treatment capacity. The result is combined sewer overflows (CSOs): discharges of untreated sewage directly into rivers and streams. Portland, Oregon reduced its CSO volume by 94% on the Willamette River through its $1.4 billion Big Pipe Project, completed in 2011, but the city simultaneously recognized that grey infrastructure alone was insufficient (City of Portland BES, 2025). Over the past three decades, Portland has deployed more than 3,000 green stormwater infrastructure facilities—primarily bioswales and green street planters—that collectively capture approximately 2.3 billion gallons of stormwater annually.

The question of *optimal placement* is deceptively complex. A bioswale's effectiveness depends on the interaction of multiple physical factors—slope, soil infiltration capacity, groundwater depth, upstream impervious area, contributing drainage area—alongside social and economic considerations including construction cost, maintenance access, parking impacts, equity across neighborhoods, and proximity to sensitive waterways. Current siting methods range from simple threshold-based screening to sophisticated optimization algorithms coupled with hydrodynamic models, yet a significant methodological gap persists: no existing tool combines dynamic water flow simulation with spatial optimization in an accessible, transparent framework.

This review examines five intersecting bodies of literature: (1) established GIS-based siting methods; (2) multi-criteria decision analysis frameworks; (3) fuzzy inference systems for environmental siting, particularly the Beaver Restoration Assessment Tool (BRAT); (4) urban drainage network analysis and its departure from natural watershed hydrology; and (5) agent-based modeling applications in green infrastructure. The review concludes by identifying the specific gap that a NetLogo-based ABM with fuzzy suitability scoring would address.

---

## 2. GIS-Based Siting Methods

### 2.1 Weighted Overlay and Threshold Screening

The dominant paradigm for GSI siting is GIS-based weighted overlay analysis, in which multiple spatial data layers—slope, soil type, land use, groundwater depth, impervious surface coverage—are reclassified into suitability scores, weighted by relative importance, and combined into a composite suitability map (MDPI Land, 2018). The approach is intuitive, reproducible, and widely supported by commercial GIS platforms.

The U.S. Environmental Protection Agency has developed two tools embodying this paradigm. The **Best Management Practices (BMPs) Siting Tool** identifies potential locations for point, linear, and area-based BMPs using spatial feasibility criteria evaluated on the ArcGIS platform (EPA, 2022). The now-discontinued **SUSTAIN** (System for Urban Stormwater Treatment and Analysis Integration) provided a more comprehensive overlay analysis that layered slope, distance to streams, and soil composition to determine suitability for different GI types (EPA, 2016). Both tools represent the static overlay approach: they evaluate site conditions at a single point in time without simulating how water actually moves through the urban landscape.

Standard physical screening criteria have converged across jurisdictions and design manuals. Bioswales require maximum side slopes of 3:1 (ideally 4:1), longitudinal slopes of 1–6%, a minimum 5-foot clearance between the facility bottom and seasonal high groundwater, maximum soil clay content of 5%, and infiltration rates between 1.0 and 6.0 inches per hour in the filter media (NACTO, 2013; Minnesota Stormwater Manual, 2023; Caltrans, 2018). These thresholds are well-established but impose hard boundaries—a site at 6.1% slope is classified identically to one at 15%, and a site at 5.9% is treated as equivalent to one at 1%. This crisp boundary problem motivates the application of fuzzy logic, discussed in Section 4.

### 2.2 EPA Tools and Their Limitations

While EPA's BMPs Siting Tool and SUSTAIN advanced the practice of systematic GI evaluation, both share fundamental limitations. They operate on static spatial data, treating the landscape as a fixed snapshot rather than a dynamic system. They do not simulate rainfall events, track water movement across the surface, or model how bioswales at different locations interact with one another. A bioswale placed upstream reduces the runoff reaching a downstream candidate site, but static overlay tools evaluate each site independently. This inability to capture spatial interaction effects limits their utility for optimizing configurations of multiple facilities.

Furthermore, these tools require ArcGIS expertise and infrastructure, limiting their accessibility to planning teams without dedicated GIS staff. SUSTAIN was discontinued in 2016, leaving no actively maintained EPA tool for comprehensive GSI siting analysis.

---

## 3. Multi-Criteria Decision Analysis

### 3.1 Analytic Hierarchy Process (AHP)

The Analytic Hierarchy Process is the most widely applied framework for assigning weights to siting criteria in GI planning (Saaty, 1980). AHP structures the decision problem hierarchically—overall goal, evaluation criteria, alternatives—and uses pairwise comparisons between criteria to derive relative weights. Studies applying AHP to GI siting typically identify four categories of criteria: technical factors (slope, soil infiltration, drainage capacity, typically receiving the highest weight at approximately 0.37), environmental factors (water quality improvement, groundwater recharge), economic factors (installation and maintenance costs), and social factors (aesthetic benefits, public safety, typically receiving the lowest weight at approximately 0.11) (MDPI Sustainability, 2022).

AHP's strength lies in making the weighting process explicit and structured. Its weakness is that pairwise comparisons are inherently subjective, and the resulting linear weighted sum assumes independence among criteria—an assumption violated when, for example, steep slopes and poor soils compound each other's negative effects on suitability in a non-linear fashion.

### 3.2 Combined MCDA Approaches

Researchers have extended AHP by combining it with other MCDA methods. The AHP-TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) approach uses AHP-derived weights within a framework that ranks alternatives by their geometric distance from ideal and anti-ideal solutions, offering a more nuanced ranking than simple weighted sums (MDPI Water, 2021). A 2024 comparative analysis in the *Journal of Environmental Management* evaluated three broad categories of LID site selection methods—index-based approaches, GIS-based MCDA, and integrated decision support tools—across ten evaluation criteria, finding that no single method dominates across all dimensions (ScienceDirect, 2024).

The common thread across MCDA approaches is their static nature. They score candidate sites based on existing conditions without simulating how those conditions respond to intervention. They answer "where *could* a bioswale go?" but not "where *should* it go to maximize system-level benefit?"

---

## 4. Fuzzy Inference Systems for Environmental Siting

### 4.1 The BRAT Precedent

The strongest precedent for applying fuzzy inference to environmental siting decisions comes not from urban stormwater management but from riparian ecology. The **Beaver Restoration Assessment Tool (BRAT)**, developed by Macfarlane, Wheaton, and colleagues at Utah State University, uses a two-stage cascaded fuzzy inference system to model the capacity of stream reaches to support beaver dam construction (Macfarlane et al., 2017). BRAT's first stage evaluates vegetation suitability using riparian and upland vegetation types; its second stage integrates the vegetation score with baseflow stream power, flood recurrence interval discharge, and stream gradient to produce a final dam density estimate.

BRAT's FIS implementation uses trapezoidal membership functions for continuous variables, Mamdani-type inference (which preserves the interpretability of linguistic rules), and centroid defuzzification to produce continuous output values. The model was validated against 8,060 documented beaver dam locations across Utah, achieving 89.97% accuracy in segregating factors controlling dam occurrence and density (Macfarlane et al., 2017). This validation approach—comparing model predictions against a large inventory of existing facilities—transfers directly to the urban GSI context, where cities like Portland maintain inventories of thousands of installed facilities.

### 4.2 Why FIS Suits Bioswale Siting

Fuzzy inference systems offer specific advantages over both crisp threshold screening and weighted linear combination for bioswale siting:

**Non-linear rule interactions.** Fuzzy rules can express conditional logic that weighted overlay cannot. The rule "IF slope IS steep THEN suitability IS unsuitable" can override favorable soil and groundwater conditions, capturing the engineering reality that some constraints are absolute while others are compensatory.

**Graceful boundary handling.** Trapezoidal membership functions allow gradual transitions between suitability categories. A site at 5.9% slope and one at 6.1% receive nearly identical suitability scores rather than falling on opposite sides of a hard threshold.

**Expert knowledge encoding.** Engineering design criteria from sources like the Portland BES Stormwater Management Manual (2025) and the NACTO Urban Street Design Guide (2013) express siting knowledge in linguistic terms ("slopes should not exceed 3:1," "clay content should be less than 5%") that map naturally onto fuzzy rules.

**Uncertainty propagation.** Output confidence reflects input uncertainty—sites with ambiguous soil classifications or interpolated groundwater depths produce appropriately hedged suitability scores.

### 4.3 Fuzzy Logic in Stormwater Management

Prior applications of fuzzy logic in stormwater management have focused primarily on real-time operational control rather than spatial siting. Researchers developed SWMM_FLC, a fuzzy logic controller integrated with SWMM for real-time flooding mitigation during storm events (ScienceDirect, 2020). Fuzzy AHP has been combined with VIKOR for evaluating LID strategies including bioretention cells, green roofs, and permeable pavement (ResearchGate, 2020). Fuzzy logic has also been applied to siting infiltration trenches for highway runoff control, using fuzzy AND operators to balance qualification criteria with groundwater vulnerability (PubMed, 2014). A 2025 study in *MDPI Cities* applied a fuzzy AI-based framework for identifying priority areas for urban green infrastructure planning.

However, the specific application of a cascaded fuzzy inference system—where physical suitability feeds into a second-stage capture potential assessment—has not been applied to bioswale or green street siting. The BRAT architecture demonstrates that this approach works for environmental facility siting; its adaptation to the urban stormwater context represents a methodological contribution.

### 4.4 Proposed Two-Stage FIS Architecture

Drawing on BRAT's validated architecture, a bioswale siting FIS would operate in two stages:

**Stage 1 (Physical Suitability):** Three inputs—terrain slope derived from a LiDAR DEM, soil saturated hydraulic conductivity (Ksat) from USDA SSURGO surveys, and depth to seasonal high groundwater—produce a continuous suitability score. Trapezoidal membership functions classify each input into linguistic categories (e.g., slope: flat, moderate, steep, unsuitable) and a rule base encodes Portland BES design constraints.

**Stage 2 (Capture Potential):** The Stage 1 suitability score is combined with upstream impervious surface percentage and a topographic wetness index (TWI) to produce a final priority rating. This second stage captures the demand side of the equation: even a physically ideal site is low-priority if it has little upstream runoff to capture.

Output categories—unsuitable, marginal, moderate, good, optimal—provide actionable classifications for planners while preserving the continuous underlying scores for optimization.

---

## 5. Urban Drainage Network Analysis

### 5.1 The D8 Algorithm and Its Urban Limitations

The D8 (deterministic eight-neighbor) flow direction algorithm is the standard method for modeling surface water routing from digital elevation models (Jenson & Domingue, 1988). Each raster cell drains to its steepest downslope neighbor among eight possible directions, producing a flow direction grid that accumulates upstream contributing area. D8 is computationally efficient, well-understood, and widely implemented in GIS software.

However, D8 assumes that water follows surface topography—an assumption that breaks down in urban environments in several important ways. First, subsurface pipes routinely move water across topographic ridges, independent of surface slope. Second, curbs and gutters redirect flow along engineered paths that may diverge from the steepest gradient. Third, storm drain inlets create discrete capture points where surface flow is removed from the overland system, producing discontinuities in the accumulation pattern. Fourth, flat graded areas—common in developed parcels and parking lots—cause the D8 algorithm to produce arbitrary or erroneous flow directions (Springer, 2024). Studies have shown that urban infrastructure can alter effective drainage areas by 17% or more compared to topographically derived boundaries (Springer, 2024).

### 5.2 Strahler Ordering in Urban Contexts

Strahler stream ordering, developed for natural dendritic river networks, has been adapted for urban sewer systems, primarily for **network simplification** rather than siting analysis. A 2025 study in *MDPI Water* demonstrated that Strahler-based simplification reduced a network of 95,219 pipes and 95,318 nodes to 604 pipes and 606 nodes while maintaining functional accuracy for flood modeling when coupled with SWMM and LISFLOOD-FP. The IWA Publishing literature confirms that the approach "constructs clear topological relations of the drainage network and shows good performance in drainage network simplification" (IWA, 2024).

The transferability of Strahler ordering to siting decisions is limited by fundamental differences between natural and urban drainage networks. Natural watersheds exhibit self-similar branching patterns with consistent bifurcation ratios (Horton's laws); urban drainage networks are designed artifacts that may not exhibit fractal properties. Natural watershed boundaries are topographically defined; urban drainage boundaries are infrastructure-defined and can shift with pipe installations or regrading. These differences mean Strahler ordering is a valid tool for computational efficiency but should not serve as a criterion for bioswale placement.

### 5.3 Graph Theory and Complex Network Analysis

Complex network theory has emerged as a powerful alternative framework for analyzing urban drainage systems. Edge betweenness centrality—a measure of how many shortest flow paths pass through a given pipe—identifies critical bottleneck locations without requiring full hydraulic simulation (Water Resources Research, 2022). Relevance-based centrality combines intrinsic pipe properties (length, flow capacity) with topological position to produce composite importance scores (River Journal, 2023). These graph-theoretic metrics can identify high-priority intervention locations where bioswales would intercept the greatest volume of runoff before it enters the piped system.

Urban drainage networks differ structurally from natural stream networks in a key respect: they are typically tree-like graphs where the number of edges equals the number of nodes minus one, whereas natural networks often contain loops and redundant pathways (Applied Network Science, 2019).

### 5.4 Hybrid Flow Routing Approaches

Given D8's limitations in urban settings, researchers have developed hybrid approaches that integrate surface topography with infrastructure data. DEM-pipe integration "burns" pipe inverts into the elevation model, forcing the flow routing algorithm to respect subsurface connectivity (HESS, 2022). Dual drainage modeling couples 1D pipe network simulation with 2D overland flow across the surface, allowing bidirectional exchange at inlet locations (ASCE, 2009; IWA Publishing, 2024). Graph neural networks have also been applied to estimate below-ground network topology from street networks and surface topography in cities lacking complete sewer data (ScienceDirect, 2024). SWMManywhere (Dobson et al., 2025), an actively developed open-source tool from Imperial College London, takes this further by deriving and simulating complete sewer networks from publicly available geospatial data given only a bounding box—a philosophy similar to the present project's reliance on Portland's open data infrastructure.

For bioswale siting specifically, the Topographic Wetness Index (TWI = ln(a / tan β), where *a* is upslope contributing area and *β* is local slope) offers a computationally efficient proxy for identifying high water accumulation potential without full hydrodynamic modeling. TWI has been validated for urban flood-prone area identification in Illinois (ISWS, 2017) and calibrated with SAR data for sustainable drainage systems (SuDS) placement in the UK (MDPI Sustainability, 2024). A practical approach for bioswale siting combines modified D8 routing—treating streets as preferential flow paths—with TWI for identifying accumulation hotspots and discrete inlet capture modeling to respect the engineered drainage system.

---

## 6. Agent-Based Modeling for Green Infrastructure

### 6.1 Existing ABM Applications

Agent-based modeling in green infrastructure research has focused on social and institutional dynamics rather than physical siting. The **Green Stormwater Infrastructure Social Spatial Adoption (G-SSA)** model simulates private property owner behavior in response to GSI incentive programs using cellular automata with small-world social networks, opinion dissemination, and diffusion of innovation concepts (PubMed, 2021). G-SSA takes demographic information, site constraints, GSI practice types and costs, and financial incentive structures as inputs, and simulates years of program implementation to predict adoption patterns. Its contribution is in understanding *who* will adopt GSI and *under what incentive structures*—not *where* facilities should be placed for maximum hydrologic benefit.

Other ABM applications include detention basin maintenance optimization (2023), which models maintenance scheduling and degradation dynamics; NJIT's dynamic GI optimization (2024), focused on permeable pavement maintenance cycles; and an ASCE study (2024) modeling regulatory interplay between agencies responsible for different aspects of green infrastructure. All focus on post-installation dynamics rather than placement decisions.

### 6.2 The Simulation-Siting Gap

A critical review of optimization and meta-heuristic techniques for green infrastructure (IWA Publishing, 2024) confirms that the most common approach couples NSGA-II (Non-dominated Sorting Genetic Algorithm II) with SWMM for multi-objective optimization. Tools like GIP-SWMM (ScienceDirect, 2020) support GI placement from city blocks to large watersheds; OSTRICH-SWMM (ScienceDirect, 2018) connects SWMM with multiple optimization algorithms including simulated annealing and genetic algorithms; and Rhodium-SWMM (Taraghi et al., 2023) addresses GI placement under deep uncertainty using Many-Objective Robust Decision Making. These tools are powerful but heavyweight—they require SWMM expertise, substantial calibration data, and significant computational resources.

Critically, none of these tools have achieved meaningful adoption. A survey of their open-source repositories (conducted February 2026) reveals a consistent pattern: each was published alongside a journal article, pushed to GitHub, and never substantively maintained. Rhodium-SWMM has a single contributor and 7 total commits, with no activity since June 2023. EPA's Greenopt has not been updated since July 2020. SWMMLIDopt has one star and zero forks. OSTRICH-SWMM shows the most community interest (39 stars, 20 forks) but receives only sporadic updates. By contrast, the general-purpose simulation platforms these tools build on—PySWMM (350 stars, active development by consulting firm HydroDigital and EPA contributors) and EPA SWMM itself (319 stars)—have genuine user bases. The pattern suggests that the bottleneck is not simulation capability but accessible, maintainable tooling for the siting decision itself. A detailed inventory of open-source tools and their adoption status is provided in a companion document (see `open_source_tools.md`).

No published model uses agent-based simulation—where autonomous agents represent water parcels flowing across real terrain—as the evaluation engine for bioswale placement optimization. This gap exists despite ABM's natural suitability for the problem: water parcels that spawn from rainfall, flow downhill following terrain and infrastructure, accumulate pollutant loads from impervious surfaces, and are intercepted by bioswale agents that capture and infiltrate them. The agent-based framing makes the causal mechanism explicit and visible in a way that lumped-parameter models (like SWMM subcatchment routing) do not.

### 6.3 NetLogo as a Platform

NetLogo (Wilensky, 1999) offers specific advantages for this application. Its GIS extension supports loading raster and vector spatial data layers. BehaviorSpace provides built-in parameter sweep capabilities for systematic optimization. The visual interface makes model behavior transparent and communicable to non-technical stakeholders, including planners and community members. And the platform has a large user community and extensive documentation, reducing barriers to adoption and reproducibility.

The tradeoff is computational performance: NetLogo is slower than compiled languages for large-scale simulation. However, for the screening and relative ranking task of bioswale siting—rather than precise hydrodynamic prediction—the performance penalty is acceptable, particularly for neighborhood-scale study areas.

---

## 7. Optimization Approaches

### 7.1 Multi-Objective Optimization

GSI placement is inherently multi-objective. Decision-makers must balance runoff volume reduction, pollutant removal effectiveness, construction and maintenance costs, flood risk reduction, and equitable distribution across neighborhoods. NSGA-II has become the standard algorithm for multi-objective GSI optimization, capable of generating Pareto-optimal solution sets that expose tradeoffs between competing objectives (IWA Publishing, 2024).

Studies using NSGA-II coupled with SWMM report that optimizing the size, location, and connection of GI facilities increases runoff reduction by 13.4–24.5% and peak flow reduction by 3.3–18% compared to non-optimized configurations (ScienceDirect, 2023). These results demonstrate substantial value in systematic placement optimization over ad hoc or rule-of-thumb siting.

### 7.2 Simulated Annealing and Parameter Sweeps

Alternative optimization approaches include simulated annealing, which is effective for escaping local optima in complex search spaces and has been applied to optimal location and sizing of stormwater detention facilities (IWA Publishing, 2024). For smaller search spaces, exhaustive parameter sweeps—systematically evaluating all possible configurations—provide guaranteed global optima at the cost of exponential computational scaling.

NetLogo's BehaviorSpace tool supports parameter sweeps natively, making it a natural starting point for optimization. If the search space proves too large for exhaustive evaluation, genetic algorithms can be integrated through NetLogo extensions or external coupling.

---

## 8. Portland as a Validation Laboratory

### 8.1 Thirty Years of Green Stormwater Infrastructure

Portland's Bureau of Environmental Services (BES) has been deploying green stormwater infrastructure since 2003, when the first Green Streets pilot demonstration projects were installed. The citywide program, initiated in 2005, has grown to encompass over 3,000 facilities, including approximately 2,500 green street planters that capture roughly 200 million gallons per year and 56,000 downspout disconnections removing 1.2 billion gallons per year from the combined sewer system (City of Portland BES, 2025). A comprehensive retrospective—"The First Thirty Years of Green Stormwater Infrastructure in Portland, Oregon"—was published in MDPI *Sustainability* in 2025, providing an authoritative synthesis of the program's evolution, performance, and lessons learned.

### 8.2 Performance Data

Portland's monitoring program has generated performance data with direct relevance to model validation. A two-year study of seven lined bioretention facilities documented 94% TSS removal, 85% ammonia reduction, 59% total copper reduction, and 80% total zinc reduction—though nitrate increased by 2,070% and orthophosphate by 141%, reflecting the facilities' tendency to leach nutrients from engineered soil media (City of Portland BES, 2025). Modeling of green street designs showed 80–85% peak flow reduction to the combined sewer system. These performance benchmarks provide calibration targets for simulation models.

### 8.3 Siting Criteria and Data Infrastructure

BES has codified siting criteria in the 2025 Stormwater Management Manual, effective March 1, 2025. Key constraints include maximum side slopes of 3:1 (4:1 preferred), longitudinal slopes of 1–6%, minimum 5-foot groundwater clearance, maximum 5% clay content in engineered soil, and maximum 6-inch ponding depth in clay soils. The city's Stormwater System Plan MapServer provides public GIS layers including infiltration classifications, dominant hydrologic soil groups, groundwater depth, and impervious surface data by catchment—a spatial data infrastructure that directly supports model development (PortlandMaps, 2025).

Portland's data infrastructure makes it an exceptionally suitable validation site. The 3,000+ facility inventory serves an analogous role to BRAT's 8,060 beaver dam locations: a large, independently documented dataset of "correct answers" against which a siting model can be evaluated.

### 8.4 Lessons Learned

Portland's three decades of experience also reveal practical challenges that inform model design. Hotter, drier summers are stressing vegetation in green streets, many of which were designed without irrigation systems; sandy soils that promote infiltration also drain quickly, exacerbating heat stress on plants. Maintenance requires horticultural skills that traditional infrastructure staff—experienced in managing buried pipes—may not possess. The city employs three full-time maintenance staff supplemented by contractors and a volunteer Green Street Stewards program. These operational realities suggest that maintenance feasibility should be considered in siting optimization alongside purely hydrologic criteria.

---

## 9. Environmental Justice and Equity

### 9.1 The Equity Gap

A systematic review of environmental justice implications in green infrastructure planning found that only 11% of GI plans define equity and only 14% define justice, despite 80% focusing on hazard management (Taylor & Francis, 2021). Fewer than 10% of plans address the underlying causes of uneven infrastructure distributions. This gap is consequential: green infrastructure's spatial distribution can either ameliorate or magnify environmental injustices, depending on whether facilities are concentrated in already-advantaged neighborhoods or directed toward underserved communities.

### 9.2 Portland's Equity Approach

Portland's Climate Action Plan explicitly acknowledges the need to deploy green infrastructure in underserved communities, particularly East Portland, where disparities in access to green space leave populations more susceptible to heat and pollution impacts. The Portland Clean Energy Fund, established by ballot measure in 2018, distributes $44–61 million annually, with at least 50% required to benefit communities of color and low-income residents. This institutional commitment to equitable deployment provides both a policy context and a testable hypothesis for optimization models: does the inclusion of equity metrics as an explicit optimization objective shift recommended facility locations toward underserved areas?

### 9.3 Emerging Tools

The open-source tool **iPlan-GreenS2** integrates geological, environmental, and sociodemographic factors for equitable GSI siting (ASCE, 2023), representing an emerging class of tools that treat equity not as a post-hoc consideration but as a first-class planning criterion. Multi-objective optimization frameworks are well-suited to incorporating equity metrics alongside hydrologic and economic objectives, allowing planners to visualize tradeoffs between maximum system-wide runoff reduction and equitable spatial distribution.

---

## 10. Climate Uncertainty

Green infrastructure performance is sensitive to precipitation patterns that are shifting under climate change. Research identifies four major sources of uncertainty in GSI assessment: non-additive effects of individual BMPs at catchment scale, spatial configuration sensitivity of fine-scale land use changes, performance degradation under altered climate regimes, and noise levels in urban flow monitoring data (Frontiers in Built Environment, 2018). Studies on optimizing GI under precipitation uncertainty demonstrate that GI effectiveness decreases with increasing rainfall return periods and that cost-benefit ratios decline as design storms intensify (ScienceDirect, 2019).

These findings argue for scenario-based evaluation in siting models: rather than optimizing for a single design storm, candidate configurations should be tested against a range of precipitation scenarios to identify robust placements that perform well across multiple possible futures.

---

## 11. Synthesis: Identifying the Research Gap

The literature reveals a clear methodological gap at the intersection of dynamic simulation and spatial optimization for GSI siting. Table 1 summarizes the landscape of existing approaches and their limitations.

**Table 1. Comparison of GSI siting methodologies**

| Approach | Examples | Dynamic Simulation | Spatial Optimization | Accessibility | Equity | Adoption |
|----------|----------|-------------------|---------------------|---------------|--------|----------|
| GIS overlay | EPA BST, SUSTAIN | No | No | Moderate (ArcGIS) | Rarely | BST abandoned (2014); SUSTAIN discontinued (2016) |
| AHP/MCDA | Various | No | No | Moderate | Rarely | Methodology only; no reusable tools |
| FIS-based | BRAT (ecology) | No | No | Low (custom) | No | Active methodology; legacy codebase (ArcPy 10.x) |
| SWMM + optimization | OSTRICH-SWMM, Rhodium-SWMM, Greenopt | Yes (lumped) | Yes | Low (expert) | Rarely | All effectively abandoned (see text) |
| ABM for adoption | G-SSA | No (social) | No | Moderate (NetLogo) | Sometimes | Paper only; no code published |
| ABM for physical siting | *None published* | — | — | — | — | — |

The final row is empty because no published agent-based model combines dynamic water flow simulation with real GIS data for green infrastructure placement optimization. Existing ABMs address social adoption dynamics (G-SSA), maintenance scheduling, or regulatory interplay—not the physical question of where to place facilities based on how water actually moves across the landscape. The SWMM-coupled tools that do perform dynamic simulation and optimization require substantial expertise, calibration data, and computational resources—and as documented above, none have sustained development or community adoption beyond their initial publication. The bottleneck in this space is not algorithmic but practical: no accessible, maintained tool exists for GI placement optimization.

---

## 12. Conclusion: Toward an ABM for Bioswale Placement

This review identifies a convergence of mature components that have not yet been combined:

1. **Fuzzy inference systems** have been validated for environmental facility siting through BRAT's 89.97% accuracy against 8,060 beaver dam locations. The two-stage cascaded FIS architecture—physical suitability followed by capture potential—transfers to bioswale siting with appropriate input variable substitution.

2. **Urban flow routing** requires modifications to standard D8 algorithms to account for engineered infrastructure, but practical hybrid approaches—modified D8 with street-based preferential flow, TWI for accumulation hotspots, discrete inlet capture—are well-supported in the literature.

3. **Portland's 3,000+ GSI facilities** provide a validation dataset analogous to BRAT's beaver dam inventory, along with 30 years of performance monitoring data and codified siting criteria.

4. **Agent-based modeling** in NetLogo offers an accessible platform for dynamic water flow simulation, with built-in optimization support through BehaviorSpace and a visual interface that supports stakeholder engagement.

5. **Environmental justice** metrics are absent from the vast majority of GI siting tools, representing both a documented gap and an opportunity for meaningful contribution.

The proposed approach—an ABM where water agents flow across real GIS terrain, bioswale agents intercept and infiltrate them, and a fuzzy inference system scores candidate locations—would be the first to combine dynamic water simulation with spatial siting optimization in an accessible platform. By testing configurations against Portland's existing facility inventory, the model can be validated against three decades of real-world siting decisions, and by incorporating equity metrics as explicit optimization objectives, it can address one of the most significant gaps in current practice.

---

## References

### EPA Tools and Guidance
- U.S. Environmental Protection Agency. (2022). Best Management Practices (BMPs) Siting Tool. https://www.epa.gov/water-research/best-management-practices-bmps-siting-tool
- U.S. Environmental Protection Agency. (2016). System for Urban Stormwater Treatment and Analysis Integration (SUSTAIN). https://www.epa.gov/water-research/system-urban-stormwater-treatment-and-analysis-integration-sustain

### Fuzzy Inference Systems
- Macfarlane, W.W., Wheaton, J.M., Bouwes, N., Jensen, M.L., Gilbert, J.T., Hough-Snee, N., & Shivick, J.A. (2017). Modeling the capacity of riverscapes to support beaver dams. *Geomorphology*, 277, 72–99. https://doi.org/10.1016/j.geomorph.2015.11.019
- Macfarlane, W.W., Wheaton, J.M., & Jensen, M.L. (2014). The Utah Beaver Restoration Assessment Tool: A Decision Support & Planning Tool. Utah State University.
- BRAT Documentation. Riverscapes Consortium. https://brat.riverscapes.net/
- scikit-fuzzy Documentation. https://scikit-fuzzy.readthedocs.io/

### Urban Drainage Networks
- Impact of Drainage Network Structure on Urban Inundation. (2025). *MDPI Water*, 17(7), 990. https://www.mdpi.com/2073-4441/17/7/990
- Potentialities of Complex Network Theory Tools for Urban Drainage. (2022). *Water Resources Research*. https://doi.org/10.1029/2022WR032277
- Centrality and Shortest Path Length Measures for Urban Drainage Networks. (2019). *Applied Network Science*. https://doi.org/10.1007/s41109-019-0247-8
- GIS-based Spatial Approaches to Urban Catchment Delineation. (2024). *Springer*. https://doi.org/10.1007/s43832-024-00083-z
- Algorithm for Belowground Stormwater Network Topology. (2022). *Hydrology and Earth System Sciences*, 26, 4279. https://hess.copernicus.org/articles/26/4279/2022/
- Fully Automated Simplification of Urban Drainage Models. (2024). *Water Science and Technology*. https://doi.org/10.2166/wst.2024.317
- Dobson, B. et al. (2025). SWMManywhere: Synthesis of urban drainage networks. *Journal of Open Source Software*. https://github.com/ImperialCollegeLondon/SWMManywhere

### Multi-Criteria Decision Analysis
- Green Infrastructure Planning Principles: AHP. (2022). *MDPI Sustainability*, 14(9), 5170. https://www.mdpi.com/2071-1050/14/9/5170
- AHP-TOPSIS for Stormwater Climate Adaptation. (2021). *MDPI Water*, 13(17), 2422. https://www.mdpi.com/2073-4441/13/17/2422
- LID Site Selection Comparative Analysis. (2024). *Journal of Environmental Management*. https://doi.org/10.1016/j.jenvman.2024.120198

### Optimization Tools
- GIP-SWMM: Green Infrastructure Placement Tool. (2020). *Journal of Environmental Management*. https://doi.org/10.1016/j.jenvman.2020.111718
- OSTRICH-SWMM: Open-Source Multi-Objective Optimization. (2018). *Environmental Modelling & Software*. https://doi.org/10.1016/j.envsoft.2018.07.009
- Taraghi, N. et al. (2023). Rhodium-SWMM: Green Infrastructure Placement Under Deep Uncertainty. *Environmental Modelling & Software*. https://doi.org/10.1016/j.envsoft.2023.105651
- Abdalla, E.M.H. et al. (2024). SWMMLIDopt: Multi-objective optimization of LID measures. *Journal of Hydroinformatics*. https://github.com/ElhadiMohsenAbdalla/SWMMLIDOPT
- Optimizing GI Size, Location, and Connection. (2023). *Journal of Hydrology*. https://doi.org/10.1016/j.jhydrol.2023.130416
- Critical Review on Optimization and Meta-Heuristic Techniques for GI. (2024). *AQUA — Water Infrastructure, Ecosystems and Society*, 73(6), 1135. https://doi.org/10.2166/aqua.2024.073
- U.S. Environmental Protection Agency. Greenopt: Multi-Objective Green Infrastructure Optimization. https://github.com/USEPA/Greenopt

### Open-Source Software Repositories (cited in Section 6.2)
- McDonnell, B.E. et al. PySWMM: Python Wrappers for SWMM. https://github.com/pyswmm/pyswmm
- Yearke, T. et al. OSTRICH-SWMM. https://github.com/lsmatott/ostrich-swmm
- Taraghi, N. Rhodium-SWMM. https://github.com/NastaranT/rhodium-swmm
- Companion inventory of open-source tools and adoption analysis: `research/open_source_tools.md`

### Agent-Based Models
- G-SSA: Green Stormwater Infrastructure Social Spatial Adoption Model. (2021). *PubMed*. https://pubmed.ncbi.nlm.nih.gov/34346118/

### Portland BES and Performance Data
- City of Portland Bureau of Environmental Services. (2025). 2025 Stormwater Management Manual. https://www.portland.gov/bes/stormwater/2025-stormwater-management-manual
- City of Portland BES. (2025). About Green Streets. https://www.portland.gov/bes/stormwater/about-green-streets
- The First Thirty Years of Green Stormwater Infrastructure in Portland, Oregon. (2025). *MDPI Sustainability*, 17(15), 7159. https://www.mdpi.com/2071-1050/17/15/7159
- PortlandMaps Stormwater System Plan MapServer. https://www.portlandmaps.com/arcgis/rest/services/Public/Stormwater_System_Plan/MapServer

### Environmental Justice
- Environmental Justice Implications of Green Infrastructure Siting. (2021). *Journal of Environmental Policy & Planning*. https://doi.org/10.1080/1523908X.2021.1945916
- Georgetown Climate Center. Green Infrastructure Toolkit — Equity. https://www.georgetownclimate.org/adaptation/toolkits/green-infrastructure-toolkit/equity-and-environmental-justice.html
- iPlan-GreenS2: Open-Source Tool for Equitable GSI Siting. (2023). *ASCE Journal of Environmental Engineering*. https://doi.org/10.1061/JOEEDU.EEENG-7586

### Climate Uncertainty
- Uncertainty in Urban Stormwater BMP Assessment. (2018). *Frontiers in Built Environment*, 4, 71. https://doi.org/10.3389/fbuil.2018.00071
- Optimizing Green Infrastructure Under Precipitation Uncertainty. (2019). *Omega*. https://doi.org/10.1016/j.omega.2019.03.011

### Design Standards
- NACTO. (2013). Urban Street Design Guide: Bioswales. https://nacto.org/publication/urban-street-design-guide/street-design-elements/stormwater-management/bioswales/
- Minnesota Pollution Control Agency. (2023). Stormwater Manual: Bioretention Design Criteria. https://stormwater.pca.state.mn.us/design_criteria_for_bioretention
- Caltrans. (2018). Design Guidance: Biofiltration Swale. https://dot.ca.gov/-/media/dot-media/programs/design/documents/2_dg-biofiltration_swale_ada.pdf

### Bioswale Performance
- International Journal of Scientific and Research Archives. (2020). Bioswale Performance Review. https://ijsra.net/sites/default/files/IJSRA-2020-0045.pdf
- Minnesota Pollution Control Agency. Pollutant Removal by BMPs. https://stormwater.pca.state.mn.us/index.php/Information_on_pollutant_removal_by_BMPs

### Topographic Wetness Index
- TWI for Urban Flood-Prone Area Identification. (2017). Illinois State Water Survey. https://www.isws.illinois.edu/pubdoc/CR/ISWSCR2017-02.pdf
- TWI Calibration with SAR Data for SuDS Placement. (2024). *MDPI Sustainability*, 16(2), 598. https://www.mdpi.com/2071-1050/16/2/598

### General References
- Jenson, S.K. & Domingue, J.O. (1988). Extracting topographic structure from digital elevation data for geographic information system analysis. *Photogrammetric Engineering and Remote Sensing*, 54(11), 1593–1600.
- Saaty, T.L. (1980). *The Analytic Hierarchy Process*. McGraw-Hill.
- Wilensky, U. (1999). NetLogo. Center for Connected Learning and Computer-Based Modeling, Northwestern University. http://ccl.northwestern.edu/netlogo/
