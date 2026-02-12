# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "gdal", "scipy"]
# ///
# ABOUTME: Two-stage Fuzzy Inference System for bioswale siting suitability.
# ABOUTME: Stage 1: physical suitability (slope × HSG). Stage 2: capture priority
# ABOUTME: (suitability × impervious fraction × TWI). Outputs rasters + ASCII grids.

import os
import numpy as np
from osgeo import gdal, ogr, osr
from scipy import stats

gdal.UseExceptions()

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
DERIVED_DIR = os.path.join(DATA_DIR, "derived")

# Input paths
SLOPE_PATH = os.path.join(DERIVED_DIR, "slope.tif")
TWI_PATH = os.path.join(DERIVED_DIR, "twi.tif")
HSG_PATH = os.path.join(DATA_DIR, "stormwater", "hydrologic_soil_groups.geojson")
IMPERVIOUS_PATH = os.path.join(DATA_DIR, "impervious", "impervious.tif")
GSI_PATH = os.path.join(DATA_DIR, "validation", "gsi_facilities.geojson")

# Output paths
HSG_RASTER_PATH = os.path.join(DERIVED_DIR, "hsg_raster.tif")
IMP_FRAC_PATH = os.path.join(DERIVED_DIR, "impervious_fraction.tif")
SUIT_PATH = os.path.join(DERIVED_DIR, "fis_suitability.tif")
PRIORITY_PATH = os.path.join(DERIVED_DIR, "fis_priority.tif")
SUIT_ASC_PATH = os.path.join(DERIVED_DIR, "fis_suitability_utm.asc")
PRIORITY_ASC_PATH = os.path.join(DERIVED_DIR, "fis_priority_utm.asc")

# HSG encoding: A=4 (best infiltration) → D=1 (worst)
HSG_MAP = {"A": 4, "B": 3, "C": 2, "D": 1}

# ─── Membership function parameters ──────────────────────────────────────────
# Each is [a, b, c, d] for trapezoidal: ramp up a→b, plateau b→c, ramp down c→d

SLOPE_MF = {
    "flat":     [0.0, 0.0, 0.3, 0.8],
    "ideal":    [0.3, 0.8, 2.0, 3.5],
    "moderate": [2.0, 3.5, 5.0, 8.0],
    "steep":    [5.0, 8.0, 25.0, 25.0],
}

HSG_MF = {
    "poor":      [0.5, 1.0, 1.0, 1.5],   # D
    "marginal":  [1.5, 2.0, 2.0, 2.5],   # C
    "good":      [2.5, 3.0, 3.0, 3.5],   # B
    "excellent": [3.5, 4.0, 4.0, 4.5],   # A
}

SUIT_IN_MF = {
    "low":      [0.0, 0.0, 0.2, 0.35],
    "moderate": [0.2, 0.35, 0.5, 0.65],
    "good":     [0.35, 0.55, 0.7, 0.85],
    "high":     [0.65, 0.8, 1.0, 1.0],
}

IMP_MF = {
    "low":       [0.0, 0.0, 0.15, 0.30],
    "moderate":  [0.15, 0.30, 0.50, 0.65],
    "high":      [0.40, 0.60, 0.80, 0.90],
    "very_high": [0.75, 0.90, 1.0, 1.0],
}

TWI_MF = {
    "low":      [2.0, 2.0, 5.0, 6.0],
    "moderate": [5.0, 6.0, 7.5, 9.0],
    "high":     [7.5, 9.0, 18.0, 18.0],
}

