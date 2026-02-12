# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "gdal"]
# ///
# ABOUTME: Computes slope, D8 flow direction, flow accumulation, and TWI from DEM.
# ABOUTME: Outputs are GeoTIFFs in EPSG:2913, aligned to the study area DEM grid.

import os
import numpy as np
from osgeo import gdal, osr

# Match the canonical study area DEM
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
DEM_PATH = os.path.join(DATA_DIR, "dem", "study_area_dem.tif")
DERIVED_DIR = os.path.join(DATA_DIR, "derived")

# D8 neighbor offsets: (row_offset, col_offset) for 8 directions
# Order: E, SE, S, SW, W, NW, N, NE
D8_OFFSETS = [
    (0, 1), (1, 1), (1, 0), (1, -1),
    (0, -1), (-1, -1), (-1, 0), (-1, 1),
]
# Distance weights: 1 for cardinal, sqrt(2) for diagonal
D8_DISTANCES = [1.0, np.sqrt(2), 1.0, np.sqrt(2),
                1.0, np.sqrt(2), 1.0, np.sqrt(2)]


def read_dem():
    """Read DEM and return elevation array, geotransform, projection."""
    ds = gdal.Open(DEM_PATH)
    if ds is None:
        raise FileNotFoundError(f"Cannot open {DEM_PATH}")
    band = ds.GetRasterBand(1)
    elev = band.ReadAsArray().astype(np.float64)
    nodata = band.GetNoDataValue()
    gt = ds.GetGeoTransform()
    proj = ds.GetProjection()
    pixel_size = gt[1]  # feet
    print(f"DEM: {elev.shape[1]}x{elev.shape[0]}, pixel={pixel_size}ft")
    print(f"  Elevation range: {np.nanmin(elev):.1f} – {np.nanmax(elev):.1f} ft")
    ds = None
    return elev, gt, proj, pixel_size, nodata


def write_raster(path, array, gt, proj, nodata=-9999, dtype=gdal.GDT_Float32):
    """Write a numpy array as a single-band GeoTIFF."""
    driver = gdal.GetDriverByName("GTiff")
    rows, cols = array.shape
    ds = driver.Create(path, cols, rows, 1, dtype)
    ds.SetGeoTransform(gt)
    ds.SetProjection(proj)
    band = ds.GetRasterBand(1)
    band.SetNoDataValue(nodata)
    band.WriteArray(array)
    band.FlushCache()
    ds = None


def calc_slope(elev, pixel_size):
    """Compute slope in degrees using numpy gradient (Horn's method approx)."""
    # np.gradient computes central differences, returns (dz/dy, dz/dx)
    dz_dy, dz_dx = np.gradient(elev, pixel_size)
    slope_rad = np.arctan(np.sqrt(dz_dx**2 + dz_dy**2))
    slope_deg = np.degrees(slope_rad)
    print(f"  Slope range: {slope_deg.min():.2f} – {slope_deg.max():.2f} degrees")
    return slope_deg, slope_rad


def calc_d8_flow_direction(elev, pixel_size):
    """Compute D8 flow direction. Returns direction index (0-7) or -1 for sinks."""
    rows, cols = elev.shape
    flow_dir = np.full((rows, cols), -1, dtype=np.int8)

    for r in range(rows):
        for c in range(cols):
            max_slope = 0.0
            best_dir = -1
            for d, (dr, dc) in enumerate(D8_OFFSETS):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    drop = elev[r, c] - elev[nr, nc]
                    if drop > 0:
                        slope = drop / (pixel_size * D8_DISTANCES[d])
                        if slope > max_slope:
                            max_slope = slope
                            best_dir = d
            flow_dir[r, c] = best_dir

    n_sinks = np.sum(flow_dir == -1)
    print(f"  Sinks (no downhill neighbor): {n_sinks} ({n_sinks / flow_dir.size * 100:.1f}%)")
    return flow_dir


def calc_flow_accumulation(elev, flow_dir):
    """Compute flow accumulation by processing cells from highest to lowest."""
    rows, cols = elev.shape
    accum = np.ones((rows, cols), dtype=np.float64)  # each cell contributes 1

    # Sort cells by elevation, highest first
    flat_indices = np.argsort(elev, axis=None)[::-1]

    for idx in flat_indices:
        r, c = divmod(idx, cols)
        d = flow_dir[r, c]
        if d >= 0:
            dr, dc = D8_OFFSETS[d]
            nr, nc = r + dr, c + dc
            accum[nr, nc] += accum[r, c]

    print(f"  Flow accumulation range: {accum.min():.0f} – {accum.max():.0f} cells")
    return accum


def calc_twi(accum, slope_rad, pixel_size):
    """Compute Topographic Wetness Index: TWI = ln(a / tan(b)).

    a = specific catchment area (upslope area per unit contour length)
    b = local slope in radians
    """
    # Specific catchment area: flow_accum * cell_area / contour_length
    # For a square grid, contour_length ≈ pixel_size
    cell_area = pixel_size * pixel_size
    specific_area = accum * cell_area / pixel_size  # ft

    # Clamp slope to avoid division by zero (flat areas get high TWI)
    tan_slope = np.tan(slope_rad)
    tan_slope = np.maximum(tan_slope, 0.001)

    twi = np.log(specific_area / tan_slope)
    print(f"  TWI range: {twi.min():.2f} – {twi.max():.2f}")
    return twi


def main():
    os.makedirs(DERIVED_DIR, exist_ok=True)

    print("Reading DEM...")
    elev, gt, proj, pixel_size, nodata = read_dem()

    print("Computing slope...")
    slope_deg, slope_rad = calc_slope(elev, pixel_size)
    slope_path = os.path.join(DERIVED_DIR, "slope.tif")
    write_raster(slope_path, slope_deg.astype(np.float32), gt, proj)
    print(f"  -> {slope_path}")

    print("Computing D8 flow direction...")
    flow_dir = calc_d8_flow_direction(elev, pixel_size)
    fdir_path = os.path.join(DERIVED_DIR, "flow_direction.tif")
    write_raster(fdir_path, flow_dir.astype(np.float32), gt, proj, nodata=-1)
    print(f"  -> {fdir_path}")

    print("Computing flow accumulation...")
    accum = calc_flow_accumulation(elev, flow_dir)
    accum_path = os.path.join(DERIVED_DIR, "flow_accumulation.tif")
    write_raster(accum_path, accum.astype(np.float32), gt, proj)
    print(f"  -> {accum_path}")

    print("Computing TWI...")
    twi = calc_twi(accum, slope_rad, pixel_size)
    twi_path = os.path.join(DERIVED_DIR, "twi.tif")
    write_raster(twi_path, twi.astype(np.float32), gt, proj)
    print(f"  -> {twi_path}")

    print("\nDone. All outputs in EPSG:2913, matching DEM grid.")


if __name__ == "__main__":
    main()
