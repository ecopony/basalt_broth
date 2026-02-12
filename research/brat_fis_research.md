# BRAT Fuzzy Inference System: Methodology Research and Transferability to Bioswale Siting

## Executive Summary

The Beaver Restoration Assessment Tool (BRAT) developed by Macfarlane, Wheaton, and colleagues at Utah State University uses a Fuzzy Inference System (FIS) to model stream reach capacity for supporting beaver dams. This research examines whether BRAT's FIS methodology could transfer to urban bioswale siting optimization.

**Key Finding:** BRAT's FIS approach is highly transferable in concept but would require significant adaptation. The core value of FIS--handling uncertainty, combining multiple factors with expert knowledge, and producing continuous suitability scores--applies directly to bioswale siting. However, the specific inputs, membership functions, and rules would need to be entirely redesigned for the urban stormwater context.

---

## 1. BRAT's FIS Methodology

### 1.1 Overview and Architecture

BRAT uses a **two-stage cascaded FIS architecture**:

1. **Vegetation FIS** (Stage 1): Combines riparian vegetation suitability to produce a vegetation-based dam capacity score
2. **Combined FIS** (Stage 2): Integrates the vegetation FIS output with hydrologic factors to produce final dam density estimates

This cascaded approach allows the model to first assess habitat quality (vegetation) and then overlay physical constraints (hydrology, slope).

### 1.2 Input Variables

#### Stage 1: Vegetation FIS (2 inputs)

| Input | Description | Data Source |
|-------|-------------|-------------|
| **30m Buffer Vegetation** | Streamside vegetation suitability for beaver foraging and dam building | LANDFIRE Existing Vegetation Type |
| **100m Buffer Vegetation** | Riparian/upland vegetation to support colony expansion and dam complex maintenance | LANDFIRE Existing Vegetation Type |

Each vegetation type receives a **preference score (0-4)**:
- 0 = Unsuitable (e.g., urban, barren)
- 1 = Barely suitable
- 2 = Moderately suitable
- 3 = Suitable
- 4 = Preferred (aspen, willow, cottonwood)

#### Stage 2: Combined FIS (3-4 inputs)

| Input | Description | Derivation |
|-------|-------------|------------|
| **Vegetation Dam Capacity** | Output from Stage 1 | Vegetation FIS (dams/km) |
| **Baseflow Stream Power** | Ability to build dams at low flow | Regional curves relating drainage area to PQ80 (flow exceeded 80% of time) |
| **Q2 Stream Power** | Dam persistence under typical floods | Two-year recurrence interval flood discharge |
| **Slope** | Stream gradient constraint | DEM-derived reach slope |

### 1.3 Membership Functions

BRAT uses **trapezoidal membership functions** for continuous variables. From the pyBRAT source code:

**Slope Membership Functions:**
```python
slope['flat'] = fuzz.trapmf(slope.universe, [0, 0, 0.0002, 0.005])
slope['can'] = fuzz.trapmf(slope.universe, [0.0002, 0.005, 0.12, 0.15])
slope['probably'] = fuzz.trapmf(slope.universe, [0.12, 0.15, 0.17, 0.23])
slope['cannot'] = fuzz.trapmf(slope.universe, [0.17, 0.23, 1, 1])
```

These translate to linguistic categories:
- **flat**: Slopes < 0.5% (ideal for beaver dams)
- **can**: Slopes 0.5-15% (beaver can build here)
- **probably**: Slopes 12-23% (marginal)
- **cannot**: Slopes > 17% (too steep for dam persistence)

### 1.4 Fuzzy Rules Structure

BRAT's Combined FIS uses a rule table that maps combinations of input membership categories to output dam density categories. The general form is:

```
IF vegetation IS [category] AND baseflow_power IS [category] AND slope IS [category]
THEN dam_capacity IS [output_category]
```

**Output Categories (dams/km):**
- **None**: 0 dams/km
- **Rare**: >0-1 dams/km (dispersing individuals only)
- **Occasional**: >1-5 dams/km (occasional dam or small colony)
- **Frequent**: >5-15 dams/km (multiple colonies, dam complexes)
- **Pervasive**: >15-40 dams/km (extensive dam complexes, many colonies)

### 1.5 Defuzzification

BRAT uses **centroid defuzzification** (center of gravity method) to produce crisp output values. This is the most common approach in Mamdani-type FIS and produces smooth, continuous outputs.

