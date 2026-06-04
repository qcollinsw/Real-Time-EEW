# Author: Quincy Collinsworth
# The purpose of this script is to create tensor file for training 
# CNN model for magnitude classification

# Input: csv file path for EQ data

import csv
from obspy import read
import time
from datetime import datetime, timedelta, timezone
import torch
import sys
import numpy as np

if __name__ == "__main__":

    if(len(sys.argv) != 5):
        sys.exit("Not enough args")

    monthDate = sys.argv[1]
    monthYear = sys.argv[2]
    year = sys.argv[3]
    seconds_to_save = int(sys.argv[4])

    file_to_process = "../Earthquake_Data/Valid_Earthquake_Params/" + year + "/" + monthYear + "/" + monthDate  + ".csv"
    raw_waveform_direct = "../Earthquake_Data/Raw_Waveforms/" + year + "/" +  monthYear + "/" + monthDate

    sampling_rate = 100 # (HZ)
    samples_to_save = seconds_to_save * sampling_rate

    stations_tensors_list = []
    depth_tensors_list    = []
    mag_tensors_list      = []

    origin_tuples         = []
    loc_tuples            = []

    coords_tuples         = []
    time_tuples           = []
    

    with open(file_to_process, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            
            directory = row['Year'] + '-' + row['Month'] + '-' + row['Day'] + '-' + row['Hour'] + '-' + row['Minute'] + '-' + row['Second']

            file_kakh = raw_waveform_direct + "/" + directory + "/" + "N.KAKH.U.SAC"
            file_rzth = raw_waveform_direct + "/" + directory + "/" + "N.RZTH.U.SAC"
            file_kkwh = raw_waveform_direct + "/" + directory + "/" + "N.KKWH.U.SAC"

            # Look at raw waveform....

            rzth_arrival = float(row['RZTH Arrival'])
            kakh_arrival = float(row['KAKH Arrival'])
            kkwh_arrival = float(row['KKWH Arrivals'])
            latest_p_arrival  = max(rzth_arrival, kakh_arrival, kkwh_arrival)
            earliest_p_arrival = min(rzth_arrival, kakh_arrival, kkwh_arrival)

        
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

            data_list_kakh = st_kakh[0].data.tolist() 
            data_list_rzth = st_rzth[0].data.tolist() 
            data_list_kkwh = st_kkwh[0].data.tolist() 

            kakh_tensor_data = data_list_kakh[sample_to_start:sample_to_start + samples_to_save]
            kkwh_tensor_data = data_list_kkwh[sample_to_start:sample_to_start + samples_to_save]
            rzth_tensor_data = data_list_rzth[sample_to_start:sample_to_start + samples_to_save]

            print(directory)
            print(sample_to_start)

            depth_tensor = []

            mag_tensor   = []    #Less than 2, 2-4, 4+

            depth = row['Depth'][:-2]
            mag   = row['Magnitude']

            long  = float(row["Long"])
            lat   = float(row["Lat"])

            if(float(depth) <= 20):
                depth_tensor = [1.0, 0.0, 0.0]
            elif(float(depth) > 20 and float(depth) <=40):
                depth_tensor = [0.0, 1.0, 0.0]
            else:
                depth_tensor = [0.0, 0.0, 1.0]

            if(float(mag) < 2.0):
                mag_tensor = [1.0, 0.0, 0.0]
            elif(float(mag) >=2.0 and float(mag) < 4.0):
                mag_tensor = [0.0, 1.0, 0.0]
            else:
                mag_tensor = [0.0, 0.0, 1.0]

            origin_time  = float(row['Hour'])*3600 + float(row['Minute'])*60 + float(row['Second'])

            a = rzth_arrival - kakh_arrival
            b = rzth_arrival - kkwh_arrival
            c = kakh_arrival - kkwh_arrival

            loc    = torch.tensor((a,b,c))
            origin = torch.tensor((origin_time - earliest_p_arrival))

            coords = torch.tensor((lat, long))
            time   = torch.tensor((origin_time))

            stations_tensor = torch.tensor([kakh_tensor_data, kkwh_tensor_data, rzth_tensor_data])
            depth_tensor    = torch.tensor(depth_tensor)
            mag_tensor      = torch.tensor(mag_tensor)

            stations_tensors_list.append(stations_tensor)
            depth_tensors_list.append(depth_tensor)
            mag_tensors_list.append(mag_tensor)

            origin_tuples.append(origin)
            loc_tuples.append(loc)

            coords_tuples.append(coords)
            time_tuples.append(time)     

        raw_data = torch.stack(stations_tensors_list)
        raw_data = raw_data.unsqueeze(1)


        depth_classification = torch.stack(depth_tensors_list)
        depth_classification = depth_classification.unsqueeze(1)

        mag_classification   = torch.stack(mag_tensors_list)
        mag_classification   = mag_classification.unsqueeze(1)

        origin_tuples_tensor = torch.stack(origin_tuples)
        origin_tuples_tensor = origin_tuples_tensor.unsqueeze(1)

        loc_tuples_tensor    = torch.stack(loc_tuples)
        loc_tuples_tensor    = loc_tuples_tensor.unsqueeze(1)

        coords_tuples_tensors = torch.stack(coords_tuples)
        time_tuples_tensors   = torch.stack(time_tuples)

        data = {
            'raw waves': raw_data,
            'depth labels': depth_classification,
            'mag labels': mag_classification,
            'origin': origin_tuples_tensor,
            'loc': loc_tuples_tensor,
            'coords': coords_tuples_tensors,
            'time': time_tuples_tensors
        }

        print(raw_data.shape)

        torch.save(data, monthDate + '.pt')