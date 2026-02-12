# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
# ABOUTME: Unzips NOAA C-CAP Oregon impervious raster, reprojects to EPSG:2913,
# ABOUTME: and clips to the canonical study area extent. Output is a 1m binary raster.

import glob
import os
import subprocess
import zipfile

# Canonical study area extent in EPSG:2913 (Oregon North State Plane, ft).
# Same source of truth as clip_dem.py.
STUDY_EXTENT_2913 = {
    "xmin": 7650146,
    "ymin": 675893,
    "xmax": 7658210,
    "ymax": 680660,
}

TARGET_CRS = "EPSG:2913"
PIXEL_SIZE = 3  # feet — match DEM resolution

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
IMPERV_DIR = os.path.join(DATA_DIR, "impervious")
ZIP_FILE = os.path.join(IMPERV_DIR, "or_2021_ccap_v2_hires_impervious_20231024.zip")
OUTPUT_TIF = os.path.join(IMPERV_DIR, "impervious.tif")
AUX_XML = OUTPUT_TIF + ".aux.xml"


def find_source_tif():
    """Find the .tif inside the zip (unzipping if needed)."""
    # Look for already-unzipped tifs
    tifs = glob.glob(os.path.join(IMPERV_DIR, "or_*impervious*.tif"))
    if tifs:
        return tifs[0]

    # Unzip
    if not os.path.exists(ZIP_FILE):
        print(f"Zip file not found: {ZIP_FILE}")
        print("Download from: https://coastalimagery.blob.core.windows.net/ccap-landcover/"
              "CCAP_bulk_download/High_Resolution_Land_Cover/Phase_1_Initial_Layers/"
              "Impervious/or_2021_ccap_v2_hires_impervious_20231024.zip")
        return None

    print(f"Unzipping {os.path.basename(ZIP_FILE)}...")
    with zipfile.ZipFile(ZIP_FILE, "r") as zf:
        tif_names = [n for n in zf.namelist() if n.endswith(".tif")]
        if not tif_names:
            print("No .tif found in zip file")
            return None
        for name in tif_names:
            zf.extract(name, IMPERV_DIR)
            print(f"  Extracted: {name}")

    tifs = glob.glob(os.path.join(IMPERV_DIR, "or_*impervious*.tif"))
    return tifs[0] if tifs else None


def main():
    source_tif = find_source_tif()
    if not source_tif:
        return

    print(f"Source: {os.path.basename(source_tif)}")

    # Check source CRS
    result = subprocess.run(
        ["gdalinfo", source_tif],
        capture_output=True, text=True, check=True,
    )
    for line in result.stdout.splitlines():
        if any(k in line for k in ["Size is", "AUTHORITY", "Pixel Size", "Type="]):
            print(f"  {line.strip()}")

    # Remove stale stats cache
    if os.path.exists(AUX_XML):
        os.remove(AUX_XML)

    # Reproject and clip to study area in one pass
    ext = STUDY_EXTENT_2913
    subprocess.run(
        [
            "gdalwarp",
            "-t_srs", TARGET_CRS,
            "-te", str(ext["xmin"]), str(ext["ymin"]), str(ext["xmax"]), str(ext["ymax"]),
            "-tr", str(PIXEL_SIZE), str(PIXEL_SIZE),
            "-r", "near",  # nearest neighbor — preserves binary classification
            "-overwrite",
            source_tif,
            OUTPUT_TIF,
        ],
        check=True,
    )

    # Print summary
    result = subprocess.run(
        ["gdalinfo", "-stats", OUTPUT_TIF],
        capture_output=True, text=True, check=True,
    )
    for line in result.stdout.splitlines():
        if any(k in line for k in ["Size is", "STATISTICS_", "Upper Left", "Lower Right", "Type="]):
            print(line.strip())

    print(f"\nSaved to {OUTPUT_TIF} ({TARGET_CRS}, {PIXEL_SIZE}ft pixels)")


if __name__ == "__main__":
    main()
