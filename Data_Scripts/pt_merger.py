import torch
from torch import optim
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

torchfile = 'allData.pt'


files_list = ['d201001a.pt', 
              'd201001b.pt',
              'd201001c.pt',
              'd201002a.pt',
              'd201002b.pt',
              'd201002c.pt',
              'd201003a.pt',
              'd201003b.pt',
              'd201003c.pt',
              'd201004a.pt',
              'd201004b.pt',
              'd201004c.pt',
              'd201005a.pt',
              'd201005b.pt',
              'd201005c.pt',
              'd201006a.pt',
              'd201006b.pt',
              'd201006c.pt',
              'd201007a.pt',
              'd201007b.pt',
              'd201007c.pt',
              'd201008a.pt',
              'd201008b.pt',
              'd201008c.pt',
              'd201009a.pt',
              'd201009b.pt',
              'd201009c.pt',
              'd201010a.pt',
              'd201010b.pt',
              'd201010c.pt',
              'd201011a.pt',
              'd201011b.pt',
              'd201011c.pt',
              'd201012a.pt',
              'd201012b.pt',
              'd201012c.pt',
              'd201101a.pt',
              'd201101b.pt',
              'd201101c.pt',
              'd201102a.pt',
              'd201102b.pt',
              'd201102c.pt',
              'd201103a.pt',
              'd201103b.pt',
              'd201104a.pt',
              'd201106a.pt',
              'd201106b.pt',
              'd201106c.pt',
              'd201107a.pt',
              'd201107b.pt',
              'd201107c.pt',
              'd201108a.pt',
              'd201108b.pt',
              'd201108c.pt',
              'd201109a.pt',
              'd201109b.pt',
              'd201109c.pt',
              'd201110a.pt',
              'd201110b.pt',
              'd201110c.pt',
              'd201111a.pt',
              'd201111b.pt',
              'd201111c.pt',
              'd201112a.pt',
              'd201112b.pt',
              'd201112c.pt',
              'd201201a.pt',
              'd201201b.pt',
              'd201201c.pt',
              'd201202a.pt',
              'd201202b.pt',
              'd201202c.pt',
              'd201203a.pt',
              'd201203b.pt',
              'd201203c.pt',
              'd201204a.pt'
            ]


raw_data_list     = []
mag_labels_list   = []
depth_labels_list = []

loc_tuples_list        = []
origin_tuples_list     = []

coords_tuples_list = []
times_tuples_list = []


for file in files_list:
    training_data = torch.load(file, map_location = 'cpu')
    raw_data     = training_data['raw waves']
    mag_labels   = training_data['mag labels']
    depth_labels = training_data['depth labels']

    loc_tuples   = training_data['loc']
    origin_tuples= training_data['origin']

    coords_tuples = training_data['coords']
    times_tuples = training_data["time"]

    raw_data_list.append(raw_data)
    mag_labels_list.append(mag_labels)
    depth_labels_list.append(depth_labels)

    loc_tuples_list.append(loc_tuples)
    origin_tuples_list.append(origin_tuples)

    coords_tuples_list.append(coords_tuples)
    times_tuples_list.append(times_tuples)



waveforms = torch.cat(raw_data_list,     dim=0)
depth     = torch.cat(depth_labels_list, dim=0)
mag       = torch.cat(mag_labels_list,   dim=0)
loc       = torch.cat(loc_tuples_list,   dim=0)
origin    = torch.cat(origin_tuples_list,dim=0)
coords    = torch.cat(coords_tuples_list,dim=0)
time      = torch.cat(times_tuples_list, dim=0)


print(waveforms.shape)
print(depth.shape)
print(mag.shape)

data = {
    'raw waves': waveforms,
    'depth labels': depth,
    'mag labels': mag,
    'origin': origin,
    'loc': loc,
    'coords': coords,
    'time': time
}

torch.save(data, torchfile)

allData = torch.load(torchfile, map_location = 'cpu')

raw_data     = allData['raw waves']
mag_labels   = allData['mag labels']
depth_labels = allData['depth labels']

print(raw_data.shape)
print(mag_labels.shape)
print(depth_labels.shape)