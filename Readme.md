# ReliefForge – 3D Terrain Modeling Toolkit

ReliefForge is an open-source Python toolkit that enables the automated creation of high-quality 3D terrain models from global elevation data. It integrates data acquisition, preprocessing, and visualization into a streamlined workflow—ideal for geoscientists, cartographers, and engineers seeking reproducible terrain outputs.

## Table of Contents
- [Motivation](#motivation)  
- [Key Features](#key-features)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Project Structure](#project-structure)  
- [Requirements](#requirements)  
- [Contribution](#contribution)  
- [License](#license)  

## Motivation  
Accurate terrain models are essential for applications in exploration geology, environmental monitoring, and infrastructure planning. However, acquiring, processing, and visualizing elevation data often involves multiple tools and workflows. ReliefForge bridges this gap by offering an end-to-end pipeline built on Python and the OpenTopography API.

## Key Features  
- Automated download of SRTM 30 m (SRTMGL1) or 90 m (SRTMGL3) datasets via the OpenTopography API.  
- Preprocessing modules including smoothing, hill-shade generation, and balanced white-relief rendering.  
- 3D visualization engine using PyVista and Matplotlib with multiple stylized outputs (matte white, colored elevation, dark brown terrain, borderless renders).  
- Modular architecture allowing each stage—acquisition, processing, and visualization—to be executed independently or as part of a full pipeline.  
- Designed for global regions with initial focus on Saudi Arabia, yet adaptable to any valid AOI supported by OpenTopography.

## Installation  
### Via Conda (recommended)  
```bash
conda env create -f environment.yml  
conda activate dem3d_env  
