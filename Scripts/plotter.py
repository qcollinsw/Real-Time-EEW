from obspy import read

# Read the SAC file into a Stream object
st = read("N.KKWH.U.SAC")
print(st)
data_list = st[0].data.tolist() 

print(st[0].stats)
# print(data_list)
# Plot the first trace in the stream

st.plot()
