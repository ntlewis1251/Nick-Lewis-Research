"""
Final py script for pycogs, WIP.

Arguments order:  N (°), E (°), S (°), W (°), Resolution (m), Watershed Dataset Scale, Project Title, API Key
"""

"""
**Script Goals**
- Enter coordinate bounding box, RES, proj title (applied to all exp files with appropriate suffix)
- Export files include:
	- Folders for each watershed w name
        - Relief map
	    - Slope map (similar but not the same!)
	    - Knickpoints mapped (maybe adjust delta ksn?  To isolate bedrock reaches.)
		- For each stream, profile w sed cover represented by colorramp
			- How to determine?  Albedo dataset is one possibility.  I.e reflectivity is modulated by stream cover.  Problem is trees.
		- Profile w trimodal morphology represented (maybe, refer to chuck suggestion)
	- CSVs of knickpoints
		- To be included:
        - Wshed
		- elevation
		- Coords
		- Shapefile geology
		- Nearest roadcut geology that is also within some threshold of elevation from knickpoint.  Do buffer around knickpoint select closest to elevation.
		- Stream cover type (to allow narrowing to bedrock)
		- If BR, fracture data, if AP, bedding
		- If not in AP or BR, Send back a message being like sorry dawg.
		- Depth to mantle @ knickpoint.  Z score to average depth in region.
		- Slope
"""
# Note: I know i saw a roadcut mapping project done by university of Tennessee.  I know it exists.  AGH! 
# Note: Ask about geology APIs to reduce file downloads needed.

# Start of script
# Import stack
import sys
from functions import * # Temporary, implimentation w/o seperate file TODO
import xdem

def wshed_sep():
    """
    Clips larger DEM to internal wsheds at scale chosen by user.  Exports each as its own DEM, deletes larger DEM.
    """
    pass



def maps():
    """
    Uses downloaded DEM object to export a TRI (Terrain Ruggedness Index, similar to local relief) map, 
    a slope map, 
    and knickpoints overlaying slope map (hued by Delta KSN).
    """
    # Xdem to get TRI, Slope.
    # LSDTopy to get knickpoint dem.
    # Code for mapping

def profiles():
    """
    Generates stream profiles.  
    Sep into 3 bins of slope, color by that.  Simplify to regions if possible.  
    Use cover data from abv to color stream profile, filter knickpoints.
    """

def csv_maker():
    pass

def main():
    """
    Main function, interfaces with the command line and calls functions defined above.
    """
    # Takes args from command line and spits them back at you.  Lets you check your work ;).
    # Saves to their own variables for use.
    args = sys.argv
    print(f'Script name: {args[0]}')
    print(f'Bounds: {args[1]}, {args[2]}, {args[3]}, {args[4]}')
    bounds = [args[1], args[2], args[3], args[4]]
    print(f'Resolution: {args[5]}')
    res = args[5]
    print(f'Watershed Scale: {args[6]}')
    wshed_scale = args[6]
    print(f'Project Title: {args[7]}')
    pj_title = args[7]
    print(f'Api key supplied: {True if 8 in range(len(args)) else False}')
    key = args[8]
    pass

if __name__ == '__main__':
    main()