# ─── Rule tables ─────────────────────────────────────────────────────────────
# Stage 1: slope × HSG → suitability centroid
# Row order: flat, ideal, moderate, steep
# Col order: excellent(A), good(B), marginal(C), poor(D)
STAGE1_RULES = [
    # (slope_cat, hsg_cat, output_centroid)
    ("flat",     "excellent", 0.70),
    ("flat",     "good",      0.50),
    ("flat",     "marginal",  0.30),
    ("flat",     "poor",      0.10),
    ("ideal",    "excellent", 0.90),
    ("ideal",    "good",      0.70),
    ("ideal",    "marginal",  0.50),
    ("ideal",    "poor",      0.30),
    ("moderate", "excellent", 0.70),
    ("moderate", "good",      0.50),
    ("moderate", "marginal",  0.30),
    ("moderate", "poor",      0.10),
    ("steep",    "excellent", 0.30),
    ("steep",    "good",      0.10),
    ("steep",    "marginal",  0.10),
    ("steep",    "poor",      0.10),
]

# Stage 2: suitability × impervious × TWI → priority centroid
# Override: suitability=low → very_low (0.10) regardless
STAGE2_RULES = [
    # suitability=low override (all imp × twi combos get very_low)
    ("low", "low",       "low",      0.10),
    ("low", "low",       "moderate", 0.10),
    ("low", "low",       "high",     0.10),
    ("low", "moderate",  "low",      0.10),
    ("low", "moderate",  "moderate", 0.10),
    ("low", "moderate",  "high",     0.10),
    ("low", "high",      "low",      0.10),
    ("low", "high",      "moderate", 0.10),
    ("low", "high",      "high",     0.10),
    ("low", "very_high", "low",      0.10),
    ("low", "very_high", "moderate", 0.10),
    ("low", "very_high", "high",     0.10),
    # suitability=moderate
    ("moderate", "low",       "low",      0.10),
    ("moderate", "low",       "moderate", 0.10),
    ("moderate", "low",       "high",     0.25),
    ("moderate", "moderate",  "low",      0.10),
    ("moderate", "moderate",  "moderate", 0.25),
    ("moderate", "moderate",  "high",     0.25),
    ("moderate", "high",      "low",      0.25),
    ("moderate", "high",      "moderate", 0.25),
    ("moderate", "high",      "high",     0.45),
    ("moderate", "very_high", "low",      0.25),
    ("moderate", "very_high", "moderate", 0.45),
    ("moderate", "very_high", "high",     0.45),
    # suitability=good
    ("good", "low",       "low",      0.10),
    ("good", "low",       "moderate", 0.25),
    ("good", "low",       "high",     0.45),
    ("good", "moderate",  "low",      0.25),
    ("good", "moderate",  "moderate", 0.45),
    ("good", "moderate",  "high",     0.45),
    ("good", "high",      "low",      0.45),
    ("good", "high",      "moderate", 0.45),
    ("good", "high",      "high",     0.70),
    ("good", "very_high", "low",      0.45),
    ("good", "very_high", "moderate", 0.70),
    ("good", "very_high", "high",     0.70),
    # suitability=high
    ("high", "low",       "low",      0.25),
    ("high", "low",       "moderate", 0.25),
    ("high", "low",       "high",     0.45),
    ("high", "moderate",  "low",      0.25),
    ("high", "moderate",  "moderate", 0.45),
    ("high", "moderate",  "high",     0.70),
    ("high", "high",      "low",      0.45),
    ("high", "high",      "moderate", 0.70),
    ("high", "high",      "high",     0.90),
    ("high", "very_high", "low",      0.70),
    ("high", "very_high", "moderate", 0.70),
    ("high", "very_high", "high",     0.90),
]


# ─── Core functions ──────────────────────────────────────────────────────────

def trapmf(x, params):
    """Vectorized trapezoidal membership function.

    params = [a, b, c, d]:
        - 0 for x <= a or x >= d
        - ramp up from a to b
        - 1.0 for b <= x <= c
        - ramp down from c to d
    """
    a, b, c, d = params
    result = np.zeros_like(x, dtype=np.float64)
    # Ramp up: a < x < b
    if b > a:
        mask = (x > a) & (x < b)
        result[mask] = (x[mask] - a) / (b - a)
    # Plateau: b <= x <= c
    result[(x >= b) & (x <= c)] = 1.0
    # Ramp down: c < x < d
    if d > c:
        mask = (x > c) & (x < d)
        result[mask] = (d - x[mask]) / (d - c)
    return result


