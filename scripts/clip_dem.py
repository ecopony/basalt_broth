# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
# ABOUTME: Mosaics USGS 3DEP source tiles, reprojects UTM→EPSG:2913, and clips
# ABOUTME: to the canonical study area extent. No WGS84 in the pipeline.

import glob
import os
import subprocess

# Canonical study area extent in EPSG:2913 (Oregon North State Plane, ft).
# This is the single source of truth for the study area boundary.
STUDY_EXTENT_2913 = {
    "xmin": 7650146,
    "ymin": 675893,
    "xmax": 7658210,
    "ymax": 680660,
}

TARGET_CRS = "EPSG:2913"
PIXEL_SIZE = 3  # feet

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
DEM_DIR = os.path.join(DATA_DIR, "dem")
OUTPUT_DEM = os.path.join(DEM_DIR, "study_area_dem.tif")
AUX_XML = OUTPUT_DEM + ".aux.xml"


def main():
    # Find all USGS source tiles
    tiles = sorted(glob.glob(os.path.join(DEM_DIR, "USGS_1M_*.tif")))
    if not tiles:
        print(f"No USGS source tiles found in {DEM_DIR}")
        return

    print(f"Source tiles ({len(tiles)}):")
    for t in tiles:
        print(f"  {os.path.basename(t)}")

    # Remove stale stats cache
    if os.path.exists(AUX_XML):
        os.remove(AUX_XML)

    # gdalwarp handles mosaicking multiple inputs, reprojection, and clipping
    # in one pass: UTM source tiles → EPSG:2913 clipped to study area.
    ext = STUDY_EXTENT_2913
    subprocess.run(
        [
            "gdalwarp",
            "-t_srs", TARGET_CRS,
            "-te", str(ext["xmin"]), str(ext["ymin"]), str(ext["xmax"]), str(ext["ymax"]),
            "-tr", str(PIXEL_SIZE), str(PIXEL_SIZE),
            "-r", "bilinear",
            "-overwrite",
            *tiles,
            OUTPUT_DEM,
        ],
        check=True,
    )

    # Print summary
    result = subprocess.run(
        ["gdalinfo", "-stats", OUTPUT_DEM],
        capture_output=True, text=True, check=True,
    )
    for line in result.stdout.splitlines():
        if any(k in line for k in ["Size is", "STATISTICS_", "Upper Left", "Lower Right"]):
            print(line.strip())

    print(f"\nSaved to {OUTPUT_DEM} ({TARGET_CRS}, {PIXEL_SIZE}ft pixels)")


if __name__ == "__main__":
    main()
