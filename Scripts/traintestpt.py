import torch
from torch import optim
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

device = 'cpu'

split = torch.load("indices.pt")
train_indices = split["train_indices"]
test_indices  = split["test_indices"]

data = torch.load("allData_8s_smoothed.pt", map_location=device)

waveforms            = data["raw waves"]
labels_depth         = data["depth labels"]
labels_mag           = data["mag labels"]
origin_tuples_tensor = data['origin']
loc_tuples_tensor    = data['loc']

train_waveforms = waveforms[train_indices]
mag_train_labels    = labels_mag[train_indices]
depth_train_labels  = labels_depth[train_indices]
origin_tuples_train = origin_tuples_tensor[train_indices]
loc_tuples_train    = loc_tuples_tensor[train_indices]

test_waveforms     = waveforms[test_indices]
mag_test_labels    = labels_mag[test_indices]
depth_test_labels  = labels_depth[test_indices]
origin_tuples_test = origin_tuples_tensor[test_indices]
loc_tuples_test    = loc_tuples_tensor[test_indices]


test_data = {
    'raw waves': test_waveforms,
    'depth labels': depth_test_labels,
    'mag labels': mag_test_labels,
    'origin': origin_tuples_test,
    'loc': loc_tuples_test
}

train_data = {
    'raw waves': train_waveforms,
    'depth labels': depth_train_labels,
    'mag labels': mag_train_labels,
    'origin': origin_tuples_train,
    'loc': loc_tuples_train
}

torch.save(train_data, 'train.pt')
torch.save(test_data, 'test.pt')