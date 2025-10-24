#!/usr/bin/env python3
import rasterio
import numpy as np
import pyvista as pv
from scipy.ndimage import gaussian_filter
from matplotlib.colors import LinearSegmentedColormap

# -----------------------------
# SETTINGS
# -----------------------------
DEM_PATH = "../../DATA/3D_prep/SRTM_90m_Riyadh_UTM.tif"
EXAGGERATION = 12.0
MAX_POINTS = 1_300_000
SMOOTH_SIGMA = 2.5     # 1.0–3.0 for smoothing intensity
# -----------------------------

# 1️⃣ Load DEM
with rasterio.open(DEM_PATH) as src:
    dem = src.read(1).astype(np.float32)
    transform = src.transform

# Fill gaps
dem = np.nan_to_num(dem, nan=np.nanmean(dem))

# 2️⃣ Smooth terrain
if SMOOTH_SIGMA > 0:
    dem = gaussian_filter(dem, sigma=SMOOTH_SIGMA)
    print(f"✅ Smoothed DEM with σ={SMOOTH_SIGMA}")

# 3️⃣ Downsample
nrows, ncols = dem.shape
total_points = nrows * ncols
factor = max(1, int(np.ceil(np.sqrt(total_points / MAX_POINTS))))
dem_ds = dem[::factor, ::factor]
print(f"✅ Downsampled to {dem_ds.shape[1]}x{dem_ds.shape[0]} (factor {factor})")

# 4️⃣ Build coordinates
x = np.arange(dem_ds.shape[1]) * transform.a * factor + transform.c
y = np.arange(dem_ds.shape[0]) * transform.e * factor + transform.f
x, y = np.meshgrid(x, y)
z = dem_ds * EXAGGERATION

grid = pv.StructuredGrid(x, y, z)

# 5️⃣ Elevation normalization
z_norm = (z - z.min()) / (z.max() - z.min())
grid["elevation"] = z_norm.ravel(order="F")

# 6️⃣ Brown–Yellow colormap (medium to dark brown at top)
colors = [
    (0.96, 0.85, 0.30),  # low → light yellow
    (0.90, 0.75, 0.25),
    (0.70, 0.55, 0.20),
    (0.45, 0.30, 0.12),
    (0.25, 0.18, 0.08),  # high → dark brown
    (0.10, 0.07, 0.05)   # highest → almost black
]
brown_dark_cmap = LinearSegmentedColormap.from_list("brown_dark", colors)

# 7️⃣ Visualization
p = pv.Plotter(window_size=[1600, 1000])
p.set_background("black")

p.add_mesh(
    grid,
    scalars="elevation",
    cmap=brown_dark_cmap,
    smooth_shading=False,
    lighting=False,
    show_edges=False,
)

# Gentle relief perception
p.enable_eye_dome_lighting()

# Camera setup
p.camera_position = [
    (x.max()*1.2, y.max()*1.2, z.max()*3),
    (x.mean(), y.mean(), z.mean()),
    (0, 0, 1)
]

print("🌋 Matte brown–yellow terrain (darker at high elevations, no reflections).")
p.show()
