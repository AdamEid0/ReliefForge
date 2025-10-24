#!/usr/bin/env python3
import rasterio
import numpy as np

DEM_PATH = "../Data/DEM_prep/SRTM_90m_Riyadh.tif"

with rasterio.open(DEM_PATH) as src:
    dem = src.read(1).astype(np.float32)
    transform = src.transform
    nodata = src.nodata

dem[dem == nodata] = np.nan

print("📘 DEM Info")
print("  Shape:", dem.shape)
print("  CRS:", src.crs)
print("  Bounds:", src.bounds)
print("  Elevation stats:")
print("   Min:", np.nanmin(dem))
print("   Max:", np.nanmax(dem))
print("   Mean:", np.nanmean(dem))
