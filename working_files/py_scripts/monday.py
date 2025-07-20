import xdem
import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def tri_map(tri, dem_name):
    fig, ax = plt.subplots(figsize=(20,20), dpi=300)
    tri_plot = tri.plot(cmap='magma', ax=ax, cbar_title = 'Relief (m)')
    ax.set_title(f'{dem_name} TRI')
    plt.savefig(f'/sciclone/home/ntlewis/Nick-Lewis-Research/working_files/data/{dem_name}.png')

def relict_mapping(tri, dem, dem_name):
    # Getting TRI values for each pixel.
    tri_data = tri.data

    # Ensure tri_data is a numpy array
    tri_data = np.asarray(tri_data)

    # Mask out no_data/nan values
    tri_valid_mask = ~np.isnan(tri_data)
    tri_valid_values = tri_data[tri_valid_mask]

    # Calculate 10th percentile
    percentile_10 = np.percentile(tri_valid_values, 10)

    # Boolean mask: True if below 10th percentile and valid, False otherwise (including no_data)
    TRI_bool_mask = np.where(tri_valid_mask & (tri_data < percentile_10), True, False)

    # If you want to guarantee dtype is bool and no None values:
    TRI_bool_mask = TRI_bool_mask.astype(bool)

    # Getting elevation values for each pixel.
    dem_data = dem.data

    dem_data = np.asarray(dem_data)

    # Mask out no_data/nan values
    dem_valid_mask = ~np.isnan(dem_data)
    dem_valid_values = dem_data[dem_valid_mask]

    # Calculate 90th percentile
    dem_percentile_90 = np.percentile(dem_valid_values, 90)

    # Boolean mask: True if above 90th percentile and valid, False otherwise (including no_data)
    dem_bool_mask = np.where(dem_valid_mask & (dem_data > dem_percentile_90), True, False)

    dem_bool_mask = dem_bool_mask.astype(bool)

    nrows, ncols = tri.data.shape
    rows, cols = np.indices((nrows, ncols))
    xs, ys = tri.transform * (cols, rows)
    
    # Make DF
    df = pd.DataFrame([xs, ys, dem_bool_mask, TRI_bool_mask]).T
    df.columns = ['lon', 'lat', 'abv_90%_elev', 'blw_10%_relief']

    # Make plot
    fig, ax = plt.subplots(figsize=(20,20), dpi=300)
    dem.plot(ax=ax, cmap='terrain', cbar_title='Elevation')
    sns.scatterplot(data=df[df['abv_90%_elev'] == True] & [df['blw_10%_relief'] == True], x='lon', y='lat')
    plt.savefig(f'/sciclone/home/ntlewis/Nick-Lewis-Research/working_files/data/{dem_name}_relict.png')


def main():
    print(f'Script name: {sys.argv[0]}')
    print(f'Path to DEM: {sys.argv[1]}')
    path = sys.argv[1]
    dem_name = path.split(sep='/')[-1]
    dem = xdem.DEM(path)
    tri = dem.terrain_ruggedness_index(window_size = 3)
    tri_map(tri=tri, dem_name=dem_name)
    relict_mapping(tri=tri, dem=dem, dem_name=dem_name)

if __name__ == '__main__':
    main()