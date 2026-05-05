import csv
import numpy as np
from sklearn.cluster import KMeans

import torch
from torch import optim
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

file_to_process = 'train.pt'
device = 'cpu'

data = torch.load(file_to_process, map_location=device)

origin_tuples_tensor = data["origin"]
loc_tuples_tensor    = data["loc"]

print(origin_tuples_tensor)


mutual_p_wave_diffs = [x for x in loc_tuples_tensor.tolist()]

print((mutual_p_wave_diffs[0][0][0]))
origin_time_diffs   = [x for x in origin_tuples_tensor.tolist()]
mutual_p = np.array(mutual_p_wave_diffs)

print(mutual_p)
origin   = np.array(origin_time_diffs)

# print(mutual_p)

location_class    = KMeans(n_clusters=3, random_state=0, n_init=10)
origin_time_class = KMeans(n_clusters=3, random_state=0, n_init=10)

location_class.fit(mutual_p)
origin_time_class.fit(origin)

print(location_class.labels_)
print(type(location_class.labels_))
print(location_class.labels_.shape) 
