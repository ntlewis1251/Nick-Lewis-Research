import rasterio
from pysheds.grid import Grid
import sys
from functions import *


def get_acc(topo_name):
    with rasterio.open(f'/sciclone/home/ntlewis/Nick-Lewis-Research/working_files/data/{topo_name}') as src:
        dem = src.read(1)
        transform = src.transform
        crs = src.crs

    grid = Grid.from_array(dem, data_name='dem', transform=transform, crs=crs)

    # Fill pits and depressions
    grid.fill_depressions(data='dem', out_name='filled_dem')
    grid.resolve_flats(data='filled_dem', out_name='resolved_dem')

    # Compute flow direction (D8 method is common)
    grid.flowdir(data='resolved_dem', out_name='dir')

    # Compute flow accumulation
    grid.accumulation(data='dir', out_name='acc')
    print(grid)

# • Define Pour Points: Determine the outlet points for the watersheds you want to delineate. These can be specific locations (e.g., stream gauges, dam locations) or points identified from the flow accumulation raster (e.g., points with high flow accumulation). 

#     # Example: Define a single pour point (replace with your desired coordinates)
#     # You would typically have a list of pour points for multiple watersheds
#     pour_points_x = [x_coord_1, x_coord_2, ...]
#     pour_points_y = [y_coord_1, y_coord_2, ...]

#     # Convert coordinates to cell indices if needed
#     # (pysheds often works with cell indices for pour points)
#     # col, row = grid.map_coords_to_indices(pour_points_x, pour_points_y)

# • Delineate Watersheds: Use the watershed function with your flow direction and pour points. 

#     # Delineate a single watershed
#     # watershed = grid.watershed(data='dir', xy=(col, row), out_name='watershed')

#     # To delineate multiple watersheds, iterate through your pour points:
#     watersheds = []
#     for i in range(len(pour_points_x)):
#         col, row = grid.map_coords_to_indices(pour_points_x[i], pour_points_y[i])
#         watershed_i = grid.watershed(data='dir', xy=(col, row), out_name=f'watershed_{i}')
#         watersheds.append(watershed_i)

# • Export Results (Optional): Save the delineated watersheds as raster or vector data (e.g., GeoTIFF, shapefile). 

#     # Example: Export a watershed raster
#     # with rasterio.open('output_watershed.tif', 'w', driver='GTiff',
#     #                    height=grid.height, width=grid.width,
#     #                    count=1, dtype=watershed.dtype,
#     #                    crs=grid.crs, transform=grid.transform) as dst:
#     #     dst.write(watershed, 1)

# Note: For multiple, non-overlapping watersheds, ensure your pour points are strategically placed to capture the desired drainage areas. If you need to delineate watersheds based on a stream network, you might first extract the stream network from the flow accumulation raster and then use stream junctions or specific points along the streams as pour points. 

def main():
    bounds = sys.argv[1:5]
    topo_name = sys.argv[5]
    print(bounds)
    get_topo(bounds=bounds, name=topo_name)
    get_acc(topo_name=topo_name)

    

if __name__ == '__main__':
    main()