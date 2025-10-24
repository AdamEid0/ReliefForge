#!/usr/bin/env python3
import rasterio
import numpy as np
import pyvista as pv
from scipy.ndimage import gaussian_filter

# -----------------------------
# SETTINGS
# -----------------------------
DEM_PATH = "../Data/3D_prep/SRTM_90m_Riyadh_UTM.tif"
EXAGGERATION = 10.0
MAX_POINTS = 1_500_000
SMOOTH_SIGMA = 1.5     # Gaussian smoothing strength (1.0–3.0 typical)
# -----------------------------

# 1️⃣ Load DEM
with rasterio.open(DEM_PATH) as src:
    dem = src.read(1).astype(np.float32)
    transform = src.transform

# Handle missing values
dem = np.nan_to_num(dem, nan=np.nanmean(dem))

# 2️⃣ Smooth spikes
if SMOOTH_SIGMA > 0:
    dem = gaussian_filter(dem, sigma=SMOOTH_SIGMA)
    print(f"✅ Applied Gaussian smoothing σ={SMOOTH_SIGMA}")

# 3️⃣ Downsample for performance
nrows, ncols = dem.shape
total_points = nrows * ncols
factor = max(1, int(np.ceil(np.sqrt(total_points / MAX_POINTS))))
dem_ds = dem[::factor, ::factor]
print(f"✅ Downsampled to {dem_ds.shape[1]}x{dem_ds.shape[0]} (factor {factor})")

# 4️⃣ Coordinate grid
x = np.arange(dem_ds.shape[1]) * transform.a * factor + transform.c
y = np.arange(dem_ds.shape[0]) * transform.e * factor + transform.f
x, y = np.meshgrid(x, y)
z = dem_ds * EXAGGERATION

grid = pv.StructuredGrid(x, y, z)

# 5️⃣ Normalize elevation for color mapping
z_norm = (z - z.min()) / (z.max() - z.min())
grid["elevation"] = z_norm.ravel(order="F")

# -----------------------------
# 6️⃣ Create custom brown→yellow colormap
# -----------------------------
from matplotlib.colors import LinearSegmentedColormap

colors = [
    (0.95, 0.80, 0.25),  # yellow (low)
    (0.80, 0.60, 0.20),
    (0.65, 0.45, 0.15),
    (0.45, 0.30, 0.10),
    (0.30, 0.20, 0.08)   # dark brown (high)
]
brown_yellow_cmap = LinearSegmentedColormap.from_list("brown_yellow", colors)

# -----------------------------
# 7️⃣ Visualize (no reflections, matte)
# -----------------------------
p = pv.Plotter(window_size=[1600, 1000])
p.set_background("black")

p.add_mesh(
    grid,
    scalars="elevation",
    cmap=brown_yellow_cmap,
    smooth_shading=False,  # keeps matte look
    lighting=False,        # disables specular highlights
    show_edges=False,
)

# Gentle depth perception
p.enable_eye_dome_lighting()

# Camera setup
p.camera_position = [
    (x.max()*1.2, y.max()*1.2, z.max()*3),
    (x.mean(), y.mean(), z.mean()),
    (0, 0, 1)
]

print("🌄 Elevation-colored terrain (brown→yellow, matte, no reflections).")
p.show()
