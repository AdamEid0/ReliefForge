#!/usr/bin/env python3
import rasterio
import numpy as np
import pyvista as pv
from scipy.ndimage import gaussian_filter
from matplotlib.colors import LinearSegmentedColormap

# -----------------------------
# SETTINGS
# -----------------------------
DEM_PATH = "../Data/3D_prep/SRTM_90m_Riyadh_UTM.tif"
EXAGGERATION = 13.0
MAX_POINTS = 1_300_000
SMOOTH_SIGMA = 2.5      # smooth spikes
FADE_EDGE = True         # fade edges to black (remove square boundary)
# -----------------------------

# 1️⃣ Load DEM
with rasterio.open(DEM_PATH) as src:
    dem = src.read(1).astype(np.float32)
    transform = src.transform

dem = np.nan_to_num(dem, nan=np.nanmean(dem))

# 2️⃣ Smooth
dem = gaussian_filter(dem, sigma=SMOOTH_SIGMA)
print(f"✅ Smoothed DEM with σ={SMOOTH_SIGMA}")

# 3️⃣ Downsample
nrows, ncols = dem.shape
factor = max(1, int(np.ceil(np.sqrt(nrows * ncols / MAX_POINTS))))
dem_ds = dem[::factor, ::factor]

# 4️⃣ Optional fade around edges (remove square look)
if FADE_EDGE:
    ny, nx = dem_ds.shape
    y = np.linspace(-1, 1, ny)
    x = np.linspace(-1, 1, nx)
    X, Y = np.meshgrid(x, y)
    fade = np.clip(1 - (X**8 + Y**8)**0.5, 0, 1)  # smooth fade at corners
    dem_ds *= fade
    print("🌀 Applied edge fade for borderless look")

# 5️⃣ Build grid
x = np.arange(dem_ds.shape[1]) * transform.a * factor + transform.c
y = np.arange(dem_ds.shape[0]) * transform.e * factor + transform.f
x, y = np.meshgrid(x, y)
z = dem_ds * EXAGGERATION

grid = pv.StructuredGrid(x, y, z)

# Normalize elevation
z_norm = (z - z.min()) / (z.max() - z.min())
grid["elevation"] = z_norm.ravel(order="F")

# 6️⃣ Brown-to-dark colormap (medium to high = darker)
colors = [
    (0.96, 0.85, 0.30),  # low → light yellow
    (0.85, 0.70, 0.30),
    (0.65, 0.50, 0.20),
    (0.45, 0.32, 0.15),
    (0.30, 0.20, 0.10),
    (0.12, 0.08, 0.06)   # high → dark brown/black
]
brown_dark_cmap = LinearSegmentedColormap.from_list("brown_dark", colors)

# 7️⃣ Visualize
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

# Gentle depth perception only
p.enable_eye_dome_lighting()

# Camera setup
p.camera_position = [
    (x.max()*1.2, y.max()*1.2, z.max()*3),
    (x.mean(), y.mean(), z.mean()),
    (0, 0, 1)
]

print("🌍 Floating matte brown→dark terrain (no square edges, no reflection).")
p.show()
