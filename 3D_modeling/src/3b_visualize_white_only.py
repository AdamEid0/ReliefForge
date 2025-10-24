#!/usr/bin/env python3
import rasterio
import numpy as np
import pyvista as pv

# -----------------------------
# SETTINGS
# -----------------------------
DEM_PATH = "../../DATA/3D_prep/SRTM_90m_Riyadh_UTM.tif"
EXAGGERATION = 10.0
MAX_POINTS = 1_500_000

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
# 3️⃣ All-white terrain surface
# -----------------------------
# Just assign a constant color (no shading values)
color_white = [1.0, 1.0, 1.0]

# -----------------------------
# 4️⃣ Visualize with black background
# -----------------------------
p = pv.Plotter(window_size=[1600, 1000])
p.set_background("black")

p.add_mesh(
    grid,
    color=color_white,
    smooth_shading=True,
    lighting=True,
    show_edges=False,
)

# Add depth and contrast
p.enable_eye_dome_lighting()
p.add_light(pv.Light(light_type="headlight", intensity=1.3))
p.add_light(pv.Light(position=(x.max()*2, y.max()*2, z.max()*4), intensity=0.8))

# Camera
p.camera_position = [
    (x.max()*1.2, y.max()*1.2, z.max()*3),
    (x.mean(), y.mean(), z.mean()),
    (0, 0, 1)
]

print("⚪ Pure white terrain with black background — minimalist relief view.")
p.show()
