# Author: Quincy Collinsworth
# The purpose of this script is to create tensor file for training 
# CNN model for magnitude classification

# Appends to already existing .pt file

# Input: csv file path for EQ data

import csv
from obspy import read
import time
from datetime import datetime, timedelta, timezone
import torch


file_to_process = "../Earthquake_Data/Valid_Earthquake_Params/2010/January2010/d201001a.csv"
raw_waveform_direct = "../Earthquake_Data/Raw_Waveforms/2010/January2010/d201001a"

sampling_rate = 100 # (HZ)

with open(file_to_process, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        
        directory = row['Year'] + '-' + row['Month'] + '-' + row['Day'] + '-' + row['Hour'] + '-' + row['Minute'] + '-' + row['Second']

        file_kakh = raw_waveform_direct + "/" + directory + "/" + "N.KAKH.U.SAC"
        file_rzth = raw_waveform_direct + "/" + directory + "/" + "N.RZTH.U.SAC"
        file_kkwh = raw_waveform_direct + "/" + directory + "/" + "N.KKWH.U.SAC"

        # Look at raw waveform....

        rzth_arrival = row['RZTH Arrival']
        kakh_arrival = row['KAKH Arrival']
        kkwh_arrival = row['KKWH Arrivals']
        p_arrivals = [rzth_arrival, kakh_arrival, kkwh_arrival]
        latest_p_arrival = max(rzth_arrival, kakh_arrival, kkwh_arrival)

        start_time = float(latest_p_arrival) - 6
        end_time   = float(latest_p_arrival) + 2

        st_kakh = read(file_kakh)
        st_rzth = read(file_rzth)
        st_kkwh = read(file_kkwh)
        file_start_time = str(st_kakh[0].stats.starttime)
        time_HM = file_start_time.partition("T")[2]


        time_HM_split = time_HM.split(":")
        file_start_time_seconds = float(time_HM_split[0])*3600 + float(time_HM_split[1])*60


        dt = start_time - file_start_time_seconds

        if(dt < 0):
            dt = (86400 - file_start_time_seconds) + start_time
            print("Detected overflow into previous day\n")

        sample_to_start = int(sampling_rate * dt)

        data_list_kakh = st_kakh[0].data.tolist() 
        data_list_rzth = st_rzth[0].data.tolist() 
        data_list_kkwh = st_kkwh[0].data.tolist() 

        kakh_tensor_data = data_list_kakh[sample_to_start:sample_to_start + 5]
        kkwh_tensor_data = data_list_kkwh[sample_to_start:sample_to_start + 5]
        rzth_tensor_data = data_list_rzth[sample_to_start:sample_to_start + 5]

        depth_tensor     = [0, 0]    #less than 20km, greater than 20km

        depth = row['Depth'][:-2]

        if(float(depth) <= 20):
            depth_tensor = [0.95, 0.05]
        else:
            depth_tensor = [0.05, 0.95]

        stations_tensor = torch.tensor([kakh_tensor_data, kkwh_tensor_data, rzth_tensor_data])

        input_output    = (stations_tensor, depth_tensor)

        print(input_output)

        # torch.save(input_output, 'depth_tensors.pt')