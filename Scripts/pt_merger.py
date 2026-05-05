import torch
from torch import optim
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

torchfile = 'allData_8s_smoothed.pt'


files_list = ['d201001a_depth_and_mag_label_smoothing.pt', 
              'd201001b_depth_and_mag_label_smoothing.pt',
              'd201001c_depth_and_mag_label_smoothing.pt',
              'd201002a_depth_and_mag_label_smoothing.pt',
              'd201002b_depth_and_mag_label_smoothing.pt',
              'd201002c_depth_and_mag_label_smoothing.pt',
              'd201003a_depth_and_mag_label_smoothing.pt',
              'd201003b_depth_and_mag_label_smoothing.pt',
              'd201003c_depth_and_mag_label_smoothing.pt',
              'd201004a_depth_and_mag_label_smoothing.pt',
              'd201004b_depth_and_mag_label_smoothing.pt',
              'd201004c_depth_and_mag_label_smoothing.pt',
              'd201005a_depth_and_mag_label_smoothing.pt',
              'd201005b_depth_and_mag_label_smoothing.pt',
              'd201005c_depth_and_mag_label_smoothing.pt',
              'd201006a_depth_and_mag_label_smoothing.pt',
              'd201006b_depth_and_mag_label_smoothing.pt',
              'd201006c_depth_and_mag_label_smoothing.pt',
              'd201007a_depth_and_mag_label_smoothing.pt',
              'd201007b_depth_and_mag_label_smoothing.pt',
              'd201007c_depth_and_mag_label_smoothing.pt',
              'd201008a_depth_and_mag_label_smoothing.pt',
              'd201008b_depth_and_mag_label_smoothing.pt',
              'd201008c_depth_and_mag_label_smoothing.pt',
              'd201009a_depth_and_mag_label_smoothing.pt',
              'd201009b_depth_and_mag_label_smoothing.pt',
              'd201009c_depth_and_mag_label_smoothing.pt',
              'd201010a_depth_and_mag_label_smoothing.pt',
              'd201010b_depth_and_mag_label_smoothing.pt',
              'd201010c_depth_and_mag_label_smoothing.pt',
              'd201011a_depth_and_mag_label_smoothing.pt',
              'd201011b_depth_and_mag_label_smoothing.pt',
              'd201011c_depth_and_mag_label_smoothing.pt',
              'd201012a_depth_and_mag_label_smoothing.pt',
              'd201012b_depth_and_mag_label_smoothing.pt',
              'd201012c_depth_and_mag_label_smoothing.pt',
              'd201101a_depth_and_mag_label_smoothing.pt',
              'd201101b_depth_and_mag_label_smoothing.pt',
              'd201101c_depth_and_mag_label_smoothing.pt',
              'd201102a_depth_and_mag_label_smoothing.pt',
              'd201102b_depth_and_mag_label_smoothing.pt',
              'd201102c_depth_and_mag_label_smoothing.pt',
              'd201103a_depth_and_mag_label_smoothing.pt',
              'd201103b_depth_and_mag_label_smoothing.pt',
              'd201104a_depth_and_mag_label_smoothing.pt',
              'd201106a_depth_and_mag_label_smoothing.pt',
              'd201106b_depth_and_mag_label_smoothing.pt',
              'd201106c_depth_and_mag_label_smoothing.pt',
              'd201107a_depth_and_mag_label_smoothing.pt',
              'd201107b_depth_and_mag_label_smoothing.pt',
              'd201107c_depth_and_mag_label_smoothing.pt',
              'd201108a_depth_and_mag_label_smoothing.pt',
              'd201108b_depth_and_mag_label_smoothing.pt',
              'd201108c_depth_and_mag_label_smoothing.pt',
              'd201109a_depth_and_mag_label_smoothing.pt',
              'd201109b_depth_and_mag_label_smoothing.pt',
              'd201109c_depth_and_mag_label_smoothing.pt',
              'd201110a_depth_and_mag_label_smoothing.pt',
              'd201110b_depth_and_mag_label_smoothing.pt',
              'd201110c_depth_and_mag_label_smoothing.pt',
              'd201111a_depth_and_mag_label_smoothing.pt',
              'd201111b_depth_and_mag_label_smoothing.pt',
              'd201111c_depth_and_mag_label_smoothing.pt',
              'd201112a_depth_and_mag_label_smoothing.pt',
              'd201112b_depth_and_mag_label_smoothing.pt',
              'd201112c_depth_and_mag_label_smoothing.pt',
              'd201201a_depth_and_mag_label_smoothing.pt',
              'd201201b_depth_and_mag_label_smoothing.pt',
              'd201201c_depth_and_mag_label_smoothing.pt',
              'd201202a_depth_and_mag_label_smoothing.pt',
              'd201202b_depth_and_mag_label_smoothing.pt',
              'd201202c_depth_and_mag_label_smoothing.pt',
              'd201203a_depth_and_mag_label_smoothing.pt',
              'd201203b_depth_and_mag_label_smoothing.pt',
              'd201203c_depth_and_mag_label_smoothing.pt',
              'd201204a_depth_and_mag_label_smoothing.pt'
            ]


raw_data_list     = []
mag_labels_list   = []
depth_labels_list = []

loc_tuples_list        = []
origin_tuples_list     = []

for file in files_list:
    training_data = torch.load(file, map_location = 'cpu')
    raw_data     = training_data['raw waves']
    mag_labels   = training_data['mag labels']
    depth_labels = training_data['depth labels']

    loc_tuples   = training_data['loc']
    origin_tuples= training_data['origin']

    raw_data_list.append(raw_data)
    mag_labels_list.append(mag_labels)
    depth_labels_list.append(depth_labels)

    loc_tuples_list.append(loc_tuples)
    origin_tuples_list.append(origin_tuples)



waveforms = torch.cat(raw_data_list,     dim=0)
depth     = torch.cat(depth_labels_list, dim=0)
mag       = torch.cat(mag_labels_list,   dim=0)
loc       = torch.cat(loc_tuples_list,   dim=0)
origin    = torch.cat(origin_tuples_list,dim=0)

print(waveforms.shape)
print(depth.shape)
print(mag.shape)

data = {
    'raw waves': waveforms,
    'depth labels': depth,
    'mag labels': mag,
    'origin': origin,
    'loc': loc
}

torch.save(data, torchfile)

allData = torch.load(torchfile, map_location = 'cpu')

raw_data     = allData['raw waves']
mag_labels   = allData['mag labels']
depth_labels = allData['depth labels']

print(raw_data.shape)
print(mag_labels.shape)
print(depth_labels.shape)