### 1.6 Seven Lines of Evidence Framework

The full BRAT model evaluates seven physical and ecological factors:

1. **Reliable water source** (perennial stream)
2. **Streamside vegetation** (30m buffer) for foraging and dam building
3. **Riparian/upland vegetation** (100m buffer) for colony expansion
4. **Low-flow dam construction** feasibility (baseflow stream power)
5. **Flood persistence** (Q2 stream power)
6. **Stream gradient** (not too low or too high)
7. **River size** (not too large to preclude dam building)

---

## 2. Validation and Performance

### 2.1 Validation Methodology

BRAT was validated against **8,060 actual beaver dam locations** in Utah, documented via:
- Web-based inventory using Google Earth imagery
- Field-based dam location surveys
- Cross-referencing with existing dam databases

### 2.2 Validation Results

The model achieved **89.97% accuracy** in segregating factors controlling beaver dam occurrence and density. Key findings:
- Beavers preferentially build dams in reaches with higher modeled capacity
- Beavers avoid reaches with lower modeled capacity
- Model performance improves with higher-resolution input data

### 2.3 Why FIS Works for BRAT

1. **Handles categorical ambiguity**: Vegetation types don't have sharp boundaries in beaver preference
2. **Incorporates expert knowledge**: Ecological understanding of beaver behavior encoded directly in rules
3. **Accounts for uncertainty**: Trapezoidal membership functions allow gradual transitions
4. **Produces continuous output**: Dam density is inherently a continuous variable
5. **Interpretable**: Rules can be explained to wildlife managers

---

## 3. Technical Implementation

### 3.1 Software Stack

- **Original**: MATLAB (matBRAT)
- **Current**: Python (pyBRAT) using **scikit-fuzzy (skfuzzy)** library
- **GIS Integration**: ArcGIS/ArcPy for spatial processing

### 3.2 scikit-fuzzy Implementation

The pyBRAT codebase uses scikit-fuzzy for FIS implementation:

```python
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define antecedent (input) and consequent (output) variables
vegetation = ctrl.Antecedent(np.arange(0, 45, 0.01), 'vegetation')
slope = ctrl.Antecedent(np.arange(0, 1, 0.0001), 'slope')
capacity = ctrl.Consequent(np.arange(0, 45, 0.01), 'capacity')

# Define membership functions
vegetation['none'] = fuzz.trapmf(vegetation.universe, [0, 0, 0.1, 0.5])
vegetation['rare'] = fuzz.trapmf(vegetation.universe, [0.1, 0.5, 1, 1.5])
# ... etc

# Define rules
rule1 = ctrl.Rule(vegetation['pervasive'] & slope['flat'], capacity['pervasive'])
rule2 = ctrl.Rule(vegetation['frequent'] & slope['can'], capacity['frequent'])
# ... etc

# Create control system
dam_ctrl = ctrl.ControlSystem([rule1, rule2, ...])
dam_sim = ctrl.ControlSystemSimulation(dam_ctrl)
```

---

## 4. Transferability to Urban Bioswale Siting

### 4.1 What Transfers Well

| BRAT Concept | Bioswale Analog | Notes |
|--------------|-----------------|-------|
| **FIS architecture** | Directly applicable | Cascaded FIS could separate physical suitability from optimization objectives |
| **Trapezoidal membership functions** | Directly applicable | Good for handling gradual transitions in slope, soil infiltration, etc. |
| **Centroid defuzzification** | Directly applicable | Produces continuous suitability scores |
| **Multi-criteria combination** | Directly applicable | Bioswale siting also requires balancing multiple factors |
| **Rule-based expert knowledge** | Directly applicable | Engineering design criteria can be encoded as rules |
| **Validation against existing facilities** | Portland has 3,000+ existing bioswales for validation |

### 4.2 Proposed Bioswale FIS Architecture

**Stage 1: Physical Suitability FIS**

| Input Variable | Membership Categories | Data Source |
|----------------|----------------------|-------------|
| **Slope** | flat (0-2%), moderate (2-4%), steep (4-6%), unsuitable (>6%) | DEM |
| **Soil infiltration rate** | excellent (>2 in/hr), good (0.5-2), marginal (0.2-0.5), poor (<0.2) | SSURGO |
| **Depth to groundwater** | safe (>10ft), adequate (5-10ft), marginal (3-5ft), unsuitable (<3ft) | USGS/well logs |

