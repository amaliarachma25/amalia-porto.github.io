Project Title
Coastal Water Quality Monitoring: Turbidity Analysis using Sentinel-2

Description
This project employs an automated Python workflow to assess water quality in coastal areas (Case Study: Pengambengan Village). By utilizing Sentinel-2 satellite imagery, the script calculates the Normalized Difference Turbidity Index (NDTI) to map sediment distribution and water clarity without the need for expensive in-situ equipment.

Methodology
Data Acquisition: Utilizes Sentinel-2 Level-2A multispectral data.

Water Masking: Applies the NDWI (Normalized Difference Water Index) using Green and NIR bands to isolate water bodies from land features (NDWI > 0.0).

Turbidity Indexing: Calculates NDTI using the Red and Green bands to detect suspended sediment.

Formula: NDTI = (Red - Green) / (Red + Green)

Logic: High reflectance in the Red band relative to Green indicates higher turbidity/sedimentation.

Visualization: Generates a side-by-side comparison of True Color (RGB) and the Turbidity Map for easy interpretation.

Results
Visual Layout: A high-resolution map showing clear water (low NDTI) versus turbid water (high NDTI) zones.

GeoTIFF Export: A georeferenced raster file of the turbidity values, compatible with QGIS/ArcGIS for further spatial analysis.

Key Technologies
Python Rasterio Matplotlib Sentinel-2 Remote Sensing Water Quality

### Python Script:
You can view the full automated script [here](./Turbidity.py).
