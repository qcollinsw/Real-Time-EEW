import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import torch
from torch import optim
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from tqdm import tqdm

import torchvision

import torch.nn.functional as F
import torchvision.datasets as datasets
import torchvision.transforms as transforms

import torchmetrics

classes = 2

# Define Model
class depthCNN(nn.Module):

    def __init__(self, num_features):
        super(depthCNN, self).__init__()

        self.conv1   = nn.Conv2d(1,   out_channels = 16,  kernel_size = 3, padding =1)
        self.conv2   = nn.Conv2d(16,  out_channels = 32,  kernel_size = 3, padding =1)
        self.conv3   = nn.Conv2d(32,  out_channels = 64,  kernel_size = 3, padding =1)
        self.conv4   = nn.Conv2d(64,  out_channels = 128, kernel_size = 3, padding =1)
        self.conv5   = nn.Conv2d(128, out_channels = 256, kernel_size = 3, padding =1)
        self.pool    = nn.MaxPool2d(kernel_size = 2, stride = 2, padding = 1)
        self.bn1     = nn.BatchNorm2d(16)
        self.bn2     = nn.BatchNorm2d(32)
        self.bn3     = nn.BatchNorm2d(64)
        self.bn4     = nn.BatchNorm2d(128)
        self.bn5     = nn.BatchNorm2d(256)
        self.relu    = nn.ReLU()
        self.softmax = nn.Softmax(dim=-1)
        self.dropout = nn.Dropout(p=0.2)

        self.fullyconnected = nn.LazyLinear(classes)
    
    def forward(self,x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.dropout(x)

        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.dropout(x)

        x = self.conv3(x)
        x = self.bn3(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.dropout(x)

        x = self.conv4(x)
        x = self.bn4(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.dropout(x)

        x = self.conv5(x)
        x = self.bn5(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.dropout(x)

        x = torch.flatten(x, start_dim = 1)
        x = self.fullyconnected(x)
        x = self.softmax(x)

        return x

# Load training data from .pt file
training_data = torch.load('depthTraining.pt', map_location = 'cpu')
waveforms = training_data['raw waves']
labels    = training_data['labels']
trainingset = TensorDataset(waveforms, labels)

loaded_data = DataLoader(trainingset, batch_size=16)

# Construct model
model = depthCNN(classes)

# define optimizer and loss function 
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

epochs = 120

for epoch in range(epochs):
    
    print(f"Epoch [{epoch + 1}/{epochs}]")

    for i, data in enumerate(loaded_data):

        raw_data, labels = data

        labels = torch.squeeze(labels)

        depth_class = model(raw_data)

        loss = criterion(depth_class, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
