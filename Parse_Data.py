import sys
import re
from io import StringIO
import pandas as pd

catalog_head = ['Day','Hour', 'Minute', 'Second','Time +/-','LAT_D','LAT_M', 'LAT +/-', 
                'LONG_D', 'LONG_M', 'LONG +/-', 'Depth (KM)', 'Depth +/-', 'Mag 1', 
                'Mag 2', 'MAX_INTENSITY','(District, Region)','REGION NAME']

# EQ Event boundaries
max_long = 144.5 # Maximum longitude for event
min_long = 141.0 # Minimum longitude for event
max_lat  = 39.2  # Maximum latitude for event 
min_lat  = 37.4  # Minimum latitude for event


if __name__ == "__main__":


    catalog_path = sys.argv[1]

    # Filter to remove header from catalog
    header_filter = re.compile(r'JST|DATE|REGION NAME')

    with open(catalog_path, "r") as f:
        headers_removed = [line for line in f if not header_filter.search(line)]
        headers_removed_stripped = [line for line in headers_removed if line.strip()]

    spaces = [(3, 4),(5, 7),(8, 10),(11, 15),(16, 19),(21, 23),(24, 28),(29, 32),(34, 37),
              (38, 42),(43, 46),(49, 51),(52, 53),(55, 59),(60, 64),(65, 66),(67, 74),(75, None)]
    
    catalog = pd.read_fwf(StringIO("".join(headers_removed)), colspecs=spaces, dtype=str, header=None)

    catalog.columns = catalog_head

    catalog['LONG_DEC'] = catalog['LONG_D'].astype(int) + (catalog['LONG_M'].astype(float)/60)
    catalog['LAT_DEC'] =  catalog['LAT_D'].astype(int)  + (catalog['LAT_M'].astype(float)/60)

    # Filter based on location
    # 141E < Longitude < 144.5 E
    # 37.4 N < Latitude < 39.2 N
    catalog_loc_filter = catalog[(catalog['LONG_DEC'].between(min_long, max_long, inclusive="neither")) 
                                 & (catalog['LAT_DEC'].between(min_lat, max_lat,  inclusive="neither"))]
    
    #print out EQ dataframe
    with open("eq_daframe.txt", "w") as v:
        print(catalog.to_string(), file = v)
    
    #TODO: LOOP THROUGH LIST OF FILENAMES AND RUN THE FILTERS ON THOSE FOLDERS. THEN, HAVE EACH DATA 
    #      FRAME FOR EACH MONTH APPENDED TO FILE REPRESENTING ALL OF THE 
    #      SEISMIC EVENTS THAT MEET THE CRITERIA

    #TODO: THEN GO THROUGH EACH SEISMIC EVENT AND CHECK CROSS REFERENCE IT WITH THE STATION CATALOG 
    #      AND ONLY KEEP THE ONES WHERE THE REQUISITE STATIONS
    #      HAVE P-ARRIVAL TIMES AND THAT THOSE TIMES ARE ALL WITHIN 8 SECONDS OF EACH OTHER