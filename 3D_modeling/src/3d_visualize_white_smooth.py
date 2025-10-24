#!/usr/bin/env python3
import rasterio
import numpy as np
import pyvista as pv
from scipy.ndimage import gaussian_filter

# -----------------------------
# SETTINGS
# -----------------------------
DEM_PATH = "../../DATA/3D_prep/SRTM_90m_Riyadh_UTM.tif"
EXAGGERATION = 10.0
MAX_POINTS = 1_500_000
SMOOTH_SIGMA = 2.5   # ↑ increase to 2–3 for stronger smoothing
# -----------------------------

# 1️⃣ Load DEM
with rasterio.open(DEM_PATH) as src:
    dem = src.read(1).astype(np.float32)
    transform = src.transform

dem = np.nan_to_num(dem, nan=np.nanmean(dem))

# 2️⃣ Smooth small spikes
dem_smooth = gaussian_filter(dem, sigma=SMOOTH_SIGMA)

# 3️⃣ Downsample for performance
nrows, ncols = dem_smooth.shape
total_points = nrows * ncols
factor = max(1, int(np.ceil(np.sqrt(total_points / MAX_POINTS))))
dem_ds = dem_smooth[::factor, ::factor]

nrows_ds, ncols_ds = dem_ds.shape
print(f"✅ Downsampled to {ncols_ds}x{nrows_ds} (factor {factor}) | Smoothed σ={SMOOTH_SIGMA}")

# 4️⃣ Build coordinate grid
x = np.arange(ncols_ds) * transform.a * factor + transform.c
y = np.arange(nrows_ds) * transform.e * factor + transform.f
x, y = np.meshgrid(x, y)
z = dem_ds * EXAGGERATION

grid = pv.StructuredGrid(x, y, z)

# 5️⃣ Visualize matte white
p = pv.Plotter(window_size=[1600, 1000])
p.set_background("black")

p.add_mesh(
    grid,
    color="white",
    smooth_shading=False,  # keeps matte look
    lighting=False,        # removes reflections
    show_edges=False,
)

# Optional: soft ambient enhancement
p.enable_eye_dome_lighting()

# Camera setup
p.camera_position = [
    (x.max()*1.2, y.max()*1.2, z.max()*3),
    (x.mean(), y.mean(), z.mean()),
    (0, 0, 1)
]

print("⚪ Matte white terrain with smoothed DEM — no spikes, no reflections.")
p.show()