def box_mean(arr, k):
    """Compute k×k box mean using integral image (summed area table).

    Handles edges by clamping to array bounds. Pure numpy, no scipy.
    """
    rows, cols = arr.shape
    # Summed area table with one row/col of padding
    sat = np.zeros((rows + 1, cols + 1), dtype=np.float64)
    sat[1:, 1:] = np.cumsum(np.cumsum(arr.astype(np.float64), axis=0), axis=1)

    half = k // 2
    # Build coordinate arrays for the four corners of each box
    r = np.arange(rows)
    c = np.arange(cols)
    # Top-left corner (inclusive)
    r1 = np.clip(r - half, 0, rows - 1)
    r2 = np.clip(r + half, 0, rows - 1) + 1  # exclusive in SAT
    c1 = np.clip(c - half, 0, cols - 1)
    c2 = np.clip(c + half, 0, cols - 1) + 1

    # Use outer indexing for 2D lookup
    r1 = r1[:, None]
    r2 = r2[:, None]
    c1 = c1[None, :]
    c2 = c2[None, :]

    box_sum = sat[r2, c2] - sat[r1, c2] - sat[r2, c1] + sat[r1, c1]
    box_count = (r2 - r1) * (c2 - c1)
    return box_sum / box_count


def rasterize_hsg(gt, proj, shape):
    """Rasterize HSG polygons to numeric grid (A=4, B=3, C=2, D=1).

    Uncovered cells default to 1 (HSG D, conservative).
    """
    rows, cols = shape
    print("Rasterizing HSG polygons...")

    # Create output raster in memory
    mem_drv = gdal.GetDriverByName("MEM")
    out_ds = mem_drv.Create("", cols, rows, 1, gdal.GDT_Byte)
    out_ds.SetGeoTransform(gt)
    out_ds.SetProjection(proj)
    band = out_ds.GetRasterBand(1)
    band.Fill(1)  # default D

    # Open HSG vector
    vec_ds = ogr.Open(HSG_PATH)
    vec_lyr = vec_ds.GetLayer()

    # Add numeric field for rasterization
    # We need to create a temporary layer with the numeric HSG value
    mem_vec_drv = ogr.GetDriverByName("MEM")
    tmp_ds = mem_vec_drv.CreateDataSource("")
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(2913)
    tmp_lyr = tmp_ds.CreateLayer("hsg", srs, ogr.wkbPolygon)
    tmp_lyr.CreateField(ogr.FieldDefn("hsg_num", ogr.OFTInteger))

    counts = {v: 0 for v in HSG_MAP.values()}
    for feat in vec_lyr:
        hsg = feat.GetField("HydrolGrp")
        musym = feat.GetField("MUSYM")
        if hsg is None:
            hsg_val = HSG_MAP["D"]  # Urban Land → D
        else:
            hsg_val = HSG_MAP.get(hsg, 1)

        new_feat = ogr.Feature(tmp_lyr.GetLayerDefn())
        new_feat.SetField("hsg_num", hsg_val)
        new_feat.SetGeometry(feat.GetGeometryRef().Clone())
        tmp_lyr.CreateFeature(new_feat)
        counts[hsg_val] += 1

    print(f"  HSG polygons: {dict(counts)}")

    # Rasterize with attribute burn
    gdal.RasterizeLayer(out_ds, [1], tmp_lyr, options=["ATTRIBUTE=hsg_num"])

    hsg_arr = band.ReadAsArray().astype(np.float64)
    out_ds = None
    tmp_ds = None
    vec_ds = None

    # Report cell counts
    for label, val in HSG_MAP.items():
        n = np.sum(hsg_arr == val)
        pct = n / hsg_arr.size * 100
        print(f"  HSG {label} ({val}): {n:,} cells ({pct:.1f}%)")

    return hsg_arr


