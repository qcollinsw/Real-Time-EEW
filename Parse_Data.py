import sys
import re
import math
import csv
import os
from io import StringIO
import pandas as pd


# Dataframe Header
catalog_head = ['Day','Hour', 'Minute', 'Second','Time +/-','LAT_D','LAT_M', 'LAT +/-', 
                'LONG_D', 'LONG_M', 'LONG +/-', 'Depth (KM)', 'Depth +/-', 'Mag 1', 
                'Mag 2', 'MAX_INTENSITY','(District, Region)','REGION NAME']

# Spacing to seperate columns in dataset
spaces = [(3, 4),(5, 7),(8, 10),(11, 15),(16, 19),(21, 23),(24, 28),(29, 32),(34, 37),
              (38, 42),(43, 46),(49, 51),(52, 53),(55, 59),(60, 64),(65, 66),(67, 74),(75, None)]

# Filter to remove headers from catalog
header_filter = re.compile(r'JST|DATE|REGION NAME')

def create_data_frame(file):
    for line in file:
        print(line)

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

    # Get working directory
    working_directory = os.listdir('.')
    working_directory_directories_list = [directory for directory in working_directory if os.path.isdir(directory)]

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
        catalog['Count'] = range(len(catalog))
    
        catalog.to_csv(path + '_unfiltered.csv', index=False)
    
        # Filter based on location
        # 141E < Longitude < 144.5 E
        # 37.4 N < Latitude < 39.2 N
        catalog_loc_filtered = catalog[(catalog['LONG_DEC'].between(min_long, max_long, inclusive="neither")) 
                                 & (catalog['LAT_DEC'].between(min_lat, max_lat,  inclusive="neither"))]
                
        catalog_loc_filtered.to_csv(path + '_filtered.csv', index=False)

        # Iterate through found earthquakes and find their corresponding entry in the other catalog
        path = "te"
        for eq in catalog_loc_filtered['Count']:
            target_count = eq
            eq_count = -1
            search_directory = ''
            eq_dataframe = ''

            # Search cwd for directory containing second catalog  
            for directory in working_directory_directories_list:
                if path in directory:

                    #found directory to search
                    search_directory = directory
                    break

            # keep running count of eqs
            for file in os.listdir(search_directory):

                # open files in search directory
                with open("./" + search_directory + "/" + file, "r") as f:

                    # Look for headers in file, and count up for every header you find (header corresponds to eq)

                    line_found = 0
                    for line in f:
                        if "R=" in line:
                            eq_count = eq_count + 1
                            if(eq_count == target_count):
                                line_found = 1
                        
                        if(line_found):
                            if(("-"*5) in line):
                                break
                            eq_dataframe = eq_dataframe + line
            
            stations = StringIO(eq_dataframe)
            stations_df = pd.read_fwf(stations, skiprows = 4, header=None)

            stations_df.columns = ['STATION', 'PHA', 'TIME_H', 'TIME_M', 'TIME_S', 'RES', 'PHA2','TIME_M2', 'TIME_S2', 'RES2',  
                                   'N-S', 'AMP1', 'E-W', 'AMP2', 'U-D', 'AMP3', 'DELTA', 'AZM', 'MAG', 'MRES']

            with open("output.txt", "w") as f:
                print(stations_df.to_string(), file =f )

                                


    
    #TODO: CHECK Stations, P-Waves, and build dataframe that contains lists of EQs for raw waveforms
    #TODO: Verify this script ~robustly~