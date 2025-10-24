#!/usr/bin/env python3
import rasterio
import numpy as np
import pyvista as pv

# -----------------------------
# SETTINGS
# -----------------------------
DEM_PATH = "../Data/3D_prep/SRTM_90m_Riyadh_UTM.tif"
EXAGGERATION = 10.0
MAX_POINTS = 1_000_000

# -----------------------------
# 1️⃣ Load DEM
# -----------------------------
with rasterio.open(DEM_PATH) as src:
    dem = src.read(1).astype(np.float32)
    transform = src.transform

dem = np.nan_to_num(dem, nan=np.nanmean(dem))
nrows, ncols = dem.shape
total_points = nrows * ncols
factor = max(1, int(np.ceil(np.sqrt(total_points / MAX_POINTS))))
dem_ds = dem[::factor, ::factor]

nrows_ds, ncols_ds = dem_ds.shape
print(f"✅ Downsampled to {ncols_ds}x{nrows_ds} (factor {factor})")

# -----------------------------
# 2️⃣ Build coordinate grid
# -----------------------------
x = np.arange(ncols_ds) * transform.a * factor + transform.c
y = np.arange(nrows_ds) * transform.e * factor + transform.f
x, y = np.meshgrid(x, y)
z = dem_ds * EXAGGERATION

grid = pv.StructuredGrid(x, y, z)

# -----------------------------
# 3️⃣ Visualize as matte white surface
# -----------------------------
p = pv.Plotter(window_size=[1600, 1000])
p.set_background("black")

# Add white mesh without lighting or reflections
p.add_mesh(
    grid,
    color="white",
    smooth_shading=False,  # no glossy lighting
    lighting=False,        # removes specular/reflection highlights
    show_edges=False,
)

# Optional: ambient depth effect for gentle shape perception
p.enable_eye_dome_lighting()

# Camera setup
p.camera_position = [
    (x.max()*1.2, y.max()*1.2, z.max()*3),
    (x.mean(), y.mean(), z.mean()),
    (0, 0, 1)
]

print("⚪ Matte white terrain (no reflections, pure white on black).")
p.show()
