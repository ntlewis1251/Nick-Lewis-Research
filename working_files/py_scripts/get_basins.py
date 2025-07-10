import rasterio
from pysheds.grid import Grid
import sys
from functions import *
import os
import ast

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
    return fdir, grid, dirmap

def make_sheds(df, grid, fdir, dirmap):
    pour_points_x = [ast.literal_eval(x)[0] for x in df.tuples]
    pour_points_y = [ast.literal_eval(x)[1] for x in df.tuples]
    watersheds = []
    for i in range(len(pour_points_x)):
        catch = grid.catchment(x=pour_points_x[i], y=pour_points_y[i], fdir=fdir, dirmap=dirmap, 
                        xytype='coordinate')
        watersheds.append(catch)
    print(len(watersheds))
    return watersheds

def main():
    tiff_name = sys.argv[1]
    if os.path.exists(f'/sciclone/home/ntlewis/Nick-Lewis-Research/working_files/data/{tiff_name}'):
        print('File exists!')
    else:
        print('No such file')
    path = f'/sciclone/home/ntlewis/Nick-Lewis-Research/working_files/data/{tiff_name}'
    src = rasterio.open(path)
    dem, grid = load_rast(path)
    fdir, grid, dirmap = preprocess(dem, grid)
    df_name = sys.argv[2]
    df = pd.read_csv(f'/sciclone/home/ntlewis/Nick-Lewis-Research/working_files/data/{df_name}')
    watersheds = make_sheds(df, grid, fdir, dirmap)
    
    transform = src.transform
    crs = src.crs
    i=0
    for watershed in watersheds:
        masked_data = np.where(watershed, src.read(1), np.nan)
        profile = {
        'driver': 'GTiff',
        'height': masked_data.shape[0],
        'width': masked_data.shape[1],
        'count': 1,  # Number of bands
        'dtype': masked_data.dtype,
        'crs': crs,
        'transform': transform,
        'compress': 'lzw' # Optional: Add compression
        }   
        output_path = f"/sciclone/home/ntlewis/Nick-Lewis-Research/working_files/data/watersheds/output_raster_{i}.tiff"
        with rasterio.open(output_path, 'w', **profile) as dst:
                dst.write(masked_data, 1)
        i+=1


if __name__ == '__main__':
    main()