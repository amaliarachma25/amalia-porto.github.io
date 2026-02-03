# Spatiotemporal Mangrove Stability Analysis (2019-2024)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat&logo=python)
![Sentinel-2](https://img.shields.io/badge/Data-Sentinel--2-green?style=flat&logo=satellite)

## 🌍 Project Overview
This project uses Python to monitor mangrove changes over 5 years. By processing satellite imagery from 2019, 2022, and 2024, this tool identifies which mangrove areas are **Stable (Old)**, **Recovering**, or **New**.

---

## 🔄 Workflow Diagram
The automated process works as follows:

```text
[Sentinel-2 Input] -> [Calculate NDVI] -> [Binary Masking] -> [Stacking Years] -> [Final Map]
```
## ⚙️ Methodology
1. Spectral Indexing (NDVI)
To separate mangroves from water and land, we use the Normalized Difference Vegetation Index.
Formula used:

NDVI = (NIR - Red) / (NIR + Red)

2. Binary Masking
We filter the image to create a "Mask" where only mangroves are visible.

If NDVI > 0.4 : Pixel is Mangrove (Value = 1)

If NDVI <= 0.4 : Pixel is Non-Mangrove (Value = 0)

3. Spatiotemporal Logic
To determine the age/stability of the mangrove, we simply add up the masks from all three years.

The Logic:
Age_Score = Mask_2019 + Mask_2022 + Mask_2024

## 📊 Classification Results
The resulting Age Score categorizes the mangrove ecosystem into three distinct stability classes:

🟢 Score 3: Stable Mangrove
Definition: Vegetation detected in all 3 years (2019, 2022, and 2024).
Interpretation: Represents mature, established forest with the highest potential for Carbon Stock storage and ecosystem resilience.

🟡 Score 2: Intermediate
Definition: Vegetation detected in 2 out of the 3 years.
Interpretation: Indicates developing forest, recovering areas, or zones experiencing slight dynamic changes.

🔴 Score 1: New Growth
Definition: Vegetation detected only in 1 year (typically 2024).
Interpretation: Represents pioneer vegetation, recent planting efforts (reforestation), or new natural expansion.

## 🗺️ Visualization Output
The script automatically generates a comprehensive layout combining True Color (RGB), False Color (Vegetation Health), and the final Mangrove Stability Map.

## 💻 Python Implementation
This analysis is fully automated using rasterio for geospatial data handling and numpy for efficient array processing.

[Link to Python Script](./spasio_temporal_2019-2024.py)
