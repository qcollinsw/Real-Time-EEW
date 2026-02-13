import sys
import pandas as pd

catalog_head = ['Day','Hour', 'Minute', 'Second','Time +/-','LAT_D','LAT_M', 'LAT +/-', 'LONG_D', 'LONG_M', 'LONG +/-', 'Depth (KM)', 'Depth +/-', 'Mag 1', 'Mag 2', '(District, Region)','REGION NAME']

# EQ Event boundaries
max_long = 144.5 # Maximum longitude for event
min_long = 141.0 # Minimum longitude for event
max_lat  = 39.2  # Maximum latitude for event 
min_lat  = 37.4  # Minimum latitude for event


if __name__ == "__main__":

    #Generate dataframe
    catalog_path = sys.argv[1]
    catalog = pd.read_fwf(catalog_path, colspecs='infer', skiprows=3, dtype=str, header=None)
    catalog.columns = catalog_head

    catalog['LONG_DEC'] = catalog['LONG_D'].astype(int) + (catalog['LONG_M'].astype(float)/60)
    catalog['LAT_DEC'] =  catalog['LAT_D'].astype(int)  + (catalog['LAT_M'].astype(float)/60)

    # Filter based on location
    # 141E < Longitude < 144.5 E
    # 37.4 N < Latitude < 39.2 N
    
    catalog_loc_filter = catalog[(catalog['LONG_DEC'].between(min_long, max_long, include="neither")) & (catalog['LAT_DEC'].between(min_lat, max_lat, include="neither"))]


    #TODO: LOOP THROUGH LIST OF FILENAMES AND RUN THE FILTERS ON THOSE FOLDERS. THEN, HAVE EACH DATA FRAME FOR EACH MONTH APPENDED TO FILE REPRESENTING ALL OF THE 
    #      SEISMIC EVENTS THAT MEET THE CRITERIA

    #TODO: THEN GO THROUGH EACH SEISMIC EVENT AND CHECK CROSS REFERENCE IT WITH THE STATION CATALOG AND ONLY KEEP THE ONES WHERE THE REQUISITE STATIONS
    #      HAVE P-ARRIVAL TIMES AND THAT THOSE TIMES ARE ALL WITHIN 8 SECONDS OF EACH OTHER