**Stage 2: Runoff Capture FIS**

| Input Variable | Membership Categories | Data Source |
|----------------|----------------------|-------------|
| **Physical suitability** | Output from Stage 1 | Stage 1 FIS |
| **Upstream impervious area** | low (<20%), moderate (20-50%), high (50-80%), very high (>80%) | Impervious surface layer |
| **Flow accumulation** | minimal, low, moderate, high | DEM flow accumulation |
| **Distance to storm drain** | near (<100ft), moderate (100-300ft), far (>300ft) | Storm sewer network |

**Output Categories:**
- **Unsuitable**: Physical constraints preclude bioswale installation
- **Marginal**: Possible but not ideal; would require engineered modifications
- **Moderate**: Reasonable candidate site
- **Good**: Strong candidate with favorable conditions
- **Optimal**: Ideal conditions; high capture potential with minimal constraints

### 4.3 What Does NOT Transfer

| BRAT Component | Why It Doesn't Transfer | Bioswale Replacement |
|----------------|------------------------|---------------------|
| **Vegetation suitability** | Urban context lacks riparian vegetation assessment | Impervious surface coverage, land use zoning |
| **Stream power calculations** | No stream channels in urban drainage | Surface runoff velocity, flow concentration points |
| **Perennial water requirement** | Bioswales handle intermittent storm flows | Storm event frequency, design storm sizing |
| **Dam persistence under floods** | No analog | Bioswale sizing relative to catchment area |
| **Beaver foraging range** | No analog | Pedestrian/vehicle access for maintenance |
| **Regional hydrologic curves** | Different hydrology | Urban runoff coefficients, time of concentration |

### 4.4 Fundamental Differences: Stream Ecosystems vs. Urban Drainage

| Dimension | BRAT (Stream Ecosystem) | Bioswale Siting (Urban Drainage) |
|-----------|------------------------|----------------------------------|
| **Water source** | Continuous perennial flow | Intermittent storm events |
| **Optimization target** | Maximize habitat potential | Maximize runoff capture, minimize cost |
| **Constraints** | Ecological (vegetation, gradient) | Engineering + regulatory (setbacks, utilities) |
| **Spatial unit** | Stream reach (line segment) | Parcel/grid cell (polygon/raster) |
| **Flow direction** | Channel-confined | Diffuse overland flow until concentrated |
| **Temporal dynamics** | Seasonal baseflow/flood cycles | Individual storm events (hours) |
| **Biological agent** | Beaver behavior/preference | Human construction/maintenance |
| **Uncertainty sources** | Ecological variability | Data quality, storm variability |

---

## 5. Implementation Recommendations

### 5.1 Recommended Approach

1. **Use cascaded FIS architecture** similar to BRAT's two-stage approach:
   - Stage 1: Physical suitability (binary go/no-go with fuzzy margins)
   - Stage 2: Optimization potential (capture efficiency, cost-effectiveness)

2. **Implement in Python using scikit-fuzzy** for consistency with modern data science workflows

3. **Define membership functions empirically** using Portland's existing bioswale performance data:
   - Analyze 3,000+ existing facilities
   - Correlate siting characteristics with performance metrics
   - Calibrate membership function boundaries to observed data

4. **Validate against Portland's bioswale inventory** similar to BRAT's dam validation approach

### 5.2 Sample Rule Set for Bioswale Siting

```
# Physical suitability rules
IF slope IS flat AND infiltration IS excellent AND groundwater IS safe THEN suitability IS optimal
IF slope IS moderate AND infiltration IS good AND groundwater IS adequate THEN suitability IS good
IF slope IS steep OR infiltration IS poor THEN suitability IS unsuitable

# Capture potential rules
IF suitability IS good AND impervious IS high AND flow_accumulation IS high THEN priority IS optimal
IF suitability IS moderate AND impervious IS moderate THEN priority IS moderate
IF suitability IS unsuitable THEN priority IS unsuitable
```

### 5.3 Advantages of FIS Over Weighted Overlay

| Approach | Strengths | Weaknesses |
|----------|-----------|------------|
| **Weighted overlay** | Simple, widely understood | Linear combination assumes independence; sharp category boundaries |
| **AHP** | Handles criteria prioritization | Still produces linear combination; subjective pairwise comparisons |
| **Fuzzy Inference System** | Handles non-linear interactions; graceful degradation at boundaries; interpretable rules; explicit uncertainty handling | More complex to implement; requires expert input for rules |

