#!/usr/bin/env python3
import numpy as np
import rasterio
from PIL import Image

DEM_PATH = "../Data/DEM_prep/dem_smooth.tif"
OUT_HS = "../Data/DEM_prep/hillshade.png"
AZIMUTH = 315
ALTITUDE = 45

with rasterio.open(DEM_PATH) as src:
    dem = src.read(1).astype(np.float32)
    transform = src.transform

cellsize = abs(transform.a)
dzdx = np.gradient(dem, axis=1) / cellsize
dzdy = np.gradient(dem, axis=0) / cellsize

az = np.deg2rad(90.0 - AZIMUTH)
alt = np.deg2rad(ALTITUDE)
slope = np.arctan(np.sqrt(dzdx**2 + dzdy**2))
aspect = np.arctan2(-dzdy, dzdx)
hs = np.sin(alt)*np.cos(slope) + np.cos(alt)*np.sin(slope)*np.cos(az - aspect)
hillshade = np.clip(hs, 0, 1)

Image.fromarray((hillshade * 255).astype("uint8")).save(OUT_HS)
print(f"✅ Hillshade saved as {OUT_HS}")