def evaluate_fis(rules, mf_dicts, inputs, rule_input_keys):
    """Evaluate a FIS over arrays using weighted-average defuzzification.

    Args:
        rules: list of tuples, last element is the output centroid,
               preceding elements are category names for each input.
        mf_dicts: list of dicts mapping category name → MF params [a,b,c,d].
        inputs: list of numpy arrays (one per input variable).
        rule_input_keys: list of lists of category names per input (for pre-computing).

    Returns:
        output array (same shape as inputs).
    """
    shape = inputs[0].shape

    # Pre-compute all membership values
    memberships = []
    for i, (mf_dict, inp) in enumerate(zip(mf_dicts, inputs)):
        mf_vals = {}
        for cat, params in mf_dict.items():
            mf_vals[cat] = trapmf(inp, params)
        memberships.append(mf_vals)

    # Evaluate rules: firing strength = min of all antecedent memberships
    numerator = np.zeros(shape, dtype=np.float64)
    denominator = np.zeros(shape, dtype=np.float64)

    for rule in rules:
        cats = rule[:-1]     # category names for each input
        centroid = rule[-1]  # output value

        # Firing strength = AND (min) of all input memberships
        strength = memberships[0][cats[0]].copy()
        for j in range(1, len(cats)):
            np.minimum(strength, memberships[j][cats[j]], out=strength)

        numerator += strength * centroid
        denominator += strength

    # Avoid division by zero (cells where no rules fire get 0)
    valid = denominator > 0
    output = np.zeros(shape, dtype=np.float64)
    output[valid] = numerator[valid] / denominator[valid]

    return output


def write_raster(path, array, gt, proj, nodata=-9999):
    """Write a single-band Float32 GeoTIFF."""
    driver = gdal.GetDriverByName("GTiff")
    rows, cols = array.shape
    ds = driver.Create(path, cols, rows, 1, gdal.GDT_Float32)
    ds.SetGeoTransform(gt)
    ds.SetProjection(proj)
    band = ds.GetRasterBand(1)
    band.SetNoDataValue(nodata)
    band.WriteArray(array.astype(np.float32))
    band.FlushCache()
    ds = None


def write_ascii_grid_utm(tif_path, asc_path):
    """Reproject a GeoTIFF from EPSG:2913 to EPSG:26910 and write as ASCII grid."""
    print(f"  Reprojecting to UTM ASCII: {os.path.basename(asc_path)}")

    src_ds = gdal.Open(tif_path)
    dst_srs = osr.SpatialReference()
    dst_srs.ImportFromEPSG(26910)

    # Warp to UTM10N with AAIGrid driver
    warp_opts = gdal.WarpOptions(
        format="AAIGrid",
        dstSRS=dst_srs.ExportToWkt(),
        resampleAlg="bilinear",
    )
    gdal.Warp(asc_path, src_ds, options=warp_opts)
    src_ds = None
    print(f"  -> {asc_path}")


def sample_gsi_facilities(raster, gt):
    """Sample a raster at GSI facility centroids. Returns array of values."""
    ds = ogr.Open(GSI_PATH)
    if ds is None:
        return np.array([])
    lyr = ds.GetLayer()

    rows, cols = raster.shape
    vals = []
    for feat in lyr:
        geom = feat.GetGeometryRef()
        centroid = geom.Centroid()
        x, y = centroid.GetX(), centroid.GetY()
        col = int((x - gt[0]) / gt[1])
        row = int((y - gt[3]) / gt[5])
        if 0 <= row < rows and 0 <= col < cols:
            vals.append(raster[row, col])
    ds = None
    return np.array(vals)


