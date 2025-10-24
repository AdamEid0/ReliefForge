#!/usr/bin/env python3
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import os

DEM_PATH = "../../DATA/DEM_prep/SRTM_90m_Riyadh.tif"
OUT_PATH = "../../DATA/3D_prep/SRTM_90m_Riyadh_UTM.tif"

# Auto-detect approximate UTM zone from bounds
with rasterio.open(DEM_PATH) as src:
    bounds = src.bounds
    center_lon = (bounds.left + bounds.right) / 2
    utm_zone = int((center_lon + 180) / 6) + 1
    dst_crs = f"EPSG:326{utm_zone}"  # Northern Hemisphere UTM

    print(f"📍 Reprojecting to {dst_crs}")

    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds
    )

    profile = src.profile
    profile.update({
        "crs": dst_crs,
        "transform": transform,
        "width": width,
        "height": height
    })

    with rasterio.open(OUT_PATH, "w", **profile) as dst:
        for i in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, i),
                destination=rasterio.band(dst, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.bilinear,
            )

print(f"✅ Reprojected DEM saved to {OUT_PATH}")
