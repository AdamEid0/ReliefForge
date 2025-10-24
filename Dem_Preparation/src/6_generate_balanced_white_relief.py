#!/usr/bin/env python3
"""
Balanced white relief map:
 - Mostly white plains
 - Gradual grayscale shading for hills/mountains
"""

import numpy as np
import rasterio
from scipy.ndimage import gaussian_filter
from PIL import Image, ImageFile

# 🧩 Allow large images
Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

DEM_PATH = "../Data/DEM_prep/SRTM_90m_Riyadh.tif"
OUT_PATH = "../Data/DEM_prep/arabia_balanced_white_relief.png"

# -----------------------------
# 1️⃣ Load DEM
# -----------------------------
with rasterio.open(DEM_PATH) as src:
    dem = src.read(1).astype(np.float32)
    transform = src.transform
    dem[dem == src.nodata] = np.nan

print("📘 DEM loaded:", dem.shape)

# -----------------------------
# 2️⃣ Smooth DEM
# -----------------------------
dem_s = gaussian_filter(np.nan_to_num(dem, nan=np.nanmean(dem)), sigma=2)

# -----------------------------
# 3️⃣ Normalize elevation
# -----------------------------
elev_norm = (dem_s - np.nanmin(dem_s)) / (np.nanmax(dem_s) - np.nanmin(dem_s))

# -----------------------------
# 4️⃣ Apply gentle contrast curve
#     - Amplifies mid-high elevations
# -----------------------------
contrast = np.power(elev_norm, 0.6)   # <1 brightens midtones
contrast = (contrast - np.min(contrast)) / (np.max(contrast) - np.min(contrast))

# -----------------------------
# 5️⃣ Compute hillshade
# -----------------------------
cellsize = abs(transform.a)
dzdx = np.gradient(dem_s, axis=1) / cellsize
dzdy = np.gradient(dem_s, axis=0) / cellsize
az = np.deg2rad(315)
alt = np.deg2rad(45)
slope = np.arctan(np.sqrt(dzdx**2 + dzdy**2))
aspect = np.arctan2(-dzdy, dzdx)
hs = np.sin(alt)*np.cos(slope) + np.cos(alt)*np.sin(slope)*np.cos(az - aspect)
hs = np.clip(hs, 0, 1)

# -----------------------------
# 6️⃣ Blend hillshade + contrast
# -----------------------------
relief = 0.7 * hs + 0.3 * contrast
relief = np.clip(relief, 0, 1)

# -----------------------------
# 7️⃣ Map to white-based grayscale
# -----------------------------
# invert + brighten to keep mostly white
white_relief = 1.0 - 0.6 * (1 - relief)
white_relief = np.clip(white_relief, 0, 1)

img = (white_relief * 255).astype(np.uint8)
img_rgb = np.dstack([img, img, img])

Image.fromarray(img_rgb).save(OUT_PATH)
print(f"✅ Balanced white relief saved as {OUT_PATH}")
