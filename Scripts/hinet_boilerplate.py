# Sample code from HinetPy documentation: https://pypi.org/project/HinetPy/0.4.1/ 

from HinetPy import Client, win32

# You need a Hi-net account to access the data
client = Client(<username>, <password>)

# Let's try to request 20-minute data of the Hi-net network (with an internal
# network code of '0101') starting at 2010-01-01T00:00 (JST, GMT+0900)
data, ctable = client.get_continuous_waveform("0101", "201001010000", 20)

# The request and download process usually takes a few minutes
# waiting for data request ...
# waiting for data download ...

# Now you can see the data and corresponding channel table in your working directory
# waveform data (in win32 format) : 0101_201001010000_20.cnt
# channel table (plaintext file)  : 0101_20100101.ch

# Let's convert data from win32 format to SAC format
win32.extract_sac(data, ctable)

# Let's extract instrument response as PZ files from the channel table file
win32.extract_sacpz(ctable)

# Now you can see several SAC and SAC_PZ files in your working directory

# N.NGUH.E.SAC  N.NGUH.U.SAC  N.NNMH.N.SAC
# N.NGUH.N.SAC  N.NNMH.E.SAC  N.NNMH.U.SAC
# ...
# N.NGUH.E.SAC_PZ  N.NGUH.U.SAC_PZ  N.NNMH.N.SAC_PZ
# N.NGUH.N.SAC_PZ  N.NNMH.E.SAC_PZ  N.NNMH.U.SAC_PZ
# ...