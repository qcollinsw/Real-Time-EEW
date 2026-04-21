# Author: Quincy Collinsworth
# Script to get raw waveform(s)
# Input: csv containing EQ list

from HinetPy import Client, win32
import csv
import time

file_to_process = "../Earthquake_Data/Valid_Earthquake_Params/2010/January2010/d201001a.csv"

client = Client('qcollin', 'iXbTVeuU9vVt')

seconds_in_day = 86400


with open(file_to_process, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        rzth_arrival = row['RZTH Arrival']
        kakh_arrival = row['KAKH Arrival']
        kkwh_arrival = row['KKWH Arrivals']
        p_arrivals = [rzth_arrival, kakh_arrival, kkwh_arrival]
        latest_p_arrival = max(rzth_arrival, kakh_arrival, kkwh_arrival)

        start_time = float(latest_p_arrival) - 60
        year_month_date = row['Year'] + '-' + row['Month'] + '-' + row['Day']


        if(start_time < 0):
            time = 60 - latest_p_arrival
            start_time = seconds_in_day - time
            original_date = date(row['Year'], row['Month'], row['Day'])
            new = original_date - timedelta(days = 1)
            year_month_date = new

            print("Detected overflow into previous day\n")

        formatted_time = time.strftime('%H:%M', time.gmtime(start_time))

        date_time  = year_month_date + "T" + formatted_time

        outputDir = row['Year'] + '-' + row['Month'] + '-' + row['Day'] + '-' + row['Hour'] + '-' + row['Minute'] + '-' + row['Second']

        print(outputDir)

        data, ctable = client.get_continuous_waveform("0101", date_time, 5)

        win32.extract_sac(data, ctable, outdir = outputDir)

        win32.extract_sacpz(ctable, outdir = outputDir)