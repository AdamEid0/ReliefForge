"""
Download and clip SRTM 90m DEM using an AOI shapefile.

This script downloads a 90-meter resolution DEM (SRTMGL3) from
OpenTopography and clips it to a user-defined Area of Interest (AOI)
provided as a shapefile.

Requirements:
    - geopandas
    - rasterio
    - shapely
    - requests
    - API_Key.txt (in project root)

Author: <Adam Eid>
"""

# ============================================================
# 🧩 USER INPUTS (edit these only)
# ============================================================

SHAPEFILE_PATH = "../../DATA/shapefiles/sa.shp"      # AOI shapefile path
OUTPUT_DEM_PATH = "../../DATA/DEM_prep/SRTM_90m_DEM.tif"  # Output DEM file
DEM_TYPE = "SRTMGL3"                                 # DEM type (90m)
TEMP_FILE = "temp_90m.tif"                           # Temporary local file
API_KEY_FILE = "../../API_Key.txt"                   # Path to API_Key.txt

# ============================================================
# 🚀 SCRIPT STARTS HERE (no need to edit below)
# ============================================================

import os
import requests
import geopandas as gpd
import rasterio
from rasterio.mask import mask


def read_api_key(filepath):
    """
    Reads the API key from API_Key.txt.
    Ignores commented lines (# ...) and returns the first non-empty key.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"API key file not found at: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                return line

    raise ValueError("API_Key.txt found, but no valid API key detected.")


def main():
    # Resolve paths relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    shapefile = os.path.join(script_dir, SHAPEFILE_PATH)
    out_dem = os.path.join(script_dir, OUTPUT_DEM_PATH)
    api_file = os.path.join(script_dir, API_KEY_FILE)
    temp_file = os.path.join(script_dir, TEMP_FILE)

    # Load API key
    API_KEY = read_api_key(api_file)

    # Read shapefile and compute bounding box
    gdf = gpd.read_file(shapefile)
    bounds = gdf.total_bounds  # (minx, miny, maxx, maxy)

    # Construct API URL
    url = (
        "https://portal.opentopography.org/API/globaldem"
        f"?demtype={DEM_TYPE}&south={bounds[1]}&north={bounds[3]}"
        f"&west={bounds[0]}&east={bounds[2]}&outputFormat=GTiff"
        f"&API_Key={API_KEY}"
    )

    print("🔄 Downloading SRTM 90m DEM from OpenTopography...")
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        raise RuntimeError(f"API request failed: {response.text}")

    with open(temp_file, "wb") as f:
        f.write(response.content)

    print("✅ DEM downloaded. Clipping to AOI...")

    # Clip DEM to AOI
    with rasterio.open(temp_file) as src:
        out_image, out_transform = mask(src, gdf.geometry, crop=True)
        out_meta = src.meta.copy()

    out_meta.update({
        "driver": "GTiff",
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })

    os.makedirs(os.path.dirname(out_dem), exist_ok=True)
    with rasterio.open(out_dem, "w", **out_meta) as dest:
        dest.write(out_image)

    os.remove(temp_file)
    print(f"✅ Finished! DEM saved to: {out_dem}")


if __name__ == "__main__":
    main()
