# Author: Quincy Collinsworth
# Script to get raw waveform(s)
# Input: csv containing EQ list

from HinetPy import Client, win32
import csv

file_to_process = "../Earthquake_Data/Valid_Earthquake_Params/2010/January2010/d201001a.csv"

# client = Client('qcollin', 'iXbTVeuU9vVt')


with open(file_to_process, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        rzth_arrival = row['RZTH Arrival']
        kakh_arrival = row['KAKH Arrival']
        kkwh_arrival = row['KKWH Arrivals']
        p_arrivals = [rzth_arrival, kakh_arrival, kkwh_arrival]
        latest_p_arrival = max(rzth_arrival, kakh_arrival, kkwh_arrival)

        start_time = latest_p_arrival - 30