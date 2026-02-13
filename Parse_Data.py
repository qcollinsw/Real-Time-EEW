import sys
import pandas as pd

cols = ['Day','Hour', 'Minute', 'Second','Time +/-','LAT_D','LAT_M', 'LAT +/-', 'LONG_D', 'LONG_M', 'LONG +/-', 'Depth (KM)', 'Depth +/-', 'Mag 1', 'Mag 2', '(District, Region)','REGION NAME']

# EQ Event boundaries
max_long = 144.5
min_long = 141.0
max_lat  = 39.2
min_lat  = 37.4 


if __name__ == "__main__":

    #Generate dataframe
    file_path = sys.argv[1]
    df = pd.read_fwf(file_path, colspecs='infer', skiprows=3, dtype=str, header=None)
    df.columns = cols

    df['LONG_DEC'] = df['LONG_D'].astype(int) + (df['LONG_M'].astype(float)/60)
    df['LAT_DEC'] =  df['LAT_D'].astype(int)  + (df['LAT_M'].astype(float)/60)

    # Filter based on location
    # 141E < Longitude < 144.5 E
    # 37.4 N < Latitude < 39.2 N
    
    df_loc_filter = df[(df['LONG_DEC'].between(min_long, max_long, include="neither")) & (df['LAT_DEC'].between(min_lat, max_lat, include="neither"))]


    #TODO: LOOP THROUGH LIST OF FILENAMES AND RUN THE FILTERS ON THOSE FOLDERS. THEN, HAVE EACH DATA FRAME FOR EACH MONTH APPENDED TO FILE REPRESENTING ALL OF THE 
    #      SEISMIC EVENTS THAT MEET THE CRITERIA

    #TODO: THEN GO THROUGH EACH SEISMIC EVENT AND CHECK CROSS REFERENCE IT WITH THE STATION CATALOG AND ONLY KEEP THE ONES WHERE THE REQUISITE STATIONS
    #      HAVE P-ARRIVAL TIMES AND THAT THOSE TIMES ARE ALL WITHIN 8 SECONDS OF EACH OTHER