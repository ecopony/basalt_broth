# Open Source Tools for Bioswale Siting and Green Infrastructure Placement

**Date:** 2026-02-09 (updated with traction/adoption analysis)
**Purpose:** Reference inventory of open source software relevant to the Basalt Broth project

---

## Summary

Every open-source tool that performs actual GI placement optimization uses the same architecture: **SWMM as simulation engine + external optimizer**. None use agent-based modeling, fuzzy inference for suitability scoring, or an accessible visual platform like NetLogo. The closest methodological ancestor for the FIS approach is **pyBRAT** (beaver dam siting in riparian ecosystems).

**Adoption reality:** The tools with real traction are general-purpose platforms (PySWMM, WhiteboxTools, pysheds). The GI placement optimization tools (Rhodium-SWMM, OSTRICH-SWMM, Greenopt, SWMMLIDopt) are paper companion code — published alongside journal articles, pushed to GitHub, and never meaningfully maintained or adopted. No tool in this space has built a community around GI placement optimization.

---

## Tier 1: Direct Placement/Siting Optimization

These tools specifically address *where* to place green infrastructure. None have achieved significant adoption.

### Rhodium-SWMM

| | |
|---|---|
| **URL** | https://github.com/NastaranT/rhodium-swmm |
| **Language** | Python |
| **Stars / Forks** | 11 / 6 |
| **Last push** | 2023-06-16 |
| **License** | None listed |
| **Status** | Dead. No push in 2.5 years. |

Multi-objective optimization of GI placement under deep uncertainty. Connects EPA SWMM to the Rhodium library (Many-Objective Robust Decision Making). GI types, sizing, and placement are defined as decision levers with multiple objectives (cost, CSO reduction, etc.). Published in *Environmental Modelling & Software* (Taraghi et al., 2023).

