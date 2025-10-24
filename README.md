# ReliefForge: A 3D Terrain Modeling Toolkit

**ReliefForge** is a Python toolkit for building accurate, publication-quality 3D terrain models from global elevation data.  
It provides a complete, reproducible workflow for acquiring SRTM DEMs via the OpenTopography API, preprocessing them for clarity, and producing high-quality 3D visualizations suitable for analysis, reports, and mapping applications.

---

## 📘 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Typical Workflow](#typical-workflow)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## 🛰 Overview

ReliefForge streamlines common terrain-processing tasks into modular Python scripts that can run individually or as a complete workflow.

1. **Download:** Retrieve SRTM 30 m (SRTMGL1) or 90 m (SRTMGL3) DEMs for any area of interest (AOI) using the OpenTopography API.  
2. **Prepare:** Process DEMs with nodata correction, smoothing, hillshading, and balanced white relief generation.  
3. **Visualize:** Generate 3D terrain scenes using PyVista and Matplotlib with styles like matte white, colored elevation, dark terrain, or borderless minimalist renders.

Each stage can be used independently or integrated into a larger GIS or modeling pipeline.

---

## 🌍 Key Features

- 🔽 Automated DEM download directly from **OpenTopography**  
- ⚙️ Advanced DEM preprocessing: nodata handling, Gaussian smoothing, hillshade, and white relief  
- 🎨 Multiple 3D rendering styles with consistent camera and lighting presets  
- 🧩 Modular scripts for flexible integration into research or GIS pipelines  
- 🌎 Works globally for any AOI supported by OpenTopography  

---

## ⚙️ Installation

### Option A – Conda (recommended)
```bash
conda env create -f environment.yml
conda activate dem3d_env
```

### Option B – Pip
```bash
pip install -r requirements.txt
```

---

## 🔑 Configuration

### API Key

ReliefForge requires a valid **OpenTopography API key** to download elevation data.

1. Visit the [OpenTopography API registration page](https://portal.opentopography.org/apikeys).  
2. Log in or create a free account.  
3. Generate a new API key (a long alphanumeric string).  
4. Copy the key and paste it inside a text file named `API_Key.txt` in the root directory of your project.

Example:
```
# OpenTopography API Key
1234567890abcdef1234567890abcdef
```

A template file named **`API_Key_TEMPLATE.txt`** is included in this repository.  
Simply duplicate it as `API_Key.txt` and insert your actual key.

✅ **Notes:**
- Do not include quotes, brackets, or spaces.  
- Only one valid key per file.  
- The comment line (`#`) is optional.  
- `API_Key.txt` is ignored by Git for security reasons.  
- Both downloader scripts automatically read the key at runtime.

If you lose or replace your key, update the file — no code changes are required.

---

### Shapefile Input

Place your AOI shapefile files (`.shp`, `.shx`, `.dbf`, `.prj`) in:
```
DATA/shapefiles/
```

Ensure your shapefile uses the right **EPSG:xxxx (WGS 84)** coordinates.

---

## 🧩 Typical Workflow

### 1. Download SRTM DEM
```bash
cd Download_the_data
python download_srtm_30m_from_shapefile.py
# or
python download_srtm_90m_from_shapefile.py
```

### 2. Prepare the DEM
```bash
cd ../Dem_Preparation/src
python 1_read_dem.py
python 2_smooth_dem.py
python 3_compute_hillshade.py
python 6_generate_balanced_white_relief.py
```

### 3. Visualize in 3D
```bash
cd ../../3D_modeling/src
python 1_reproject_dem_utm.py
python 2_visualize_utm_3d.py
```

Other rendering options:
```
3_visualize_white_on_black.py
3b_visualize_white_only.py
3c_visualize_white_matte.py
3d_visualize_white_smooth.py
4_visualize_colored_elevation.py
4b_visualize_colored_dark_brown.py
4c_visualize_no_border.py
```

---

## 🗂 Project Structure

```
ReliefForge/
├── Download_the_data/
│   └── src/
│       ├── download_srtm_30m_from_shapefile.py
│       └── download_srtm_90m_from_shapefile.py
├── Dem_Preparation/
│   └── src/
│       ├── 1_read_dem.py
│       ├── 2_smooth_dem.py
│       ├── 3_compute_hillshade.py
│       ├── 4_generate_white_relief.py
│       ├── 5_preview_relief.py
│       └── 6_generate_balanced_white_relief.py
├── 3D_modeling/
│   └── src/
│       ├── 1_reproject_dem_utm.py
│       ├── 2_visualize_utm_3d.py
│       ├── 3_visualize_white_on_black.py
│       ├── 3b_visualize_white_only.py
│       ├── 3c_visualize_white_matte.py
│       ├── 3d_visualize_white_smooth.py
│       ├── 4_visualize_colored_elevation.py
│       ├── 4b_visualize_colored_dark_brown.py
│       └── 4c_visualize_no_border.py
├── DATA/
│   ├── shapefiles/
│   │   ├── sa.shp
│   │   ├── sa.shx
│   │   ├── sa.dbf
│   │   └── sa.prj
│   ├── DEM_prep/
│   │   └── (generated DEMs after preprocessing)
│   ├── 3D_prep/
│   │   └── (reprojected DEMs for visualization)
│   └── output_renders/
│       └── (final exported images and 3D renders)
├── docs/
│   └── preview/
│       ├── white_relief.png
│       ├── colored_elevation.png
│       └── viz_3d.png
├── API_Key_TEMPLATE.txt
├── environment.yml
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🧰 Troubleshooting

**Invalid API Key**  
Ensure `API_Key.txt` contains only the key (no brackets, quotes, or spaces).

**Request Too Large**  
OpenTopography limits SRTMGL1 datasets to 450,000 km². Use a smaller AOI if necessary.

**Missing GDAL/PROJ**  
Install dependencies via Conda using the `conda-forge` channel to avoid conflicts.

**Rendering Issues**  
For headless servers or limited GPUs, use PyVista’s off-screen rendering and image export options.

---

## 🧭 Roadmap

- Configuration file for paths and parameters  
- Jupyter notebooks for reproducible analysis  
- Batch tiling for large AOIs  
- Cloud masking for satellite overlays  
- Integration with EMIT and Sentinel spectral datasets  

---

## 🤝 Contributing

Contributions are welcome!  

1. Fork the repository.  
2. Create a feature branch (`feature-name`).  
3. Commit and push your changes.  
4. Submit a pull request describing your updates.

Please keep code style consistent and include clear docstrings where relevant.

---

## ⚖️ License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for full terms and conditions.

---

## 🧾 Citation

If you use **ReliefForge** in your research, teaching, or publications, please cite:

**Adam Eid (2025)**  
*ReliefForge: A 3D Terrain Modeling Toolkit*  
[https://github.com/AdamEid0/ReliefForge](https://github.com/AdamEid0/ReliefForge)
