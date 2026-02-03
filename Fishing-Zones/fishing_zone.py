import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from rasterio.warp import transform_bounds

# ==========================================
# 0. SETUP ENVIRONMENT & PATHS
# ==========================================
# Automatically detect the folder where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUT_DIR  = os.path.join(BASE_DIR, 'output')

# Create output folder if it doesn't exist
os.makedirs(OUT_DIR, exist_ok=True)

# Input/Output Paths
# NOTE: Ensure your input file in the 'data' folder matches this name
path_img = os.path.join(DATA_DIR, "sentinel2_2025.tif")
output_layout = os.path.join(OUT_DIR, "Fishing_Zone_Layout.png")
output_tif = os.path.join(OUT_DIR, "Chlorophyll_Potential_Map.tif")

print(f"Working Directory: {BASE_DIR}")

# ==========================================
# 1. AESTHETIC FUNCTIONS
# ==========================================
def dms_formatter(x, pos):
    """Converts decimal degrees to Degrees Minutes format"""
    d = int(x)
    m = int(abs((x - d) * 60))
    return f"{d}°{m:02d}'"

def add_map_elements(ax):
    """Adds a North Arrow to the map"""
    ax.annotate('N', xy=(0.05, 0.95), xytext=(0.05, 0.88),
                xycoords='axes fraction', textcoords='axes fraction',
                arrowprops=dict(facecolor='black', width=3, headwidth=10, headlength=10),
                ha='center', va='center', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle="circle,pad=0.3", fc="white", ec="black", alpha=0.8))

def force_coordinate_style(ax, extent_deg):
    """Formats the map axes to look professional"""
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
    
    ax.tick_params(axis='both', which='major', labelsize=8, rotation=0)
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)

# ==========================================
# 2. MAIN PROCESSING
# ==========================================
def analyze_fishing_zones():
    if not os.path.exists(path_img):
        print(f"ERROR: Input file not found at {path_img}")
        return

    print("1. Reading Data & Preparing Validation...")

    with rasterio.open(path_img) as src:
        # Band Mapping (Adjust indices based on your specific stack)
        # Assuming: B2(Blue), B3(Green), B4(Red), B5(RedEdge), B8(NIR)
        blue     = src.read(1).astype('float32')
        green    = src.read(2).astype('float32')
        red      = src.read(3).astype('float32')
        red_edge = src.read(5).astype('float32') 
        nir      = src.read(7).astype('float32') 

        # Copy profile for safe export
        profile = src.profile.copy()
        
        np.seterr(divide='ignore', invalid='ignore')

        # --- A. PREPARE TRUE COLOR (Reference) ---
        rgb = np.dstack((red, green, blue))
        rgb_norm = np.clip(rgb / 2500, 0, 1) 
        
        # --- B. LAND MASKING (NDWI) ---
        ndwi = (green - nir) / (green + nir)
        water_mask = np.where(ndwi > 0.0, 1, 0)
        
        # --- C. CALCULATE NDCI (Chlorophyll-a) ---
        # Formula: (RedEdge - Red) / (RedEdge + Red)
        ndci = (red_edge - red) / (red_edge + red)
        chlorophyll_map = np.where(water_mask == 1, ndci, np.nan)
        
        # --- D. VALIDATION STATISTICS ---
        valid_pixels = ndci[water_mask == 1]
        mean_val = np.nanmean(valid_pixels)
        max_val = np.nanmax(valid_pixels)
        
        print(f"\n[STATISTICAL CHECK]")
        print(f"Mean NDCI : {mean_val:.4f} (Expected: -0.1 to 0.1 for coastal)")
        print(f"Max NDCI  : {max_val:.4f}")
        
        # --- E. COORDINATES ---
        left, bottom, right, top = src.bounds
        new_bounds = transform_bounds(src.crs, 'EPSG:4326', left, bottom, right, top)
        extent_deg = [new_bounds[0], new_bounds[2], new_bounds[1], new_bounds[3]]

    print("2. Generating Layout...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10), facecolor='#f8f9fa')

    # Main Title
    plt.suptitle("Identification of Potential Fishing Zones", 
                 fontsize=20, weight='bold', y=0.96, color='#2c3e50')

    # Subtitle
    fig.text(0.5, 0.92, "Chlorophyll-a Distribution & Validation Analysis", 
             ha='center', fontsize=12, color='#555555')

    # --- LEFT PANEL: TRUE COLOR ---
    ax1.imshow(rgb_norm, extent=extent_deg, aspect='auto')
    ax1.set_title("A. Reference: True Color (Cloud Check)", fontsize=11, weight='bold', pad=10)
    force_coordinate_style(ax1, extent_deg)
    add_map_elements(ax1)

    # --- RIGHT PANEL: NDCI ---
    cmap = plt.get_cmap('viridis') 
    cmap.set_bad('black') 

    im = ax2.imshow(chlorophyll_map, cmap=cmap, vmin=-0.05, vmax=0.15, extent=extent_deg, aspect='auto')
    ax2.set_title("B. Analysis: Chlorophyll-a (NDCI)", fontsize=11, weight='bold', pad=10)
    force_coordinate_style(ax2, extent_deg)
    add_map_elements(ax2)

    # Legend & Validation Box
    cbar = plt.colorbar(im, ax=ax2, fraction=0.046, pad=0.04, extend='max')
    cbar.set_label('Chlorophyll Index (NDCI)', fontsize=9)

    valid_str = '\n'.join((
        r'$\bf{Validation\ Logic:}$',
        r'1. Cloud Artifacts: If Panel A is White but Panel B is Yellow',
        r'   -> FALSE POSITIVE (Ignore).',
        r'2. Algae Presence: High NDCI (Yellow) should align',
        r'   with greenish tints in Panel A.',
        f'3. Statistical Mean: {mean_val:.3f}'
        ))
    props = dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='red')
    ax2.text(0.02, 0.03, valid_str, transform=ax2.transAxes, fontsize=8,
            verticalalignment='bottom', bbox=props)

    # Footer
    fig.text(0.5, 0.02, 
             f"Method: Sentinel-2 Red-Edge Analysis (NDCI) | Validation: Visual & Statistical", 
             ha='center', fontsize=9, color='#555555', style='italic')

    plt.tight_layout(rect=[0, 0.04, 1, 0.90]) 
    plt.savefig(output_layout, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    print(f"   Layout saved to: {output_layout}")
    plt.show()

    # Export GeoTIFF
    print("3. Exporting GeoTIFF...")
    profile.update(dtype=rasterio.float32, count=1, nodata=-9999)
    with rasterio.open(output_tif, 'w', **profile) as dst:
        data_save = np.nan_to_num(chlorophyll_map, nan=-9999)
        dst.write(data_save.astype(rasterio.float32), 1)
    print(f"   GeoTIFF saved to: {output_tif}")

if __name__ == "__main__":
    analyze_fishing_zones()