**Who made it:** Nastaran Taraghi ([@NastaranT](https://github.com/NastaranT)) — sole contributor, 7 total commits. Published the paper, pushed the code, moved on. Zero community.

### OSTRICH-SWMM

| | |
|---|---|
| **URL** | https://github.com/lsmatott/ostrich-swmm |
| **Language** | Python |
| **Stars / Forks** | 39 / 20 |
| **Last push** | 2024-12-24 |
| **Open issues** | 22 |
| **License** | GNU GPLv2 |
| **Status** | Most-used GI placement optimizer, but sporadic updates. |

Connects SWMM with the OSTRICH optimization toolkit. Supports multi-objective optimization with numerous heuristic algorithms (simulated annealing, genetic algorithms, others), many parallelized. Published case study on rain barrel placement in Buffalo, NY to reduce CSOs.

**Who made it:** Tom Yearke ([@tyearke](https://github.com/tyearke)) — 23 of 35 commits. 5 total contributors. The 22 open issues and 20 forks suggest some community interest, but forks come in at roughly one per year from scattered academics (Iran, China, Norway, US). People find it via the paper, not through a community.

### EPA Greenopt

| | |
|---|---|
| **URL** | https://github.com/USEPA/Greenopt |
| **Language** | Python |
| **Stars / Forks** | 4 / 2 |
| **Last push** | 2020-07-30 |
| **License** | None listed (EPA public domain) |
| **Status** | Dead. No push in 5.5 years. |

Multi-objective optimization of GI placement using the Borg MOEA. Evaluates candidate management plans for runoff/pollutant load reduction vs. cost. Designed to complement EPA's WMOST watershed tool.

**Who made it:** EPA statutory code dump. Published because policy requires it, not because anyone intends to maintain it.

### SWMMLIDopt

| | |
|---|---|
| **URL** | https://github.com/ElhadiMohsenAbdalla/SWMMLIDOPT |
| **Language** | R (built on swmmr package) |
| **Stars / Forks** | 1 / 0 |
| **Last push** | 2023-07-31 |
| **License** | GNU GPL (per paper) |
| **Status** | Paper companion code. Never used by anyone else. |

Multi-objective optimization of LID measure selection and placement. Optimizes for peak flow minimization and cost minimization. Published November 2024 in *Journal of Hydroinformatics*.

### EPA SERTO

| | |
|---|---|
| **URL** | https://github.com/USEPA/SERTO |
| **Language** | Python / Jupyter Notebook |
| **Stars / Forks** | 2 / 2 |
| **Last push** | 2025-08-11 |
| **License** | None listed (EPA public domain) |
| **Status** | Barely exists. |

Work-in-progress package for optimizing infrastructure sizing and placement in stormwater systems. Also handles sensor network placement and emergency response. Built around EPA SWMM.

### pyBRAT (Beaver Restoration Assessment Tool)

| | |
|---|---|
| **URL** | https://github.com/Riverscapes/pyBRAT |
| **Language** | Python (ArcPy dependency) |
| **Stars / Forks** | 11 / 10 |
| **Last push** | 2026-02-03 |
| **Open issues** | 9 |
| **License** | GNU GPLv3 |
| **Status** | Legacy codebase; methodology lives on in sqlBRAT. |

Two-stage cascaded fuzzy inference system for environmental facility siting. Uses trapezoidal membership functions, Mamdani inference, centroid defuzzification. Validated against 8,060 beaver dam locations (89.97% accuracy). Not for bioswales, but the FIS architecture is directly transferable.

**Who made it:** Joe Wheaton's lab at **Utah State University**. Wheaton is a well-known fluvial geomorphologist and Professor of Riverscapes. The repo has 10 contributors from his lab (banderson1618, bangen, lhaycock, wally-mac, etc.). It's an established academic lab project, not a lone paper artifact. pyBRAT itself is legacy (ArcPy 10.x no longer supported by Esri) but the BRAT *methodology* lives on through sqlBRAT and the Riverscapes Consortium. The FIS logic is the valuable part, not the codebase.

---

## Tier 2: Simulation Engines and Building Blocks

Not siting tools per se, but the platforms that siting tools are built on. This is where the real traction lives.

### PySWMM

| | |
|---|---|
| **URL** | https://github.com/pyswmm/pyswmm |
| **Language** | Python |
| **Stars / Forks** | 350 / 151 |
| **Last push** | 2026-02-06 |
| **Open issues** | 12 |
| **License** | Custom |
| **Status** | **Most active tool in this space.** Real ecosystem, real users. |

Python wrapper for SWMM. Allows mid-simulation parameter manipulation including LID parameters. v2.0 (2024) added 100% INP file coverage, making it "easily suitable to embed into optimization." Ecosystem includes SWMMIO (visualization), StormReactor (water quality), pystorms (benchmarking).

**Who made it and who uses it:** Lead is Bryant McDonnell ([@bemcdonnell](https://github.com/bemcdonnell)), Hydroinformatics Engineer at **HydroDigital** — a consulting firm, not an academic side project. Key contributors include Michael Tryby (former **EPA**, PhD in Civil Engineering, the SWMM engine developer), Katherine Ratliff (**EPA** Office of Research and Development), Constantine Karos (also **HydroDigital**), Abhiram ([@abhiramm7](https://github.com/abhiramm7)) at **Xylem** (major water technology company), and Brooke Mason at **University of Michigan** kLabUM. Recent forks from a **USGS** employee plus users in China, Iran, Germany, and Canada. ~10 forks in the last 6 months. External bug reports and PRs from real users. **This is the only tool in this space with a genuine user base**, because it wraps the regulatory-standard model — if you work with SWMM in Python, you need this.

### SWMManywhere

| | |
|---|---|
| **URL** | https://github.com/ImperialCollegeLondon/SWMManywhere |
| **Language** | Python |
| **Stars / Forks** | 33 / 5 |
| **Last push** | 2026-02-09 |
| **Open issues** | 100 |
| **License** | BSD 3-Clause |
| **Status** | **Actively developed right now.** 100 open issues = lots of work in progress. |

Derives and simulates sewer networks anywhere in the world from publicly available geospatial data — just give it a bounding box. Network topology derivation accounts for impervious area and pipe slope. Published in JOSS 2025. Similar philosophy to Basalt Broth's use of Portland open data.

**Who made it:** Barney Dobson ([@barneydobson](https://github.com/barneydobson)) — 633 of 633 non-bot commits. **Imperial College London** Research Software Engineering group (Diego Alonso Álvarez also contributes). Funded research project with CI infrastructure and JOSS publication. Essentially one researcher's PhD/postdoc work, but backed by institutional support. One to watch.

### WhiteboxTools

| | |
|---|---|
| **URL** | https://github.com/jblindsay/whitebox-tools |
| **Language** | Rust (with Python frontend) |
| **Stars / Forks** | 1,108 / 183 |
| **Last push** | 2025-02-07 |
| **Open issues** | 170 |
| **License** | MIT |
| **Status** | Healthy. Most starred tool in this entire inventory. |

Comprehensive terrain and hydrology analysis platform. D8/Dinf flow accumulation, TWI, watershed delineation, slope, curvature, sink removal. 500+ geospatial tools. Most starred tool in this entire inventory.

**Who made it:** John Lindsay — Professor at **University of Guelph**, geomorphometrist. Wrote virtually all 776 commits himself. Spun it into **Whitebox Geospatial Inc.** (a company). One person's life work, but widely adopted because it fills a real gap — free alternative to ArcGIS Spatial Analyst for terrain analysis. Used by GIS practitioners who can't afford (or don't want to depend on) Esri.

### pysheds

| | |
|---|---|
| **URL** | https://github.com/mdbartos/pysheds |
| **Language** | Python |
| **Stars / Forks** | 852 / 227 |
| **Last push** | 2025-08-14 |
| **Open issues** | 95 |
| **License** | GNU GPLv3 |
| **Status** | Healthy. Widely used for lightweight watershed delineation. |

Simple and fast watershed delineation. D8 flow direction, flow accumulation, catchment delineation from DEMs. Pure Python, no ArcGIS dependency. Popular because it's pip-installable with minimal dependencies — the "just works" option for Python developers who need quick watershed analysis.

### RichDEM

| | |
|---|---|
| **URL** | https://github.com/r-barnes/richdem |
| **Language** | C++ (with Python bindings) |
| **Stars / Forks** | 307 / 79 |
| **Last push** | 2024-06-24 |
| **Open issues** | 61 |
| **License** | GNU GPLv3 |
| **Status** | Slowing down. No push in 20 months. |

High-performance terrain and hydrology analysis. D8, Dinf, flow accumulation, slope, curvature, wetness index. Designed for performance on large rasters.

### EPA SWMM (Storm Water Management Model)

| | |
|---|---|
| **URL** | https://github.com/USEPA/Stormwater-Management-Model |
| **Language** | C |
| **Stars / Forks** | 319 / 213 |
| **Last push** | 2025-05-01 |
| **Open issues** | 57 |
| **License** | Public domain (EPA) |
| **Status** | The industry standard. Slow-moving but not going anywhere. |

The regulatory-standard dynamic hydrology-hydraulic water quality simulation model. Includes LID module for bioretention, bioswales, rain gardens, etc. Foundation for all the optimization tools in Tier 1. Every city with a stormwater permit has SWMM models.

### EPA GIFMod (Green Infrastructure Flexible Model)

| | |
|---|---|
| **URL** | https://github.com/USEPA/GIFMod |
| **Language** | C++ |
| **Stars / Forks** | 6 / 4 |
| **Last push** | 2020-05-25 |
| **License** | GNU GPLv3 |
| **Status** | Dead. No push in 5.5 years. |

Models hydraulic and water quality performance of individual GI facilities (bioswales, rain gardens, etc.). Supports deterministic and probabilistic inverse modeling. Not a siting tool — models how a *single facility performs*.

### SWMMIO

| | |
|---|---|
| **URL** | https://github.com/pyswmm/swmmio |
| **Language** | Python |
| **Stars / Forks** | 143 |
| **Last push** | 2026-02-05 |
| **License** | MIT |
| **Status** | Active. Part of the PySWMM ecosystem. |

Tools for interacting with, editing, and visualizing EPA SWMM5 models. GIS integration.

### swmm_api

| | |
|---|---|
| **URL** | https://github.com/MarkusPic/swmm_api |
| **Language** | Python |
| **Stars / Forks** | 17 |
| **Last push** | 2026-01-13 |
| **License** | MIT |

Read, manipulate, and run SWMM projects. Strong INP file parsing and GIS data interaction.

### StormReactor

| | |
|---|---|
| **URL** | https://github.com/kLabUM/StormReactor |
| **Language** | Python |
| **Stars / Forks** | 27 / 10 |
| **Last push** | 2023-07-06 |
| **License** | GNU LGPLv3 |
| **Status** | Stale. No push in 2.5 years. |

Water quality modeling (pollutant generation and removal) integrated with SWMM's water balance engine. Models TSS, nutrients, etc. From the kLabUM group at **University of Michigan**.

### pystorms

| | |
|---|---|
| **URL** | https://github.com/kLabUM/pystorms |
| **Language** | Python / Jupyter Notebook |
| **Stars / Forks** | 35 / 16 |
| **Last push** | 2025-08-22 |
| **License** | GNU GPLv3 |
| **Status** | Niche but maintained. |

Simulation sandbox for designing and evaluating stormwater control algorithms. Benchmark scenarios for testing optimization approaches. Also from **University of Michigan** kLabUM.

### PyDEM

| | |
|---|---|
| **URL** | https://github.com/creare-com/pydem |
| **Language** | Python / Cython |
| **Stars / Forks** | 127 / 37 |
| **Last push** | 2025-12-12 |
| **License** | Apache 2.0 |
| **Status** | Modest activity. |

Global hydrology analysis. Upstream contributing area, aspect, slope, TWI. Supports parallel processing.

---

## Tier 3: Watershed and BMP Planning

Broader-scope tools that include GI/BMP components.

### Model My Watershed (WikiWatershed)

| | |
|---|---|
| **URL** | https://github.com/WikiWatershed/model-my-watershed |
| **Language** | JavaScript (web app) |
| **Stars / Forks** | 58 |
| **Last push** | 2026-01-14 |
| **License** | Apache 2.0 |

Web-based watershed modeling and BMP planning. TR-55 runoff modeling, SLAMM, STEPL water quality algorithms. BMP spreadsheet tool for load reduction estimates.

### EPA National Stormwater Calculator

| | |
|---|---|
| **URL** | https://github.com/USEPA/National_Stormwater_Calculator_Desktop |
| **Language** | JavaScript |
| **Stars / Forks** | 7 |
| **Last push** | 2026-01-28 |
| **License** | None listed (EPA public domain) |

Estimates annual rainfall/runoff from a specific site using local soil, land cover, and historical rainfall. Evaluates LID control effectiveness. Site-scale, not watershed-scale.

### RBEROST

| | |
|---|---|
| **URL** | https://github.com/USEPA/RBEROST |
| **Language** | R / AMPL |
| **Stars / Forks** | 3 |
| **Last push** | 2026-01-28 |
| **License** | GNU GPLv3 |

Least-cost optimization of BMP combinations to meet nutrient loading targets across a river basin. Basin-scale.

### MAPC Stormwater Toolkit

| | |
|---|---|
| **URL** | https://github.com/MAPC/stormwater-toolkit |
| **Language** | Python (ArcGIS toolbox) |
| **Stars / Forks** | 9 |
| **Last push** | 2026-01-07 |
| **License** | None listed |

Maps stormwater outfall catchment areas for MS4 permit requirements. Includes BMP Prioritization Toolbox for initial screening.

---

## Not Actually Open Source

These tools are referenced in the literature as "open source" or "publicly available" but have no discoverable source code repository.

| Tool | Status | Notes |
|------|--------|-------|
| **EPA BMP Siting Tool** | ArcGIS 10.1 download only | Last updated August 2014 (v1.2). Essentially abandoned. |
| **EPA SUSTAIN** | Discontinued | ArcGIS 9.3 extension. No source code ever publicly released. |
| **GIP-SWMM** | Paper only | Described as Excel-VBA. No public repository found. |
| **iPlan-GreenS2** | Paper says "open-source" | No GitHub/GitLab repo discoverable. May require contacting authors. |
| **G-SSA** | Paper only | Cellular automata ABM for social adoption. No code published. |

---

## Traction Summary

### Tools with real adoption

| Tool | Stars | Forks | Why people use it |
|------|-------|-------|-------------------|
| **WhiteboxTools** | 1,108 | 183 | Free alternative to ArcGIS Spatial Analyst. Practical, not academic. |
| **pysheds** | 852 | 227 | Lightweight, pip-installable watershed delineation. Just works. |
| **PySWMM** | 350 | 151 | Python API to the regulatory standard. If you work with SWMM, you need this. |
| **EPA SWMM** | 319 | 213 | The industry standard itself. Every permitted city has SWMM models. |
| **RichDEM** | 307 | 79 | High-performance terrain analysis. Slowing down (no push in 20 months). |

### Niche but alive

| Tool | Stars | Forks | Notes |
|------|-------|-------|-------|
| **SWMMIO** | 143 | — | PySWMM ecosystem. Active. |
| **PyDEM** | 127 | 37 | Modest, still getting updates. |
| **OSTRICH-SWMM** | 39 | 20 | Most-used GI placement optimizer. 22 open issues suggest some community. Sporadic. |
| **pystorms** | 35 | 16 | U of Michigan kLabUM research group. Niche but maintained. |
| **SWMManywhere** | 33 | 5 | **Actively developed right now.** Imperial College London. JOSS-published. One to watch. |

### Paper companion code (published and abandoned)

| Tool | Stars | Forks | Last push | Notes |
|------|-------|-------|-----------|-------|
| **Rhodium-SWMM** | 11 | 6 | 2023-06 | Single author, 7 commits, zero community. |
| **pyBRAT** | 11 | 10 | 2026-02 | Lab project (USU). Code is legacy but methodology lives on. |
| **EPA GIFMod** | 6 | 4 | 2020-05 | EPA code dump. Dead. |
| **EPA Greenopt** | 4 | 2 | 2020-07 | EPA code dump. Dead. |
| **EPA SERTO** | 2 | 2 | 2025-08 | Barely exists. |
| **SWMMLIDopt** | 1 | 0 | 2023-07 | Never used by anyone else. |

### Key people in the space

| Person | Affiliation | Role |
|--------|-------------|------|
| **Bryant McDonnell** | HydroDigital / HydroInformatics LLC | PySWMM lead (462 commits). Hydroinformatics engineer. Commercial practice, not just academic. |
| **Michael Tryby** | Former EPA | SWMM engine developer. PhD Civil Engineering. PySWMM contributor. |
| **Katherine Ratliff** | EPA Office of Research and Development | PySWMM contributor. Center for Environmental Solutions and Emergency Response. |
| **Abhiram** | Xylem (water technology company) | PySWMM contributor. Industry adoption signal. |
| **John Lindsay** | University of Guelph / Whitebox Geospatial Inc. | WhiteboxTools sole creator (776 commits). Geomorphometrist. Turned it into a company. |
| **Joe Wheaton** | Utah State University | pyBRAT creator. Professor of Riverscapes. Well-known fluvial geomorphologist. |
| **Barney Dobson** | Imperial College London | SWMManywhere sole creator (633 commits). Active research. |
| **Brooke Mason** | University of Michigan kLabUM | PySWMM, StormReactor, pystorms. Academic lab driving the SWMM Python ecosystem. |

---

## Relevance to Basalt Broth

### What exists

All open-source placement optimization tools share one architecture: **SWMM simulation + external multi-objective optimizer** (NSGA-II, Borg MOEA, simulated annealing, etc.). This is powerful but heavyweight — requires SWMM expertise, calibration data, and significant compute.

### The adoption pattern

Tools with real traction are **general-purpose platforms** (PySWMM, WhiteboxTools, pysheds, SWMM itself). The **GI placement optimization tools** are uniformly paper companion code — published alongside a journal article, pushed to GitHub, and never meaningfully maintained or adopted. The space has no established, actively maintained tool for GI placement optimization. Every attempt got published but didn't build a community.

### What doesn't exist

No open-source tool combines:
- **Agent-based modeling** for the water flow simulation
- **Fuzzy inference system** for suitability scoring (adapted from pyBRAT)
- **Accessible visual platform** (NetLogo vs. SWMM command line)
- **Equity metrics** as a first-class optimization objective

### Most useful as reference

| Tool | What to learn from it |
|------|----------------------|
| **pyBRAT** | FIS architecture: two-stage cascaded Mamdani FIS, trapezoidal membership functions, scikit-fuzzy implementation, validation methodology |
| **Rhodium-SWMM** | Multi-objective optimization structure, handling deep uncertainty, Pareto front generation |
| **WhiteboxTools** | D8/Dinf flow routing, TWI calculation — potential preprocessing tool for our pipeline |
| **pysheds** | Lightweight alternative to WhiteboxTools for flow accumulation |
| **SWMManywhere** | Deriving sewer network topology from public data (similar philosophy to our approach) |
| **PySWMM** | If we ever want to benchmark against SWMM results |
