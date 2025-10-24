#!/usr/bin/env python3
import numpy as np
import rasterio
from PIL import Image, ImageFile

# 🧩 Allow large images
Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

DEM_PATH = "../../DATA/DEM_prep/dem_smooth.tif"
HS_PATH = "../../DATA/DEM_prep/hillshade.png"
OUT_RELIEF = "../../DATA/DEM_prep/white_relief.png"

with rasterio.open(DEM_PATH) as src:
    dem = src.read(1).astype(np.float32)

# ✅ Allow Pillow to open huge images
hillshade = np.array(Image.open(HS_PATH).convert("L")).astype(np.float32) / 255.0
elev_norm = (dem - np.nanmin(dem)) / (np.nanmax(dem) - np.nanmin(dem))

# combine hillshade + elevation
relief = 0.6 * hillshade + 0.4 * elev_norm
relief = np.clip(relief, 0, 1)
img = (relief * 255).astype("uint8")

Image.fromarray(np.dstack([img, img, img])).save(OUT_RELIEF)
print(f"✅ White shaded relief saved as {OUT_RELIEF}")
