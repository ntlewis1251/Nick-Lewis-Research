import pandas as pd
from matplotlib import pyplot as plt
import rasterio
from rasterio import plot
import numpy as np
from functions import *
import matplotlib
import os
import sys

# Lets make some arrays and the main relief df.
def make_arrays(raster, resolution, area):
    window_list = []
    height_list = []
    max_height_list = []
    width_list = []
    max_width_list = []
    tile_size = round(area / resolution)
    width = raster.width
    height = raster.height
    for i in range(0, height, tile_size):
        for j in range(0, width, tile_size):
            # Define the window for the current chunk
            window = rasterio.windows.Window(j, i, min(tile_size, width - j), min(tile_size, height - i))
            slice_data = raster.read(1, window=window)
            window_list.append(slice_data.max()-slice_data.min())
            height_list.append(i)
            max_height_list.append(i+tile_size)
            width_list.append(j)
            max_width_list.append(j+tile_size)
    return np.array(window_list), np.array(height_list), np.array(max_height_list), np.array(width_list), np.array(max_width_list)

def arr_to_df(src, win, he, m_he, wi, m_we):
    df_relief = pd.DataFrame(data=[win,he,m_he,wi,m_we]).T
    df_relief.columns = ['Relief','y','max_y','x', 'max_x']
    transform = src.transform
    lon, lat = rasterio.transform.xy(transform, df_relief.y, df_relief.x)
    lon_min, lat_min = rasterio.transform.xy(transform, df_relief.max_y, df_relief.max_x)
    df_relief['North'], df_relief['West'] = lat, lon
    df_relief['South'], df_relief['East'] = lat_min, lon_min
    df_relief['rank'] = df_relief['Relief'].rank(pct=True)
    return df_relief

def contour_arr(df):
    arr_list=[]
    i=0
    for y in np.arange(0, df.y.max()+333, step=333):
        arr=[]
        for x in np.arange(0, df.x.max()+333, step=333):
            mask = (df.y==y) & (df.x==x)
            arr.append((df.Relief[mask]).values[0])
        arr_list.append(arr)
        i+=1
        print(f'Debug {i}')
    return arr_list

def make_plot(arr_list, df, src):
    matplotlib.use('WebAgg')
    fig, ax = plt.subplots(figsize=(20,20), dpi=300)
    basemap = rasterio.plot.show(src, ax=ax, cmap='binary')
    x=(df.West.unique()+df.East.unique())/2
    y=(df.North.unique()+df.South.unique())/2
    X, Y = np.meshgrid(x,y)
    Z=arr_list
    contours = ax.contourf(X,Y,Z, cmap='Reds', alpha=0.5)
    ax.set_title('Relief Contours')
    ax.set_xlabel('Longitude (°)')
    ax.set_ylabel('Latitude (°)')
    cbar = fig.colorbar(contours, ax=ax, label="Relief (m)", shrink=0.8, location='bottom',pad=0.05)
    plt.show()

def main():
    bounds=[]
    for x in enumerate(sys.argv[1:]):
        bounds.append(str(x[1]))
    if os.path.exists('/sciclone/home/ntlewis/Nick-Lewis-Research/working_files/data/va_regions.tiff'):
        print('file exists!')
    else:
        get_topo(bounds=bounds, name='va_regions.tiff')
        print('Topo got!')
    src=rasterio.open('/sciclone/home/ntlewis/Nick-Lewis-Research/working_files/data/va_regions.tiff')
    print('Raster loaded!')
    win, he, m_he, wi, m_we = make_arrays(raster=src, resolution=30, area=10000)
    print('Arrays made!')
    df = arr_to_df(src=src, win=win, he=he, m_he=m_he, wi=wi, m_we=m_we)
    print('Made into a dataframe')
    arrs = contour_arr(df)
    print('Contours created')
    make_plot(arr_list=arrs, df=df, src=src)

if __name__ == '__main__':
    main()