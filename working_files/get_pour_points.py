import rasterio
from pysheds.grid import Grid
import sys
from functions import *
from matplotlib import colors
import matplotlib.pyplot as plt
import geopandas as gpd
import json
import os

def load_rast(path): # Load raster
    grid = Grid.from_raster(path)
    dem = grid.read_raster(path)
    print('read raster')
    return dem, grid

def preprocess(dem, grid): # Preprocess
    pit_filled_dem = grid.fill_pits(dem)
    print('Pits filled.')
    flooded_dem = grid.fill_depressions(pit_filled_dem)
    print('Depressions filled.')
    inflated_dem = grid.resolve_flats(flooded_dem)
    print('Flats resolved.')
    dirmap = (64, 128, 1, 2, 4, 8, 16, 32)
    fdir = grid.flowdir(inflated_dem, dirmap=dirmap)
    print('Flow direction got.')
    acc = grid.accumulation(fdir, dirmap=dirmap)
    print('Accumulation got.')
    return acc, fdir, grid

def pour_points(acc, fdir, grid): # Make Df
    # Make sub arrays of coords
    arr = np.array(acc.coords)
    sub_arrays = np.split(arr, grid.shape[0], axis=0)

    # High acc coords and vals
    high_acc_coords = [sub_arrays[i][np.argsort(acc.view()[i])[-5:]] for i in range(len(sub_arrays))]
    high_acc_values = [acc.view()[i][np.argsort(acc.view()[i])[-5:]] for i in range(len(sub_arrays))]

    # Make GDF for coords & vals
    x = [x[i][1] for x in high_acc_coords for i in range(len(x))]
    y = [x[i][0] for x in high_acc_coords for i in range(len(x))]
    vals = np.array([x[i] for x in high_acc_values for i in range(len(x))]).reshape(-1,1)
    gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(x,y), crs='EPSG:4326')
    gdf['acc'] = vals

    # Extract river network
    branches = grid.extract_river_network(fdir, acc > 100000, apply_output_mask=False)

    # Put rivers in GDF
    geojson_string = json.dumps(branches, indent=2)
    gdf_streams = gpd.read_file(geojson_string)
    gdf_streams['stream_no'] = gdf_streams.index
    # Join both GDF
    joined = gpd.sjoin_nearest(gdf, gdf_streams, how='left')
    joined.drop(columns=['index_right'], inplace=True)
    idx = joined.groupby(['stream_no'])['acc'].transform(max) == joined['acc']
    pour_points_df = joined[idx]

    # Get pour points
    pour_points = [(point.x, point.y) for point in pour_points_df.geometry]
    pour_points_df['tuples'] = pour_points
    pour_points_df['geometry_WKT'] = pour_points_df.geometry.to_wkt()
    gdf_save = pour_points_df.drop(columns=['geometry'])
    gdf_save.to_csv('/sciclone/home/ntlewis/Nick-Lewis-Research/working_files/data/pour_points')
    print('Saved to CSV.')


def main():
    tiff_name = sys.argv[1]
    if os.path.exists(f'/sciclone/home/ntlewis/Nick-Lewis-Research/working_files/data/{tiff_name}'):
        print('File exists!')
    else:
        print('No such file')
    path = f'/sciclone/home/ntlewis/Nick-Lewis-Research/working_files/data/{tiff_name}'
    dem, grid = load_rast(path)
    acc, fdir, grid = preprocess(dem, grid)
    pour_points(acc, fdir, grid)

if __name__ == '__main__':
    main()