def validate_against_gsi(suitability, priority, gt):
    """Statistical validation of FIS outputs against GSI facility locations.

    Tests: Mann-Whitney U, Kolmogorov-Smirnov, AUC-ROC, Boyce Index,
    percentile rank analysis.
    """
    print("\n" + "=" * 65)
    print("STATISTICAL VALIDATION: FIS Priority vs. GSI Facility Locations")
    print("=" * 65)

    fac_suit = sample_gsi_facilities(suitability, gt)
    fac_pri = sample_gsi_facilities(priority, gt)
    if len(fac_pri) == 0:
        print("  WARNING: Cannot open GSI facilities file, skipping validation.")
        return

    bg_vals = priority.ravel()
    n = len(fac_pri)

    # ── 1. Descriptive comparison ────────────────────────────────────────
    print(f"\n1. DESCRIPTIVE STATISTICS")
    print(f"   Background (all {bg_vals.size:,} cells):")
    print(f"     mean={np.mean(bg_vals):.4f}  median={np.median(bg_vals):.4f}"
          f"  std={np.std(bg_vals):.4f}")
    print(f"   Facilities ({n} locations):")
    print(f"     mean={np.mean(fac_pri):.4f}  median={np.median(fac_pri):.4f}"
          f"  std={np.std(fac_pri):.4f}")

    print(f"\n   Suitability: facility mean={np.mean(fac_suit):.4f}"
          f"  background mean={np.mean(suitability):.4f}"
          f"  ratio={np.mean(fac_suit) / np.mean(suitability):.2f}x")

    # ── 2. Mann-Whitney U test ───────────────────────────────────────────
    rng = np.random.default_rng(42)
    bg_sample = rng.choice(bg_vals, size=10000, replace=False)
    u_stat, u_pval = stats.mannwhitneyu(
        fac_pri, bg_sample, alternative="greater"
    )
    n1, n2 = len(fac_pri), len(bg_sample)
    rank_biserial = 2 * u_stat / (n1 * n2) - 1

    print(f"\n2. MANN-WHITNEY U TEST")
    print(f"   H0: facility priorities = background priorities")
    print(f"   Ha: facility priorities > background priorities")
    print(f"   U = {u_stat:,.0f},  p = {u_pval:.2e}")
    print(f"   Rank-biserial r = {rank_biserial:.3f}")
    sig = "REJECT H0" if u_pval < 0.01 else "fail to reject"
    print(f"   Interpretation: {sig} at alpha=0.01")
    print(f"   (r: 0.1=small, 0.3=medium, 0.5=large effect)")

    # ── 3. Kolmogorov-Smirnov test ───────────────────────────────────────
    ks_stat, ks_pval = stats.ks_2samp(fac_pri, bg_sample, alternative="less")

    print(f"\n3. KOLMOGOROV-SMIRNOV TEST")
    print(f"   H0: facility and background CDFs are identical")
    print(f"   Ha: facility CDF shifted right (higher values)")
    print(f"   D = {ks_stat:.4f},  p = {ks_pval:.2e}")
    sig = "REJECT H0" if ks_pval < 0.01 else "fail to reject"
    print(f"   Interpretation: {sig} at alpha=0.01")

    # ── 4. AUC-ROC ──────────────────────────────────────────────────────
    n_pos = len(fac_pri)
    bg_neg = rng.choice(bg_vals, size=n_pos, replace=False)
    labels = np.concatenate([np.ones(n_pos), np.zeros(n_pos)])
    scores = np.concatenate([fac_pri, bg_neg])

    order = np.argsort(-scores)
    labels_sorted = labels[order]
    tpr = np.cumsum(labels_sorted) / n_pos
    fpr = np.cumsum(1 - labels_sorted) / n_pos
    tpr = np.concatenate([[0], tpr])
    fpr = np.concatenate([[0], fpr])
    auc = np.trapezoid(tpr, fpr)

    print(f"\n4. AUC-ROC (Area Under ROC Curve)")
    print(f"   Positive: {n_pos} facility locations")
    print(f"   Negative: {n_pos} random background cells")
    print(f"   AUC = {auc:.3f}")
    print(f"   Interpretation: 0.5=random, 0.7=acceptable, 0.8=good, 0.9=excellent")

    # ── 5. Boyce Index (continuous) ──────────────────────────────────────
    n_bins = 10
    bin_edges = np.linspace(priority.min(), priority.max(), n_bins + 1)
    bin_mids = (bin_edges[:-1] + bin_edges[1:]) / 2

    pe_ratios = []
    for i in range(n_bins):
        lo, hi = bin_edges[i], bin_edges[i + 1]
        include_upper = i == n_bins - 1
        if include_upper:
            bg_frac = np.mean((bg_vals >= lo) & (bg_vals <= hi))
            fac_frac = np.mean((fac_pri >= lo) & (fac_pri <= hi))
        else:
            bg_frac = np.mean((bg_vals >= lo) & (bg_vals < hi))
            fac_frac = np.mean((fac_pri >= lo) & (fac_pri < hi))
        pe_ratios.append(fac_frac / bg_frac if bg_frac > 0 else np.nan)

    pe_ratios = np.array(pe_ratios)
    valid = ~np.isnan(pe_ratios)
    boyce_r, boyce_p = stats.spearmanr(bin_mids[valid], pe_ratios[valid])

    print(f"\n5. CONTINUOUS BOYCE INDEX")
    print(f"   Spearman correlation between priority bins and P/E ratio")
    print(f"   Boyce index (B) = {boyce_r:.3f}  (p = {boyce_p:.4f})")
    print(f"   Interpretation: B>0 = facilities prefer higher-priority areas")
    print(f"                   B=1 = perfect monotonic, B=0 = random")
    print(f"\n   Bin         Expected   Observed   P/E ratio")
    for i in range(n_bins):
        lo, hi = bin_edges[i], bin_edges[i + 1]
        include_upper = i == n_bins - 1
        if include_upper:
            bg_n = np.sum((bg_vals >= lo) & (bg_vals <= hi))
            fac_n = np.sum((fac_pri >= lo) & (fac_pri <= hi))
        else:
            bg_n = np.sum((bg_vals >= lo) & (bg_vals < hi))
            fac_n = np.sum((fac_pri >= lo) & (fac_pri < hi))
        pe = pe_ratios[i]
        pe_str = f"{pe:.2f}" if not np.isnan(pe) else "  - "
        bar = "#" * min(int(pe * 10), 40) if not np.isnan(pe) else ""
        print(f"   {lo:.2f}-{hi:.2f}  {bg_n:>9,}   {fac_n:>4}       {pe_str:>5}  {bar}")

    # ── 6. Percentile rank ───────────────────────────────────────────────
    fac_pctiles = np.array(
        [stats.percentileofscore(bg_sample, v) for v in fac_pri]
    )
    print(f"\n6. PERCENTILE RANK OF FACILITIES")
    print(f"   Mean percentile:   {np.mean(fac_pctiles):.1f}th")
    print(f"   Median percentile: {np.median(fac_pctiles):.1f}th")
    print(f"   (50th expected if random placement)")

    # Top-quartile enrichment
    p75 = np.percentile(priority, 75)
    fac_in_top_q = np.sum(fac_pri >= p75)
    pct_top_q = fac_in_top_q / n * 100
    print(f"\n   Top quartile (>= {p75:.3f}): {fac_in_top_q}/{n}"
          f" ({pct_top_q:.1f}%, expected 25%)")

    print(f"\n{'=' * 65}")
    print(f"SUMMARY")
    print(f"  AUC-ROC:         {auc:.3f}")
    print(f"  Mann-Whitney:    p = {u_pval:.2e}  (effect r = {rank_biserial:.3f})")
    print(f"  Boyce Index:     B = {boyce_r:.3f}  (p = {boyce_p:.4f})")
    print(f"  Mean percentile: {np.mean(fac_pctiles):.0f}th")
    print(f"{'=' * 65}")


