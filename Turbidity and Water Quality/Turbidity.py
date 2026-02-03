import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from rasterio.warp import transform_bounds

# ==========================================
# 0. SETUP ENVIRONMENT & PATHS
# ==========================================
# The script will look for 'data' and 'output' folders in the location where this file is saved
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUT_DIR  = os.path.join(BASE_DIR, 'output')

# Create the output folder if it doesn't exist
os.makedirs(OUT_DIR, exist_ok=True)

# File Paths (Ensure the filename in the data folder matches exactly)
path_img = os.path.join(DATA_DIR, "sentinel2_2025.tif") 
output_layout = os.path.join(OUT_DIR, "Turbidity_Analysis_Layout.png")
output_tif = os.path.join(OUT_DIR, "Turbidity_Map_Result.tif")

print(f"Working Directory: {BASE_DIR}")

# ==========================================
# 1. UTILITY FUNCTIONS
# ==========================================
def dms_formatter(x, pos):
    """Formats decimal degrees to Degree Minutes (DMS)"""
    d = int(x)
    m = int(abs((x - d) * 60))
    return f"{d}°{m:02d}'"

def add_map_elements(ax):
    """Add North Arrow and stylistic elements"""
    ax.annotate('N', xy=(0.05, 0.95), xytext=(0.05, 0.88),
                xycoords='axes fraction', textcoords='axes fraction',
                arrowprops=dict(facecolor='black', width=3, headwidth=10, headlength=10),
                ha='center', va='center', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle="circle,pad=0.3", fc="white", ec="black", alpha=0.8))

def force_coordinate_style(ax, extent_deg):
    """Force specific coordinate tick placement and formatting"""
    width = extent_deg[1] - extent_deg[0]
    height = extent_deg[3] - extent_deg[2]
    pad_x = width * 0.10 
    pad_y = height * 0.10
    
    x_ticks = np.linspace(extent_deg[0] + pad_x, extent_deg[1] - pad_x, 4)
    y_ticks = np.linspace(extent_deg[2] + pad_y, extent_deg[3] - pad_y, 4)
    
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.xaxis.set_major_formatter(FuncFormatter(dms_formatter))
    ax.yaxis.set_major_formatter(FuncFormatter(dms_formatter))
    ax.tick_params(axis='both', labelsize=8)
    ax.grid(False)

# ==========================================
# 2. MAIN DATA PROCESSING
# ==========================================
def process_turbidity():
    if not os.path.exists(path_img):
        print(f"ERROR: File not found at {path_img}")
        print("Please check your 'data' folder and filename.")
        return

    print("1. Reading Data & Calculating Algorithms...")
    with rasterio.open(path_img) as src:
        blue  = src.read(1).astype('float32')
        green = src.read(2).astype('float32')
        red   = src.read(3).astype('float32')
        nir   = src.read(4).astype('float32')
        
        profile = src.profile.copy()
        
        # Handle division by zero errors
        np.seterr(divide='ignore', invalid='ignore')
        
        # A. True Color (RGB)
        rgb = np.dstack((red, green, blue))
        rgb_norm = np.clip(rgb / 3000, 0, 1) # Standard Sentinel-2 scaling
        
        # B. NDTI (Turbidity) Formula: (Red - Green) / (Red + Green)
        # First, mask Land using NDWI
        ndwi = (green - nir) / (green + nir)
        water_mask = np.where(ndwi > 0.0, 1, 0) # Water > 0
        
        ndti = (red - green) / (red + green)
        turbidity_map = np.where(water_mask == 1, ndti, np.nan)
        
        # C. Coordinates Transformation
        left, bottom, right, top = src.bounds
        new_bounds = transform_bounds(src.crs, 'EPSG:4326', left, bottom, right, top)
        extent_deg = [new_bounds[0], new_bounds[2], new_bounds[1], new_bounds[3]]

    print("2. Generating Visualization...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10), facecolor='#f8f9fa')

    plt.suptitle("Turbidity and Water Quality Mapping Analysis", 
                 fontsize=20, weight='bold', y=0.96, color='#2c3e50')

    # Plot 1: RGB
    ax1.imshow(rgb_norm, extent=extent_deg, aspect='auto')
    ax1.set_title("A. Natural View (True Color RGB)", fontsize=12, weight='bold', pad=10, loc='left')
    force_coordinate_style(ax1, extent_deg)
    add_map_elements(ax1)

    # Plot 2: NDTI
    cmap = plt.get_cmap('gist_earth_r') 
    cmap.set_bad('black') 
    im = ax2.imshow(turbidity_map, cmap=cmap, vmin=-0.15, vmax=0.15, extent=extent_deg, aspect='auto')
    ax2.set_title("B. Sediment Distribution (NDTI Analysis)", fontsize=12, weight='bold', pad=10, loc='left')
    force_coordinate_style(ax2, extent_deg)
    add_map_elements(ax2)

    # Legend
    cbar = plt.colorbar(im, ax=ax2, fraction=0.046, pad=0.04, extend='both')
    cbar.set_label('Turbidity Index (NDTI)\nBlue = Clear Water | Brown = High Turbidity', fontsize=9)

    # Info Box
    textstr = '\n'.join((
        r'$\bf{Analysis\ Interpretation:}$',
        r'• Brown/Yellow Areas: High Sedimentation.',
        r'• Blue/Green Areas: Clear Water.',
        r'• Black Areas: Land Mask (Excluded).',
        ))
    props = dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray')
    ax2.text(0.03, 0.03, textstr, transform=ax2.transAxes, fontsize=9,
             verticalalignment='bottom', bbox=props)

    plt.tight_layout(rect=[0, 0.04, 1, 0.92]) 
    plt.savefig(output_layout, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    print(f"   Layout saved to: {output_layout}")

    print("3. Exporting GeoTIFF...")
    profile.update(dtype=rasterio.float32, count=1, nodata=-9999)
    with rasterio.open(output_tif, 'w', **profile) as dst:
        data_save = np.nan_to_num(turbidity_map, nan=-9999)
        dst.write(data_save.astype(rasterio.float32), 1)
    print(f"   GeoTIFF saved to: {output_tif}")

if __name__ == "__main__":
    process_turbidity()