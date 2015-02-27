import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft

filtered_data = np.genfromtxt('IIR_filtered.txt', delimiter=' ', names=True, skiprows=0)
filtered_array = [list(each) for each in filtered_data]

filtered_list = []
for i,row in enumerate(filtered_array):
    filtered_list.append(row[0])
print len(filtered_list)
#print filtered_list

data = np.genfromtxt('test.txt', delimiter=', ', names=True, skiprows=0)
data_array = [list(each) for each in data]

data_list = []
for i,row in enumerate(data_array):
    if i < 1599:
	data_list.append(row[0])
print len(data_list)
#print data_list

#plt.plot(data_list)
#plt.plot(filtered_list)
#plt.show()
#"""

from scipy.fftpack import fft

sample_freq = 8000
nyquist_freq = sample_freq/2
num_samples = len(data_list)

data_fft = fft(data_list)
filtered_fft = fft(filtered_list)

wf = np.linspace(0, nyquist_freq, num_samples/2)
plt.semilogy(wf[1:num_samples/2], 2.0/num_samples * np.abs(data_fft[1:num_samples/2]))
plt.semilogy(wf[1:num_samples/2], 2.0/num_samples * np.abs(filtered_fft[1:num_samples/2]))

plt.show()
#"""

