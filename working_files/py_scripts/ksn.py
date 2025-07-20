import lsdtopytools as lsd
import matplotlib.pyplot as plt
import numpy as np
import sys

def make_ksn_df(path, dem_name):
    mydem = lsd.LSDDEM(path, dem_name)
    print('Raster Loaded')
    mydem.PreProcessing()
    print('PreProcessed')
    mydem.CommonFlowRoutines()
    print('Flow routines got')
    mydem.ExtractRiverNetwork()
    print('River Network Extracted')
    mydem.DefineCatchment(method='main_basin')
    print('Catchment defined')
    mydem.GenerateChi()
    print('Chi generated')
    mydem.ksn_MuddEtAl2014(target_nodes=70, n_iterations=60, skip=1, minimum_segment_length=10, sigma=2,  nthreads = 1, reload_if_same = False)
    mydem.knickpoint_extraction(lambda_TVD = "auto", combining_window = 30, window_stepped = 80, n_std_dev = 7)
    knickpoint_df = mydem.df_knickpoint
    knickpoint_df.to_csv(f'/sciclone/home/ntlewis/Nick-Lewis-Research/working_files/data/{dem_name}_knickpoints.csv')

def main():
    path = sys.argv[1]
    dem_name = sys.argv[2]
    make_ksn_df(path, dem_name)

if __name__ == '__main__':
    main()