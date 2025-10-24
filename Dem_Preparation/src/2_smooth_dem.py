#!/usr/bin/env python3
import numpy as np
import rasterio
from scipy.ndimage import gaussian_filter

DEM_PATH = "../../DATA/DEM_prep/SRTM_90m_Riyadh.tif"
OUT_PATH = "../../DATA/DEM_prep/dem_smooth.tif"
SIGMA = 2.0  # control smoothing level

with rasterio.open(DEM_PATH) as src:
    dem = src.read(1).astype(np.float32)
    profile = src.profile
    dem[dem == src.nodata] = np.nan

print("🌀 Applying Gaussian smoothing...")
dem_smooth = gaussian_filter(np.nan_to_num(dem, nan=np.nanmean(dem)), sigma=SIGMA)

profile.update(dtype=rasterio.float32, nodata=np.nan)
with rasterio.open(OUT_PATH, "w", **profile) as dst:
    dst.write(dem_smooth, 1)

print(f"✅ Smoothed DEM saved as {OUT_PATH}")