def main():
    os.makedirs(DERIVED_DIR, exist_ok=True)

    # ── Load reference raster for grid alignment ─────────────────────────────
    print("Loading slope raster (reference grid)...")
    slope_ds = gdal.Open(SLOPE_PATH)
    slope = slope_ds.GetRasterBand(1).ReadAsArray().astype(np.float64)
    gt = slope_ds.GetGeoTransform()
    proj = slope_ds.GetProjection()
    shape = slope.shape
    slope_ds = None
    print(f"  Grid: {shape[1]}x{shape[0]}, pixel={gt[1]}ft")
    print(f"  Slope range: {slope.min():.2f} – {slope.max():.2f} degrees")

    # ── Load TWI ─────────────────────────────────────────────────────────────
    print("Loading TWI...")
    twi_ds = gdal.Open(TWI_PATH)
    twi = twi_ds.GetRasterBand(1).ReadAsArray().astype(np.float64)
    twi_ds = None
    print(f"  TWI range: {twi.min():.2f} – {twi.max():.2f}")

    # ── Step 1: Rasterize HSG ────────────────────────────────────────────────
    hsg = rasterize_hsg(gt, proj, shape)
    write_raster(HSG_RASTER_PATH, hsg, gt, proj)
    print(f"  -> {HSG_RASTER_PATH}")

    # ── Step 2: Compute impervious neighborhood fraction ─────────────────────
    print("\nComputing impervious neighborhood fraction (11×11 box mean)...")
    imp_ds = gdal.Open(IMPERVIOUS_PATH)
    imp_raw = imp_ds.GetRasterBand(1).ReadAsArray().astype(np.float64)
    imp_ds = None
    imp_frac = box_mean(imp_raw, 11)
    print(f"  Raw impervious: {imp_raw.mean():.3f} mean")
    print(f"  Fraction range: {imp_frac.min():.3f} – {imp_frac.max():.3f}")
    print(f"  Fraction mean:  {imp_frac.mean():.3f}")
    print(f"  Fraction median: {np.median(imp_frac):.3f}")
    write_raster(IMP_FRAC_PATH, imp_frac, gt, proj)
    print(f"  -> {IMP_FRAC_PATH}")

    # ── Stage 1: Physical Suitability FIS ────────────────────────────────────
    print("\n=== Stage 1: Physical Suitability (slope × HSG) ===")
    suitability = evaluate_fis(
        rules=STAGE1_RULES,
        mf_dicts=[SLOPE_MF, HSG_MF],
        inputs=[slope, hsg],
        rule_input_keys=None,
    )
    print(f"  Suitability range: {suitability.min():.3f} – {suitability.max():.3f}")
    print(f"  Suitability mean:  {suitability.mean():.3f}")
    print(f"  Suitability median: {np.median(suitability):.3f}")
    write_raster(SUIT_PATH, suitability, gt, proj)
    print(f"  -> {SUIT_PATH}")

    # ── Stage 2: Capture Priority FIS ────────────────────────────────────────
    print("\n=== Stage 2: Capture Priority (suitability × impervious × TWI) ===")
    priority = evaluate_fis(
        rules=STAGE2_RULES,
        mf_dicts=[SUIT_IN_MF, IMP_MF, TWI_MF],
        inputs=[suitability, imp_frac, twi],
        rule_input_keys=None,
    )
    print(f"  Priority range:  {priority.min():.3f} – {priority.max():.3f}")
    print(f"  Priority mean:   {priority.mean():.3f}")
    print(f"  Priority median: {np.median(priority):.3f}")
    write_raster(PRIORITY_PATH, priority, gt, proj)
    print(f"  -> {PRIORITY_PATH}")

    # ── ASCII grids for NetLogo (EPSG:26910) ─────────────────────────────────
    print("\nGenerating ASCII grids for NetLogo (EPSG:26910)...")
    write_ascii_grid_utm(SUIT_PATH, SUIT_ASC_PATH)
    write_ascii_grid_utm(PRIORITY_PATH, PRIORITY_ASC_PATH)

    # ── Validation ───────────────────────────────────────────────────────────
    validate_against_gsi(suitability, priority, gt)

    print("\nDone.")


if __name__ == "__main__":
    main()
