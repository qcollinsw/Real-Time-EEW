import sys
import re
import math
import csv
import os
from io import StringIO
import pandas as pd
import numpy as np

stations_spaces = [(0, 9),(9, 14),(14, 26),(26, 32),(32, 37),(37, 48),(48, 54),(54, 66),  
                   (66, 78),(78, 100),(100, 108),(108, 115),(115, 120),(120, None)]

output_cols = ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second', 'Latitude',
               'Longitude', 'Depth', 'Magnitude', 'N.KKWH P Arrival Time', 'N.RZTH P Arrival Time',
               'N.KAKH P Arrival Time']

valid_stations_set = {'N.KKWH','N.RZTH','N.KAKH'}

max_long = 144.5 # Maximum longitude for event
min_long = 141.0 # Minimum longitude for event
max_lat  = 39.2  # Maximum latitude for event 
min_lat  = 37.4  # Minimum latitude for event

if __name__ == "__main__":

    # Ensure enough arguments
    argc = len(sys.argv[1:])
    if(argc != 2):
        print("Not enough arguments!\nProper usage .\dataParser.py <Directories List> <Output CSV Name>")
        sys.exit()

    directories_list = sys.argv[1]
    output_file_name = sys.argv[2]

    with open(directories_list, 'r', encoding='utf-8') as listfiles:
        directories = [line.rstrip('\n') for line in listfiles]

    valid_eqs = pd.DataFrame(columns = output_cols)

    for directory in directories:

        for file in os.listdir(directory):

            full_path = "./" + directory + "/" + file

            print("Searching in " + full_path)

            # open files in search directory
            with open(full_path, "r", encoding='utf-8') as f:

                with open("debug.txt", "a") as e:
                    full_event = ''
                    eq_year    = 0
                    eq_month   = 0
                    eq_day     = 0
                    eq_hour    = 0
                    eq_minute  = 0
                    eq_second  = 0
                    lat_deg    = 0
                    lat_min    = 0
                    long_deg   = 0
                    long_min   = 0
                    lat_dec    = 0 
                    long_dec   = 0
                    mag        = 0
                    depth      = 0
                    for line in f:

                        # Get time info of earthquake
                        if "R=" in line:
                            time_info = line.split()
                            eq_year  = time_info[0][:-1]
                            eq_month = time_info[1][:-1]
                            eq_day   = time_info[2][:-1]
                            eq_hour  = time_info[3][:-1]
                            eq_min   = time_info[4][:-1]
                            eq_second= time_info[5][:-1]  

                        # Get Location, magnitude, and depth of earthquake                        
                        elif "LAT=" in line:
                            loc_and_mag_info = line.split()
                            lat_deg  = loc_and_mag_info[0][4:]
                            lat_min  = loc_and_mag_info[1][:-1]
                            long_deg = loc_and_mag_info[3][5:]
                            long_min = loc_and_mag_info[4][:-1]

                            lat_dec  = float(lat_deg)  + (float(lat_min)/60)
                            long_dec = float(long_deg) + (float(long_min)/60)
                            
                            if(loc_and_mag_info[1][-1] != 'N'):
                                lat_dec = -lat_dec
                                                        
                            if(loc_and_mag_info[4][-1] != 'E'):
                                long_dec = -long_dec

                            if(loc_and_mag_info[6][-1] == "="):
                                depth   = loc_and_mag_info[7]
                                mag = loc_and_mag_info[9][5:]

                            else:
                               depth = loc_and_mag_info[6][6:]
                               mag = loc_and_mag_info[8][5:] 
                    

                        full_event = full_event+line

                        if(("-"*5) in line):

                            stations = StringIO(full_event)

                            stations_df = pd.read_fwf(stations, colspecs=stations_spaces, skiprows = 4, header=None)

                            stations_df.columns = ['STATION', 'PHA', 'TIME', 'RES', 'PHA2','TIME2', 'RES2',  
                                                   'N-S AMP', 'E-W AMP', 'U-D AMP', 'DELTA', 'AZM', 'MAG', 'MRES']
                            
                            # Check if EQ is in right location
                            if((min_lat < lat_dec < max_lat) and (min_long < long_dec < max_long)):

                                if valid_stations_set.issubset(set(stations_df['STATION'])):
                                    # If stations are found, check to see if they have P wave data
                                    desired_stations = stations_df[stations_df['STATION'].isin(valid_stations_set)]
                                    allowed_wave_types = ['P', 'IP', 'EP']
                                    if(desired_stations['PHA'].isin(allowed_wave_types).all()):
                                        # Calculate the P-wave time for each station in SECONDS
                                        arrival_hour = desired_stations['TIME_H'].astype(float).tolist()
                                        arrival_min  = desired_stations['TIME_M'].astype(float).tolist()
                                        arrival_sec  = desired_stations['TIME_S'].astype(float).tolist()

                                        arrival_time_tot_secs = list(3600*np.array(arrival_hour) + 60*np.array(arrival_min) + np.array(arrival_sec))
                                        # If they have P wave data, ensure P wave arrival times are all within 6 seconds
                                        if(max(arrival_time_tot_secs) - min(arrival_time_tot_secs) < 6):
                                            print("VALID EQ FOUND")
                                            print(full_event, file = e)

                            full_event = ''  

                                                