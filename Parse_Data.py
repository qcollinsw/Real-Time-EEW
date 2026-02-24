import sys
import re
from io import StringIO
import pandas as pd
import math
import csv

# Dataframe Header
catalog_head = ['Day','Hour', 'Minute', 'Second','Time +/-','LAT_D','LAT_M', 'LAT +/-', 
                'LONG_D', 'LONG_M', 'LONG +/-', 'Depth (KM)', 'Depth +/-', 'Mag 1', 
                'Mag 2', 'MAX_INTENSITY','(District, Region)','REGION NAME']

# Spacing to seperate columns in dataset
spaces = [(3, 4),(5, 7),(8, 10),(11, 15),(16, 19),(21, 23),(24, 28),(29, 32),(34, 37),
              (38, 42),(43, 46),(49, 51),(52, 53),(55, 59),(60, 64),(65, 66),(67, 74),(75, None)]

# Filter to remove headers from catalog
header_filter = re.compile(r'JST|DATE|REGION NAME')

# EQ Event Loc boundaries
max_long = 144.5 # Maximum longitude for event
min_long = 141.0 # Minimum longitude for event
max_lat  = 39.2  # Maximum latitude for event 
min_lat  = 37.4  # Minimum latitude for event


if __name__ == "__main__":

    # Input list of catalogs
    catalog_paths = sys.argv[1:]

    # Number of input catalogs
    argc = len(catalog_paths)

    #Iterate through every catalog
    for path in catalog_paths:
    
        # Remove page breaks from catalogs
        with open(path, "r") as f:
            headers_removed = [line for line in f if not header_filter.search(line)]
            headers_removed_stripped = [line for line in headers_removed if line.strip()]
        

        catalog = pd.read_fwf(StringIO("".join(headers_removed)), colspecs=spaces, dtype=str, header=None)
    
        catalog.columns = catalog_head

        prev_day = 0

        # Fill in blank catalog days
        for i, day in catalog["Day"].items():
            
            if not math.isnan(float(day)):
                prev_day = catalog["Day"][i]
            else:
                catalog.loc[i,"Day"] = prev_day
        

        catalog['LONG_DEC'] = catalog['LONG_D'].astype(int) + (catalog['LONG_M'].astype(float)/60)
        catalog['LAT_DEC'] =  catalog['LAT_D'].astype(int)  + (catalog['LAT_M'].astype(float)/60)

    
        catalog.to_csv(path + '_unfiltered.csv', index=False, quoting=csv.QUOTE_ALL)
    
        # Filter based on location
        # 141E < Longitude < 144.5 E
        # 37.4 N < Latitude < 39.2 N
        catalog_loc_filtered = catalog[(catalog['LONG_DEC'].between(min_long, max_long, inclusive="neither")) 
                                 & (catalog['LAT_DEC'].between(min_lat, max_lat,  inclusive="neither"))]
                
        catalog_loc_filtered.to_csv(path + '_filtered.csv', index=False)
    
    #TODO: THEN GO THROUGH EACH SEISMIC EVENT AND CHECK CROSS REFERENCE IT WITH THE STATION CATALOG 
    #      AND ONLY KEEP THE ONES WHERE THE REQUISITE STATIONS
    #      HAVE P-ARRIVAL TIMES AND THAT THOSE TIMES ARE ALL WITHIN 8 SECONDS OF EACH OTHER