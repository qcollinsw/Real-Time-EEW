from obspy import read

# Read the SAC file into a Stream object
st = read("../Earthquake_Data/Raw_Waveforms/2010/January2010/d201001a/2010-1-1-4-2-9.45/N.RZTH.U.SAC")
# print(st)
data_list = st[0].data.tolist() 

print(st[0].stats.starttime)
print(data_list[7978:(7978 + 8)])
# Plot the first trace in the stream

# st.plot()