For bioswale siting, FIS offers key advantages:
- **Non-linear rule interactions**: "IF slope IS steep THEN unsuitable" can override other factors
- **Graceful boundaries**: A site at 5.9% slope isn't sharply different from 6.1%
- **Interpretable outputs**: Rules can be explained to planners and engineers
- **Uncertainty propagation**: Confidence in output reflects input uncertainty

---

## 6. Conclusions

### 6.1 Transferability Assessment

**BRAT's FIS methodology is conceptually transferable to bioswale siting** with the following caveats:

1. **Architecture transfers**: Cascaded FIS with physical suitability followed by optimization objectives
2. **Technique transfers**: Trapezoidal membership functions, Mamdani inference, centroid defuzzification
3. **Validation approach transfers**: Use existing Portland bioswales (3,000+) similar to how BRAT used 8,000+ dam locations
4. **Inputs do NOT transfer**: Entirely different physical and ecological context requires new input variables
5. **Rules do NOT transfer**: Expert engineering knowledge must replace ecological knowledge

### 6.2 Key Takeaways

1. FIS is appropriate when:
   - Multiple factors interact non-linearly
   - Boundary conditions are fuzzy, not crisp
   - Expert knowledge needs to be encoded
   - Output uncertainty should reflect input uncertainty

2. Bioswale siting meets all these criteria

3. BRAT provides a validated precedent for FIS in environmental siting applications

4. Implementation path is clear: scikit-fuzzy + GIS integration

### 6.3 Next Steps

1. Define membership functions for Portland-specific inputs (slope, soil, groundwater, impervious cover)
2. Develop rule set based on Portland BES design criteria
3. Prototype FIS in Python using scikit-fuzzy
4. Validate against existing bioswale locations
5. Integrate into NetLogo model for optimization

---

## References

### Primary Sources

- Macfarlane, W.W., Wheaton, J.M., Bouwes, N., Jensen, M.L., Gilbert, J.T., Hough-Snee, N., and Shivick, J.A. (2017). [Modeling the capacity of riverscapes to support beaver dams](https://www.sciencedirect.com/science/article/abs/pii/S0169555X15302166). *Geomorphology*, 277, 72-99.

- Macfarlane, W.W., Wheaton, J.M., and Jensen, M.L. (2014). [The Utah Beaver Restoration Assessment Tool: A Decision Support & Planning Tool](https://www.researchgate.net/publication/267096045_The_Utah_Beaver_Restoration_Assessment_Tool_A_Decision_Support_Planning_Tool). Utah State University Ecogeomorphology & Topographic Analysis Lab.

### BRAT Documentation and Code

- [BRAT Documentation](https://brat.riverscapes.net/) - Riverscapes Consortium
- [pyBRAT GitHub Repository](https://github.com/Riverscapes/pyBRAT) - Python implementation
- [BRAT Combined FIS Tutorial](https://brat.riverscapes.net/Documentation/Tutorials/7-BRATCombinedFIS.html)
- [matBRAT Documentation](https://riverscapes.github.io/matBRAT/) - Original MATLAB version

### Fuzzy Logic Resources

- [scikit-fuzzy Documentation](https://scikit-fuzzy.readthedocs.io/en/latest/)
- [MATLAB Fuzzy Logic Toolbox - Mamdani vs. Sugeno](https://www.mathworks.com/help/fuzzy/types-of-fuzzy-inference-systems.html)

### Urban Green Infrastructure Siting

- [EPA BMP Siting Tool](https://www.epa.gov/water-research/best-management-practices-bmps-siting-tool)
- [Identifying Priority Areas for Planning Urban Green Infrastructure: A Fuzzy AI-Based Framework](https://www.mdpi.com/2413-8851/9/4/126)
- [NACTO Bioswales Design Guide](https://nacto.org/publication/urban-street-design-guide/street-design-elements/stormwater-management/bioswales/)

### Bioswale Design Criteria

- [Minnesota Stormwater Manual - Bioretention Design Criteria](https://stormwater.pca.state.mn.us/design_criteria_for_bioretention)
- [Clemson University - Introduction to Bioswales](https://hgic.clemson.edu/factsheet/an-introduction-to-bioswales/)
- [SUNY ESF - Bioswale Calculator](https://www.esf.edu/ere/endreny/GICalculator/BioswaleIntro.html)
