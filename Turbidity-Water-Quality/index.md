# Coastal Water Quality Monitoring: Turbidity Analysis (Sentinel-2)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Sentinel-2](https://img.shields.io/badge/Data-Sentinel--2-green)
![Field](https://img.shields.io/badge/Focus-Marine--Biology-blue)

## 🌍 Project Overview
This project employs an automated Python workflow to assess water quality in coastal areas, specifically focusing on **Pengambengan Village**. 

By utilizing **Sentinel-2 multispectral imagery**, the script calculates the **Normalized Difference Turbidity Index (NDTI)**. This allows for the mapping of sediment distribution and water clarity over large areas without the immediate need for expensive in-situ equipment, providing a cost-effective solution for coastal management.

---

## 🔄 The Automated Workflow
The processing cycle is designed for speed and precision:

```text
[Sentinel-2 Data] -> [NDWI Water Masking] -> [NDTI Calculation] -> [Statistical Analysis] -> [Mapping]
```

## ⚙️ Methodology
To ensure the analysis only focuses on water, the script performs a two-step spectral process:

1. Water Masking (NDWI)
First, we isolate the water bodies from land features (buildings, vegetation, and sand) using the Normalized Difference Water Index:

NDWI = (Green - NIR) / (Green + NIR)

Logic: Only pixels with NDWI > 0.0 are processed for water quality, ensuring land features do not interfere with the turbidity results.

2. Turbidity Indexing (NDTI)
Once the water is isolated, we calculate the Normalized Difference Turbidity Index to detect suspended sediment:

NDTI = (Red - Green) / (Red + Green)

Key Concept: In coastal waters, a high reflectance in the Red band relative to the Green band indicates a higher concentration of suspended solids or sedimentation.

## 📊 Interpretation Scale
The NDTI values range from -1 to 1, which we interpret as follows:

Low NDTI (Cooler Colors): Clearer water, low suspended sediment.

High NDTI (Warmer Colors): Turbid water, high sediment concentration, or recent runoff events.

## 🗺️ Visualization & Outputs
The script generates high-resolution spatial data for decision-making:

Analytical Layout: A side-by-side comparison of True Color (RGB) and the Turbidity Map.

GeoTIFF Export: A georeferenced raster file ready for further spatial analysis in QGIS or ArcGIS.

## 💻 Python Implementation
This analysis is built for scalability, utilizing rasterio for heavy geospatial data handling and matplotlib for scientific visualization.

[Link to Python Script](./Turbidity.py)
