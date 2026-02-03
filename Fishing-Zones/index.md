# Potential Fishing Zone (PFZ) Identification (Sentinel-2)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Sentinel-2](https://img.shields.io/badge/Data-Sentinel--2-green)
![Sector](https://img.shields.io/badge/Focus-Marine--Resources-orange)

## 🌍 Project Overview
This project provides an automated Python workflow for identifying **Potential Fishing Zones (PFZ)** by mapping Chlorophyll-a concentration in coastal waters. 

Using **Sentinel-2 satellite data**, the script calculates the **Normalized Difference Chlorophyll Index (NDCI)**, a key indicator of phytoplankton abundance. Since phytoplankton is the base of the marine food web, its presence correlates directly with fish aggregation, making this tool vital for sustainable marine resource management and efficient fishing operations.

---

## 🔄 The Automated Workflow
The system processes multispectral data through a rigorous masking and indexing pipeline:

```text
[Sentinel-2 Data] -> [Water Masking (NDWI)] -> [Chlorophyll Index (NDCI)] -> [Cloud/Error Validation] -> [PFZ Mapping]
```

## ⚙️ Methodology
The identification of fishing zones relies on precise spectral mathematics using specific Sentinel-2 bands.

1. Water Body Isolation
Before analyzing biological content, we must strictly isolate the water surface to prevent false readings from land or shallow seabeds. We use the Normalized Difference Water Index (NDWI):

NDWI = (Green - NIR) / (Green + NIR)

Logic: Only pixels identified as pure water are passed to the next stage.

2. Chlorophyll-a Detection (NDCI)
To detect phytoplankton, we utilize the specialized Red-Edge Band (Band 5), which is highly sensitive to vegetation in water. The NDCI formula used is:

NDCI = (RedEdge - Red) / (RedEdge + Red)

Why Red-Edge? The Red-Edge band captures the specific reflection peak of chlorophyll that standard Red/Green bands often miss in turbid coastal waters.

Interpretation: Higher NDCI values indicate higher phytoplankton density, signaling a potential feeding ground for fish schools (PFZ).

3. Validation Logic
The script includes a built-in validation system that compares the NDCI result against a True Color (RGB) reference. This step is crucial for manually filtering out:

Cloud artifacts (which can mimic high reflectance).

Bottom reflectance in very shallow waters.

## 📊 Results & Outputs
The tool generates actionable insights for marine analysts:

Analytical Dashboard: A dual-panel visualization showing the Natural View vs. Chlorophyll Distribution, complete with statistical validation metrics.

Geospatial Export: A high-precision GeoTIFF of the chlorophyll values, ready for integration with Sea Surface Temperature (SST) data in QGIS/ArcGIS.

## 💻 Python Implementation
This script demonstrates advanced usage of rasterio for spectral indexing and matplotlib for creating publication-ready marine maps.

[Link to Python Script](./fishing_zone.py)
