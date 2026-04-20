# Author: Quincy Collinsworth
# The purpose of this script is to create tensor file for training 
# CNN model for magnitude classification

# Appends to already existing .pt file

# Input: csv file path for EQ data

import csv

file_to_process = "../Earthquake_Data/Valid_Earthquake_Params/2010/January2010/d201001a.csv"
raw_waveform_direct = "../Earthquake_Data/Raw_Waveforms/2010/January2010/d201001a"

with open(file_to_process, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        
        directory = row['Year'] + '-' + row['Month'] + '-' + row['Day'] + '-' + row['Hour'] + '-' + row['Minute'] + '-' + row['Second']

        # Look at raw waveform....

        # For each station :
            # Open the .sac file and look at the time 

            # Look at the latest P arrival

            # get the samples starting at the right time in the .sac file

        # make the tensor

        # figure out the mag classification

        # make the right answer

        # append to dictionary of the (data, correct output)

    
    # Load to .pt file


            









