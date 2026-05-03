# Author: Quincy Collinsworth
# The purpose of this script is to create tensor file for training 
# CNN model for magnitude classification

# Input: csv file path for EQ data

import csv
from obspy import read
import time
from datetime import datetime, timedelta, timezone
import torch

monthDate = "d201204c"
monthYear = "April2012"
year = "2012"

seconds_to_save = 10

file_to_process = "../Earthquake_Data/Valid_Earthquake_Params/" + year + "/" + monthYear + "/" + monthDate  + ".csv"
raw_waveform_direct = "../Earthquake_Data/Raw_Waveforms/" + year + "/" +  monthYear + "/" + monthDate

sampling_rate = 100 # (HZ)
samples_to_save = seconds_to_save * sampling_rate

stations_tensors_list = []
depth_tensors_list    = []
mag_tensors_list      = []

with open(file_to_process, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        
        
        directory = row['Year'] + '-' + row['Month'] + '-' + row['Day'] + '-' + row['Hour'] + '-' + row['Minute'] + '-' + row['Second']

        print(directory)

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

        try:
            st_kakh = read(file_kakh)
            st_rzth = read(file_rzth)
            st_kkwh = read(file_kkwh)
            file_start_time = str(st_kakh[0].stats.starttime)
            time_HM = file_start_time.partition("T")[2]
        except:
            continue


        time_HM_split = time_HM.split(":")
        file_start_time_seconds = float(time_HM_split[0])*3600 + float(time_HM_split[1])*60


        dt = start_time - file_start_time_seconds

        if(dt < 0):
            dt = (86400 - file_start_time_seconds) + start_time
            print("Detected overflow into previous day\n")

        sample_to_start = int(sampling_rate * dt)

        # print(sample_to_start)

        data_list_kakh = st_kakh[0].data.tolist() 
        data_list_rzth = st_rzth[0].data.tolist() 
        data_list_kkwh = st_kkwh[0].data.tolist() 

        kakh_tensor_data = data_list_kakh[sample_to_start:sample_to_start + samples_to_save]
        kkwh_tensor_data = data_list_kkwh[sample_to_start:sample_to_start + samples_to_save]
        rzth_tensor_data = data_list_rzth[sample_to_start:sample_to_start + samples_to_save]

        depth_tensor     = [0, 0, 0, 0]    #less than 20km, greater than 20km and less than 40, 
                                           #greater than 40 and less than 60, greater than 60

        mag_tensor       = [0, 0, 0, 0]    #Less than 2, 2-3.49, 3.5-4.5, 4.5+

        depth = row['Depth'][:-2]
        mag   = row['Magnitude']

        if(float(depth) <= 20):
            depth_tensor = [1.0, 0.0, 0.0, 0.0]
        elif(float(depth) > 20 and float(depth) <= 40):
            depth_tensor = [0.00, 1.0, 0.0, 0.0]
        elif(float(depth) > 40 and float(depth) <= 60):
            depth_tensor = [0.00, 0.0, 1.0, 0.0]
        else:
            depth_tensor = [0.00, 0.0, 0.0, 1.0]

        if(float(mag) < 2):
            mag_tensor = [1.0, 0, 0, 0]
        elif(float(mag) >=2 and float(mag) < 3.5):
            mag_tensor = [0, 1.0, 0, 0]
        elif(float(mag) >= 3.5 and float(mag) < 4.5):
            mag_tensor = [0, 0, 1.0, 0]
        else:
            mag_tensor = [0, 0, 0, 1.0]

        stations_tensor = torch.tensor([kakh_tensor_data, kkwh_tensor_data, rzth_tensor_data])
        depth_tensor    = torch.tensor(depth_tensor)
        mag_tensor      = torch.tensor(mag_tensor)

        stations_tensors_list.append(stations_tensor)
        depth_tensors_list.append(depth_tensor)
        mag_tensors_list.append(mag_tensor)

    raw_data = torch.stack(stations_tensors_list)
    raw_data = raw_data.unsqueeze(1)

    depth_classification = torch.stack(depth_tensors_list)
    depth_classification = depth_classification.unsqueeze(1)

    mag_classification   = torch.stack(mag_tensors_list)
    mag_classification   = mag_classification.unsqueeze(1)

    data = {
        'raw waves': raw_data,
        'depth labels': depth_classification,
        'mag labels': mag_classification
    }

    print(raw_data.shape)

    torch.save(data, monthDate + '_depth_and_mag.pt')