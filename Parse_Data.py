import sys
import re
import math
import csv
import os
from io import StringIO
import pandas as pd
import numpy as np

#TODO: Another script will take excel sheet and download waveforms using HiNetPy

valid_eqs_list = []

# Dataframe Header
catalog_head = ['Day','Hour', 'Minute', 'Second','Time +/-','LAT_D','LAT_M', 'LAT +/-', 
                'LONG_D', 'LONG_M', 'LONG +/-', 'Depth (KM)', 'Depth +/-', 'Mag 1', 
                'Mag 2', 'MAX_INTENSITY','(District, Region)','REGION NAME']

# Spacing to seperate columns in params dataset
catalog_spaces = [(3, 4),(5, 7),(8, 10),(11, 15),(16, 19),(21, 23),(24, 28),(29, 32),(34, 37),
              (38, 42),(43, 46),(49, 51),(52, 53),(55, 59),(60, 64),(65, 66),(67, 74),(75, None)]

# Spacing to seperate columns in stations dataset
stations_spaces = [(0, 9),(9, 14),(14, 26),(26, 32),(32, 37),(37, 48),(48, 54),(54, 66),  
                   (66, 78),(78, 100),(100, 108),(108, 115),(115, 120),(120, None)]

valid_stations_set = {'N.KKWH','N.RZTH','N.KAKH'}

# Filter to remove headers from catalog
header_filter = re.compile(r'JST|DATE|REGION NAME')

# EQ Event Loc boundaries
max_long = 144.5 # Maximum longitude for event
min_long = 141.0 # Minimum longitude for event
max_lat  = 39.2  # Maximum latitude for event 
min_lat  = 37.4  # Minimum latitude for event


if __name__ == "__main__":

    # Ensure enough arguments
    argc = len(sys.argv[1:])
    if(argc != 2):
        print("Not enough arguments!\nProper usage .\Parse_Data.py <Catalog List> <Output File Name>")
        sys.exit()
    
    


    # Input text file that is list of catalog files
    catalog_list = sys.argv[1]
    output_file_name = sys.argv[2]

    # Make list of catalog files
    with open(catalog_list, 'r', encoding='utf-8') as listfiles:
        catalog_paths = [line.rstrip('\n') for line in listfiles]

    # Get working directory
    working_directory = os.listdir('.')
    working_directories_list = [directory for directory in working_directory if os.path.isdir(directory)]

    #Iterate through every catalog
    for path in catalog_paths:
    
        # Remove page breaks from catalogs
        with open(path, "r", encoding='utf-8') as f:
            headers_removed = [line for line in f if not header_filter.search(line)]
            headers_removed_stripped = [line for line in headers_removed if line.strip()]
        

        catalog = pd.read_fwf(StringIO("".join(headers_removed)), colspecs=catalog_spaces, dtype=str, header=None)
    
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
        catalog['Year'] = int(path[1:-6])
        catalog['Month'] = int(path[6:-4])
        catalog['Count'] = range(len(catalog))
    
        # catalog.to_csv(path + '_unfiltered.csv', index=False)
    
        # Filter based on location
        # 141E < Longitude < 144.5 E
        # 37.4 N < Latitude < 39.2 N
        catalog_loc_filtered = catalog[(catalog['LONG_DEC'].between(min_long, max_long, inclusive="neither")) 
                                 & (catalog['LAT_DEC'].between(min_lat, max_lat,  inclusive="neither"))]
                        
        # catalog_loc_filtered.to_csv(path + '_filtered.csv', index=False)

        # Iterate through found earthquakes and find their corresponding entry in the other catalog
        for idx, eq in enumerate(catalog_loc_filtered['Count']):
            target_count = eq
            eq_count = -1
            search_directory = ''
            eq_dataframe = ''

            # Search cwd for directory containing second catalog  
            for directory in working_directories_list:
                # Only look at the date and month part of the file name
                if path[1:-4] in directory:

                    #found directory to search
                    search_directory = directory
                    break

            # keep running count of eqs
            for file in os.listdir(search_directory):

                # open files in search directory
                with open("./" + search_directory + "/" + file, "r", encoding='utf-8') as f:

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
            stations_df = pd.read_fwf(stations, colspecs=stations_spaces, skiprows = 4, header=None)

            stations_df.columns = ['STATION', 'PHA', 'TIME', 'RES', 'PHA2','TIME2', 'RES2',  
                                   'N-S AMP', 'E-W AMP', 'U-D AMP', 'DELTA', 'AZM', 'MAG', 'MRES']
            
            stations_df[['TIME_H', 'TIME_M', 'TIME_S']] = stations_df['TIME'].str.split(expand=True)

        
            # Once the EQ is found, check to see if the required substations are there
            if valid_stations_set.issubset(set(stations_df['STATION'])):

                # If stations are found, check to see if they have P wave data
                desired_stations = stations_df[stations_df['STATION'].isin(valid_stations_set)]
                if((desired_stations['PHA'] == 'P').all()):

                    # Calculate the P-wave time for each station in SECONDS
                    arrival_hour = desired_stations['TIME_H'].astype(float).tolist()
                    arrival_min  = desired_stations['TIME_M'].astype(float).tolist()
                    arrival_sec  = desired_stations['TIME_S'].astype(float).tolist()

                    arrival_time_tot_secs = list(3600*np.array(arrival_hour) + 60*np.array(arrival_min) + np.array(arrival_sec))
                    # If they have P wave data, ensure P wave arrival times are all within 6 seconds
                    if(max(arrival_time_tot_secs) - min(arrival_time_tot_secs) < 6):
                        valid_eqs_list.append(catalog_loc_filtered.iloc[idx])

    valid_eqs = pd.DataFrame(valid_eqs_list)

    if(not valid_eqs.empty):
        valid_eqs.columns = catalog_loc_filtered.columns
        valid_eqs.to_csv(output_file_name, index=False)
        print(valid_eqs)

