import csv
import numpy as np
from sklearn.cluster import KMeans

import torch
from torch import optim
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

import matplotlib.colors as mcolors


import matplotlib.pyplot as plt 

file_to_process = 'split_training.pt'
device = 'cpu'

data = torch.load(file_to_process, map_location=device)

origin_tuples_tensor = data["origin"]
loc_tuples_tensor    = data["loc"]
raw = data['raw waves']
print(raw.shape)

mag = data['mag labels']
print(mag.shape)


mutual_p_wave_diffs = [tuple(x) for x in    loc_tuples_tensor.reshape(-1, 3).tolist()]
origin_time_diffs   = [tuple(x) for x in origin_tuples_tensor.reshape(-1, 1).tolist()]

mutual_p = np.array(mutual_p_wave_diffs)
origin   = np.array(origin_time_diffs)

location_class    = KMeans(n_clusters=3, random_state=0, n_init=10)
origin_time_class = KMeans(n_clusters=3, random_state=0, n_init=10)

location_class.fit(mutual_p)
origin_time_class.fit(origin)

print(type(location_class))

location_labels = location_class.labels_
origin_time_labels = origin_time_class.labels_

location_tensors_list =    []
origin_time_tensors_list = []

for i in location_labels:
    
    if(i == 0):
        location_tensors_list.append(torch.tensor([1, 0, 0]))
    elif(i == 1):
        location_tensors_list.append(torch.tensor([0, 1, 0]))
    else:
        location_tensors_list.append(torch.tensor([0, 0, 1]))

for i in origin_time_labels:
    
    if(i == 0):
        origin_time_tensors_list.append(torch.tensor([1, 0, 0]))
    elif(i == 1):
        origin_time_tensors_list.append(torch.tensor([0, 1, 0]))
    else:
        origin_time_tensors_list.append(torch.tensor([0, 0, 1]))

origin_time_classification = torch.stack(origin_time_tensors_list)
origin_time_classification = origin_time_classification.unsqueeze(1)

loc_class = torch.stack(location_tensors_list)
loc_class = loc_class.unsqueeze(1)

data['loc class'] = loc_class
data['origin class'] = origin_time_classification

# Predict the catagories of the test data

test_file = 'split_testing.pt'

test = torch.load(test_file, map_location=device)

test_origin_tuples = test["origin"]
test_loc_tuples    = test["loc"]

time_tuples        = test["time"]
test_coords_tuples = test["coords"]

loc_tuples      = [tuple(x) for x in test_loc_tuples.reshape(-1, 3).tolist()]
origin_tuples   = [tuple(x) for x in test_origin_tuples.reshape(-1, 1).tolist()]

coords_tuples   = [tuple(x) for x in test_coords_tuples.reshape(-1, 2).tolist()]
time_tuples     = [tuple(x) for x in time_tuples.reshape(-1,1).tolist()]

lats = [loc[0] for loc in coords_tuples ]
longs = [loc[1] for loc in coords_tuples ]

oTimes = [abs(time[0]) for time in origin_tuples]

test_loc_class    = location_class.predict(loc_tuples)
test_origin_class = origin_time_class.predict(origin_tuples)

cmap = mcolors.ListedColormap(["tab:blue", "tab:orange", "tab:green"])

plt.figure()

loc_clusters = plt.scatter(
    longs,
    lats,
    c=test_loc_class,
    cmap=cmap,
    s = 40
)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Location Clusters")
plt.grid(True)

cbar = plt.colorbar(loc_clusters , ticks=[0, 1, 2])
cbar.set_label("Cluster")
cbar.set_ticklabels(["1", "2", "3"])
plt.savefig("location_clusters.png", dpi=300, bbox_inches="tight")
plt.close()

plt.figure()

x = []
for i, _ in enumerate(test_origin_class):
    x.append(i)

time_clusters = plt.scatter(
    x,
    oTimes,
    c = test_origin_class,
    cmap = cmap,
    s = 40

)

plt.xlabel("Event Number")
plt.ylabel("Seconds between origin and latest P-Wave")
plt.title("Origin Time Clusters")
plt.grid(True)

cbar = plt.colorbar(time_clusters , ticks=[0, 1, 2])
cbar.set_label("Cluster")
cbar.set_ticklabels(["1", "2", "3"])
plt.savefig("time_clusters.png", dpi=300, bbox_inches="tight")
plt.close()


test_location_class_tensors = []
test_origin_class_tensors   = []

for i in test_loc_class:
    
    if(i == 0):
        test_location_class_tensors.append(torch.tensor([1, 0, 0]))
    elif(i == 1):
        test_location_class_tensors.append(torch.tensor([0, 1, 0]))
    else:
        test_location_class_tensors.append(torch.tensor([0, 0, 1]))

for i in test_origin_class:
    
    if(i == 0):
        test_origin_class_tensors.append(torch.tensor([1, 0, 0]))
    elif(i == 1):
        test_origin_class_tensors.append(torch.tensor([0, 1, 0]))
    else:
        test_origin_class_tensors.append(torch.tensor([0, 0, 1]))

test_origin_time_class = torch.stack(test_origin_class_tensors)
test_origin_time_class = test_origin_time_class.unsqueeze(1)

test_loc_class = torch.stack(test_location_class_tensors)
test_loc_class = test_loc_class.unsqueeze(1)

test['loc class'] = test_loc_class
test['origin class'] = test_origin_time_class

torch.save(test, 'test.pt')
torch.save(data, 'train.pt')

print(loc_class.shape)
print(loc_class)