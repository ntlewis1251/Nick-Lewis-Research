from rasterio.crs import CRS
import rioxarray as rxr
import sys

def reproject(dem_path, dem_name):
    crs = CRS.from_epsg(2283)
    dem = rxr.open_rasterio(dem_path)
    reprojected_dem = dem.rio.reproject(dst_crs=crs)
    reprojected_dem.rio.to_raster(f"/sciclone/home/ntlewis/Nick-Lewis-Research/working_files/data/{dem_name}_reproj.tiff")

def main():
    dem_path = sys.argv[1]
    dem_name = dem_path.split(sep='/')[-1][0:-5]
    reproject(dem_path=dem_path, dem_name=dem_name)

if __name__ == '__main__':
    main()