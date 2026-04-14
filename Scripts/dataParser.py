import re
from pathlib import Path
import pandas as pd

# EQ Event Loc boundaries
max_long = 144.5 # Maximum longitude for event
min_long = 141.0 # Minimum longitude for event
max_lat  = 39.2  # Maximum latitude for event 
min_lat  = 37.4  # Minimum latitude for event

valid_stations = ['N.KKWH','N.RZTH','N.KAKH']

valid_year   =   []
valid__month =   []
valid_day    =   []
valid_hour   =   []
valid_minute =   []
valid_second =   []

valid_mag    =   []
valid_depth  =   []
valid_lat    =   []
valid_long   =   []

kkwh_arrivals =  []
rzth_arrivals =  []
kakh_arrivals =  []


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


if __name__ == "__main__":

    # Change these to get data
    path = "./testdata.txt"
    output_file_name = "output.csv"


  
    with open(path, 'r') as data:

        eq_data = ""

        valid_eq = 0
        eq_count = 0

        for line in data:
            eq_data = eq_data + line

            if("-----" in line):
                long_re  = re.search(r"(?<=LONG=)([^a-zA-Z]+[a-zA-Z])", eq_data)
                lat_re   = re.search(r"(?<=LAT=)([^a-zA-Z]+[a-zA-Z])", eq_data)
                depth_re = re.search(r"(?<=DEPTH=)(.*)(KM)", eq_data)
                mag_re   = re.search(r"(?<=MAG1=)(.*)([Vv])", eq_data)

                first_line = eq_data.splitlines()[0]

                first_line_list = first_line.split()

                year_unit  = first_line_list[0]
                month_unit = first_line_list[1]
                day_unit   = first_line_list[2]
                hour_unit  = first_line_list[3]
                minute_unit= first_line_list[4]
                second_unit= first_line_list[5]

                year  = first_line_list[0][0:-1]
                month = first_line_list[1][0:-1]
                day   = first_line_list[2][0:-1]
                hour  = first_line_list[3][0:-1]
                minute= first_line_list[4][0:-1]
                second= first_line_list[5][0:-1]

                # Check to see if the data is numbers
                if(not    is_number(year) 
                   or not is_number(month)  
                   or not is_number(day) 
                   or not is_number(hour) 
                   or not is_number(minute) 
                   or not is_number(second)):
                        print(year)
                        eq_data = ""
                        continue
                
                # check to see if all of the units (Year, month , day, hour, minutes, seconds)
                if("Y" != year_unit[-1]   or
                   "M" != month_unit[-1]  or
                   "D" != day_unit[-1]    or
                   "H" != hour_unit[-1]   or
                   "M" != minute_unit[-1] or
                   "S" != second_unit[-1]):
                    eq_data = ""
                    continue


                if("R=" not in first_line):
                    eq_data = ""
                    continue
                if(long_re is None or lat_re is None or depth_re is None or mag_re is None):
                    eq_data = ""
                    continue

                eq_count = eq_count + 1

                long_ddm = long_re[0]
                lat_ddm  = lat_re[0]
                
                depth = depth_re[0].replace(" ", "")
                mag   = mag_re[0][0:-1]

                if(not is_number(mag)):
                    eq_data = ""
                    continue

                long_ddm_list = long_ddm.split()
                lat_ddm_list  = lat_ddm.split()

                long_dec = float(long_ddm_list[0]) + (float(long_ddm_list[1][:-1]) / 60)
                if(long_ddm_list[1][-1] == 'W'):
                    long_dec = -long_dec

                lat_dec = float(lat_ddm_list[0]) + (float(lat_ddm_list[1][:-1]) / 60)
                if(lat_ddm_list[1][-1] == 'S'):
                    lat_dec = -lat_dec

                if(lat_dec < max_lat and lat_dec > min_lat and long_dec < max_long and long_dec > min_long):

                    if(valid_stations[0] in eq_data and valid_stations[1] in eq_data and valid_stations[2] in eq_data):

                        kkwh_line =  [line for line in eq_data.splitlines() if valid_stations[0] in line]  
                        kkwh_line_list = kkwh_line[0].split() 

                        rzth_line =  [line for line in eq_data.splitlines() if valid_stations[1] in line]  
                        rzth_line_list = rzth_line[0].split() 

                        kakh_line =  [line for line in eq_data.splitlines() if valid_stations[2] in line]  
                        kakh_line_list = kakh_line[0].split() 

                        # if('P' in kkwh_line_list[1] and 'P' in rzth_line_list[1] and 'P' in kakh_line_list[1]):

                        if(kkwh_line_list[1] == 'P' and rzth_line_list[1] == 'P' and kakh_line_list[1] == 'P'):

                            kkwh_arrival = float(kkwh_line_list[2])*3600 + float(kkwh_line_list[3])*60 + float(kkwh_line_list[4])
                            kakh_arrival = float(kakh_line_list[2])*3600 + float(kakh_line_list[3])*60 + float(kakh_line_list[4])
                            rzth_arrival = float(rzth_line_list[2])*3600 + float(rzth_line_list[3])*60 + float(rzth_line_list[4])

                            station_times = [kkwh_arrival, kakh_arrival, rzth_arrival]

                            if(max(station_times) - min(station_times) < 6):

                                valid_year.append(year)  
                                valid__month.append(month)
                                valid_day.append(day)   
                                valid_hour.append(hour)  
                                valid_minute.append(minute)
                                valid_second.append(second)
                                valid_mag.append(mag)   
                                valid_depth.append(depth)
                                valid_lat.append(lat_dec)   
                                valid_long.append(long_dec) 

                                rzth_arrivals.append(rzth_arrival) 
                                kakh_arrivals.append(kakh_arrival)
                                kkwh_arrivals.append(kkwh_arrival)


                                valid_eq = valid_eq+1

                eq_data = ""

        eqxl_data = {"Year": valid_year, "Month": valid__month, "Day": valid_day, "Hour": valid_hour,
                     "Minute": valid_minute, "Second": valid_second, "Magnitude": valid_mag, "Depth": valid_depth,
                     "Lat": valid_lat, "Long": valid_long, "RZTH Arrival": rzth_arrivals, 
                     "KAKH Arrival": kakh_arrivals, "KKWH Arrivals": kkwh_arrivals}  
        
        eqxl_data_df = pd.DataFrame(eqxl_data)
        eqxl_data_df.to_csv(output_file_name, index = False)

        print("Earthquakes parsed: ", eq_count)
        print("Valid earthquakes found: ", valid_eq)
