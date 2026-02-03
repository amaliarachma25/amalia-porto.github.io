import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter
from rasterio.warp import transform_bounds 

# ==========================================
# 0. SETUP ENVIRONMENT & PATHS
# ==========================================
# Mengatur agar script membaca folder 'data' di lokasi script berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUT_DIR  = os.path.join(BASE_DIR, 'output')

# Pastikan folder output ada
os.makedirs(OUT_DIR, exist_ok=True)

# Path File Input (Pastikan nama file di folder data sesuai dengan ini)
path_2019 = os.path.join(DATA_DIR, "2019_S2.tif")
path_2022 = os.path.join(DATA_DIR, "2022_S2.tif")
path_2024 = os.path.join(DATA_DIR, "2024_S2.tif")

output_png = os.path.join(OUT_DIR, "Mangrove_Analysis_Layout.png")
output_tif = os.path.join(OUT_DIR, "Mangrove_Stability_Map.tif")

print(f"Working Directory: {BASE_DIR}")

# ==========================================
# 1. DEFINISI FUNGSI
# ==========================================

def dms_formatter(x, pos):
    d = int(x)
    m = int(abs((x - d) * 60))
    return f"{d}°{m:02d}'"

def force_coordinate_style(ax, extent_deg):
    width = extent_deg[1] - extent_deg[0]
    height = extent_deg[3] - extent_deg[2]
    pad_x = width * 0.15 
    pad_y = height * 0.15
    x_ticks = np.linspace(extent_deg[0] + pad_x, extent_deg[1] - pad_x, 4)
    y_ticks = np.linspace(extent_deg[2] + pad_y, extent_deg[3] - pad_y, 4)
    
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.xaxis.set_major_formatter(FuncFormatter(dms_formatter))
    ax.yaxis.set_major_formatter(FuncFormatter(dms_formatter))
    ax.tick_params(axis='both', labelsize=8)
    ax.grid(False)

def process_data(path_file, full_output=False):
    if not os.path.exists(path_file):
        raise FileNotFoundError(f"File tidak ditemukan: {path_file}")
        
    with rasterio.open(path_file) as src:
        # Read bands & Normalization
        blue  = src.read(1).astype('float32')
        green = src.read(2).astype('float32')
        red   = src.read(3).astype('float32')
        nir   = src.read(4).astype('float32')
        
        prof = src.profile
        bnds = src.bounds
        crs_val = src.crs

        np.seterr(divide='ignore', invalid='ignore')
        
        # Calculate NDVI
        ndvi = (nir - red) / (nir + red)
        mangrove_mask = np.where(ndvi > 0.4, 1, 0)
        
        if full_output:
            ndwi = (green - nir) / (green + nir)
            
            # True Color Composite
            tci = np.dstack((red, green, blue))
            tci_norm = np.clip(tci / 3000, 0, 1) # Adjust dividing factor based on data scale
            
            # False Color Composite (NIR-Red-Green)
            fcc = np.dstack((nir, red, green))
            fcc_norm = np.clip(fcc / 3000, 0, 1)
            
            return mangrove_mask, tci_norm, fcc_norm, ndwi, prof, bnds, crs_val
            
        return mangrove_mask

# ==========================================
# 2. EKSEKUSI UTAMA
# ==========================================
if __name__ == "__main__":
    print("1. Processing Data...")
    try:
        mask_19 = process_data(path_2019)
        mask_22 = process_data(path_2022)
        mask_24, tci_24, fcc_24, ndwi_24, profile_24, bounds_24, crs_24 = process_data(path_2024, full_output=True)

        print("2. Transforming Coordinates...")
        left, bottom, right, top = bounds_24
        new_bounds = transform_bounds(crs_24, 'EPSG:4326', left, bottom, right, top)
        extent_degree = [new_bounds[0], new_bounds[2], new_bounds[1], new_bounds[3]]

        print("3. Calculating Mangrove Age/Stability...")
        # Logic: 3 = Exist in all years (Stable), 1 = Only in 2024 (New)
        age_score = mask_19 + mask_22 + mask_24
        final_age_map = age_score * mask_24 

        print("4. Generating Visualization...")
        fig, axes = plt.subplots(2, 2, figsize=(16, 14))
        ax1, ax2, ax3, ax4 = axes.flatten()
        
        plt.suptitle("Spatiotemporal Mangrove Stability Analysis (2019-2024)", fontsize=20, weight='bold', y=0.95)

        # Plotting
        ax1.imshow(tci_24, extent=extent_degree, aspect='auto')
        ax1.set_title("True Color (2024)")
        force_coordinate_style(ax1, extent_degree)

        ax2.imshow(fcc_24, extent=extent_degree, aspect='auto')
        ax2.set_title("False Color (Vegetation)")
        force_coordinate_style(ax2, extent_degree)

        ax3.imshow(ndwi_24, cmap='RdBu', vmin=-0.5, vmax=0.5, extent=extent_degree, aspect='auto')
        ax3.set_title("NDWI (Water Index)")
        force_coordinate_style(ax3, extent_degree)

        # Custom Colormap for Age
        colors = ['#ffffff', '#8af257', '#08b825', '#004f0d'] # White, Light Green, Green, Dark Green
        cmap_age = ListedColormap(colors)
        
        ax4.imshow(final_age_map, cmap=cmap_age, extent=extent_degree, aspect='auto')
        ax4.set_title("Mangrove Stability Class")
        force_coordinate_style(ax4, extent_degree)

        # Legend
        legend_elements = [
            Patch(facecolor=colors[3], edgecolor='k', label='Stable (>5 Years)'),
            Patch(facecolor=colors[2], edgecolor='k', label='Intermediate (~3 Years)'),
            Patch(facecolor=colors[1], edgecolor='k', label='New Growth (<2 Years)'),
        ]
        ax4.legend(handles=legend_elements, loc='lower right')

        plt.savefig(output_png, dpi=300, bbox_inches='tight')
        print(f"   Image saved to: {output_png}")

        print("5. Exporting GeoTIFF...")
        profile_24.update(count=1, dtype=rasterio.int32, nodata=0)
        with rasterio.open(output_tif, 'w', **profile_24) as dst:
            dst.write(final_age_map.astype(rasterio.int32), 1)
        print(f"   TIF saved to: {output_tif}")

    except Exception as e:
        print(f"ERROR: {e}")