Project Title
Potential Fishing Zone (PFZ) Identification using Sentinel-2 Imagery

Project Description
This project provides an automated Python workflow for identifying Potential Fishing Zones (PFZ) by mapping Chlorophyll-a concentration in coastal waters. Using Sentinel-2 satellite data, the script calculates the Normalized Difference Chlorophyll Index (NDCI), a key indicator of phytoplankton abundance which correlates directly with fish presence. This tool assists in sustainable marine resource management and efficient fishing operations.

Methodology
Data Processing: Loads Sentinel-2 Multispectral Instrument (MSI) data.

Water Masking: Isolates water bodies using the NDWI (Normalized Difference Water Index) to prevent false readings from land.

Chlorophyll Analysis (NDCI): Utilizes the specialized Red-Edge band (B5) and Red band (B4) to detect chlorophyll concentration.

Formula: NDCI = (RedEdge - Red) / (RedEdge + Red)

Validation System: Includes a built-in validation logic that compares the NDCI result against a True Color (RGB) reference to manually filter out cloud artifacts or bottom reflectance errors.

Results & Output
Analytical Dashboard: A dual-panel visualization showing the Natural View vs. Chlorophyll Distribution, complete with statistical validation metrics.

Geospatial Data: Exports a high-precision GeoTIFF of the chlorophyll values for further analysis in GIS software (QGIS/ArcGIS).

Keywords
Remote Sensing Python Sentinel-2 Chlorophyll-a NDCI Marine Analytics Fishing Zones
