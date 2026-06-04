# This script creates random indices pt file for the traintest.py file 
# that stores indices. These indices are used to determine where the training / testing
# split is in the data

import torch
from torch import optim
from torch import nn
from torch.utils.data import DataLoader, TensorDataset, random_split

# Load training data from .pt file
training_data = torch.load('allData.pt', map_location = 'cpu')
waveforms = training_data['raw waves']
labels    = training_data['depth labels']
dataset = TensorDataset(waveforms, labels)

train_perc = 0.7
test_perc  = 0.3

trainingset, testset = random_split(dataset, [train_perc, test_perc])

training = DataLoader(trainingset, batch_size=16, shuffle=True)
testing  = DataLoader(testset,     batch_size=16, shuffle=True)

train_indices = trainingset.indices
test_indices  = testset.indices
torch.save({
    "train_indices": train_indices,
    "test_indices": test_indices
},  "indices.pt")