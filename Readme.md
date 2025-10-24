# ReliefForge: A 3D Terrain Modeling Toolkit

ReliefForge is a Python toolkit for building accurate, publication-quality 3D terrain models from global elevation data. It provides a complete, reproducible workflow for acquiring SRTM DEMs via the OpenTopography API, preprocessing them for clarity, and producing high-quality visualizations suitable for analysis, reports, and maps.

## Contents
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

## Overview

ReliefForge streamlines common terrain tasks:
1. Download SRTM 30 m (SRTMGL1) or 90 m (SRTMGL3) DEMs for a user-defined AOI.
2. Prepare DEMs with smoothing, hillshade, and balanced relief.
3. Generate 3D visualizations (matte white, colored elevation, dark terrain, borderless) using PyVista and Matplotlib.

The toolkit is organized as small, focused scripts so each step can be used independently or as part of an end-to-end pipeline.

## Key Features

- Automated SRTM download from OpenTopography.
- Robust DEM preprocessing: nodata handling, Gaussian smoothing, hillshade, white relief.
- Multiple 3D rendering styles; camera and shading presets for consistent results.
- Clear paths and configuration, ready to integrate with larger GIS workflows.
- Works globally for any AOI supported by OpenTopography.

## Installation

### Option A: Conda (recommended)
```bash
conda env create -f environment.yml
conda activate dem3d_env
### Option B: Using Pip
pip install -r requirements.txt

##Configuration
### API Key
1. Visit the [OpenTopography API registration page](https://portal.opentopography.org/apikeys).  
2. Log in or create an OpenTopography account.  
3. Generate a new API key (a long alphanumeric string).  
4. Copy the key and paste it inside a text file named `API_Key.txt` in the root directory of your project.
#### !
A template file named API_Key_TEMPLATE.txt is included in this repository for reference.
Simply copy it as API_Key.txt and paste your real key inside.
### Shapefile Input
Place your AOI shapefile (.shp, .shx, .dbf, .prj) inside:DATA/shapefiles/
Ensure the shapefile uses the right geographic coordinates (EPSG:****).
## Typical Workflow
### Download SRTM DEM
cd Download_the_data
python download_srtm_30m_from_shapefile.py
# or
python download_srtm_90m_from_shapefile.py
### Prepare the DEM
cd ../Dem_Preparation/src
python 1_read_dem.py
python 2_smooth_dem.py
python 3_compute_hillshade.py
python 6_generate_balanced_white_relief.py
### Visualize in 3D
cd ../../3D_modeling/src
python 1_reproject_dem_utm.py
python 2_visualize_utm_3d.py
# Other styles:
# 3_visualize_white_on_black.py
# 3b_visualize_white_only.py
# 3c_visualize_white_matte.py
# 3d_visualize_white_smooth.py
# 4_visualize_colored_elevation.py
# 4b_visualize_colored_dark_brown.py
# 4c_visualize_no_border.py

## Project Structure
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
├── API_Key.txt
├── environment.yml
├── requirements.txt
├── README.md
└── .gitignore

## Troubleshooting
Invalid API Key – Ensure API_Key.txt contains only the key (no brackets, no spaces).

Request too large – OpenTopography limits some datasets to 450 000 km². Clip or reduce AOI.

Missing GDAL/PROJ – Install via Conda (conda-forge) to resolve dependency conflicts.

Rendering issues – Use PyVista’s image export for headless servers or limited GPUs.
## Roadmap
Configuration file for parameters and paths.

Jupyter notebooks for reproducible workflows.

Batch tiling for large AOIs.

Automatic cloud masking for satellite overlays.

Integration with EMIT and Sentinel spectral datasets.
## Contributing
Contributions are welcome!
Follow these steps:

Fork the repository.

Create a feature branch (feature-name).

Commit and push your changes.

Submit a pull request describing your updates.

Please keep code style consistent and include concise docstrings where relevant.

## License
This project is licensed under the MIT License.
See the LICENSE file for full terms and conditions.

## Citation
If you use ReliefForge in research, teaching, or publications, please cite:
Adam Eid (2025)
ReliefForge: A 3D Terrain Modeling Toolkit
https://github.com/AdamEid0/ReliefForge
