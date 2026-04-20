from obspy import read

# Read the SAC file into a Stream object
st = read("../Earthquake_Data/Raw_Waveforms/2010/January2010/d201001a/2010-1-1-1-58-58.82/N.KKWH.U.SAC")
print(st)
data_list = st[0].data.tolist() 

print(st[0].stats)
# print(data_list)
# Plot the first trace in the stream

# st.plot()
