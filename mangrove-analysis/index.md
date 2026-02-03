Deskripsi & Penjelasan Script (Untuk README atau Laporan)
Project Title: Spatiotemporal Mangrove Stability Analysis (2019-2024)

Brief Description:
Script ini adalah alat otomatisasi berbasis Python untuk memantau dinamika perubahan tutupan lahan mangrove selama periode 5 tahun. Alat ini memproses citra satelit multi-temporal untuk mengidentifikasi mana area mangrove yang stabil (tua), sedang berkembang, atau baru tumbuh.

Methodology:

Data Processing: Menggunakan library rasterio untuk membaca data spektral Sentinel-2 Level-2A.

Spectral Indexing: Menghitung NDVI (Normalized Difference Vegetation Index) untuk memisahkan vegetasi mangrove dari objek lain dengan nilai ambang batas (threshold) > 0.4.

Spatiotemporal Stacking: Menggunakan logika pixel-based algebraic, di mana masker biner mangrove dari tahun 2019, 2022, dan 2024 dijumlahkan.

Rumus: Age Score = Mask_2019 + Mask_2022 + Mask_2024

Classification:

Score 3 = Stable Mangrove (Terdeteksi di ketiga tahun).

Score 2 = Intermediate (Terdeteksi di 2 tahun terakhir).

Score 1 = New Growth (Baru terdeteksi di 2024).

Results:
Script ini menghasilkan dua output utama:

GeoTIFF Map: Peta klasifikasi umur mangrove yang memiliki georeferensi, siap untuk analisis lebih lanjut di QGIS/ArcGIS.

Analytical Layout (PNG): Visualisasi komprehensif yang menampilkan perbandingan True Color, False Color (untuk kesehatan vegetasi), NDWI (indeks air), dan Peta Stabilitas Mangrove dalam satu bingkai.

### Python Script:
You can view the full automated script [here](./spasio_temporal_2019-2024.py).
