import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy.signal import butter, lfilter, ellip
from scipy.signal import freqz
import pylab


def robs_lfilter(b, a, x):
    print 'b'
    print b
    print 'a'
    print a
    lenx = len(x)
    print 'lenx'
    print lenx
    y = [0 for i in range(0,lenx)]
    for n in range(2,lenx):
        #print n
        y[n] = (b[0]*x[n] + b[1]*x[n-1] + b[2]*x[n-2] - a[1]*y[n-1] -a[2]*y[n-2])/2
    return y

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def elliptic_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = ellip(order, 5, 40, [low, high], btype='band')
    return b, a

def elliptic_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = ellip(order, 5, 40, [lowcut, highcut], 'bandpass', analog=True)
    y = lfilter(b, a, data)
    return y

data = np.genfromtxt('data.txt', delimiter=', ', names=True, skiprows=2)
list_data = [list(row) for row in data]
matt = np.mat(list_data)

array_matt1 = np.array(matt[:,1])

data_2d_list = []
fft_2d_list = []

num_columns = 5

num_samples = len(array_matt1)

sample_freq = 8000
#sample_freq = 44100
nyquist_freq = sample_freq / 2

#plt.figure(1)
wf = np.linspace(0.0, nyquist_freq, num_samples/2)
for j in range(0,num_columns,1):
    #if j not in data_2d_list:
    data_2d_list.append([])
    array_matt = np.array(matt[:,j])
    for i,row in enumerate(array_matt):
        for element in row:
            data_2d_list[j].append(element)
    if j not in fft_2d_list:
        fft_2d_list.append([])
    fft_temp_list = fft(data_2d_list[j])
    for i,element in enumerate(fft_temp_list):
        fft_2d_list[j].append(element)
    #if j != 0:
	#plt.plot(data_2d_list[j], label = str(j))
	#if j != 5:
	    #plt.plot(data_2d_list[j], label = str(j))
	    #plt.semilogy(wf, 2.0/num_samples * np.abs(fft_2d_list[j][0:num_samples/2]), label = str(j))

#pylab.figure(figsize=(12,12))
#ax1 = pylab.subplot(2,2,1)
#ax1.set_title('Original Audio')
#for j in [1,2]:
    #plt.plot(data_2d_list[j], label = str(j))

#ax2 = pylab.subplot(2,2,2)
#ax2.set_title('Unmoved Fitered Audio')
#for j in [3,4]:
    #plt.plot(data_2d_list[j], label = str(j))

#ax3 = pylab.subplot(2,2,3)
#ax3.set_title('Correct Phase Shift')
#for j in [3,5]:
    #plt.plot(data_2d_list[j], label = str(j))

#ax4 = pylab.subplot(2,2,4)
#ax4.set_title('Filtered Phase Shift')
#for j in [3,6]:
    #plt.plot(data_2d_list[j], label = str(j))


pylab.figure(figsize=(12,12))
ax1 = pylab.subplot(2,1,1)
ax1.set_title('Original Audio')
plt.plot(data_2d_list[3], label = str(j))
#plt.plot(data_2d_list[5], label = str(j))

ax2 = pylab.subplot(2,1,2)
ax2.set_title('Unmoved Fitered Audio')
plt.plot(data_2d_list[4], label = str(j))


summer = 0
for item in fft_2d_list[2]:
    summer += np.abs(item)

print summer

#lowcut = 3000.0
#highcut = 4000.0

#y1 = butter_bandpass_filter(data_2d_list[1], lowcut, highcut, sample_freq, order=5)
#y2 = butter_bandpass_filter(data_2d_list[2], lowcut, highcut, sample_freq, order=5)
#e1 = elliptic_bandpass_filter(data_2d_list[1], lowcut, highcut, sample_freq, order=3)
#e2 = elliptic_bandpass_filter(data_2d_list[2], lowcut, highcut, sample_freq, order=3)



##plt.plot(y1, label = 'y1')
##plt.plot(y2, label = 'y2')
#y1fft = fft(y1)
#y2fft = fft(y2)
#e1fft = fft(e1)
#e2fft = fft(e2)
#plt.semilogy(wf, 2.0/num_samples * np.abs(y1fft[0:num_samples/2]), label = 'y1')
#plt.semilogy(wf, 2.0/num_samples * np.abs(y2fft[0:num_samples/2]), label = 'y2')
#plt.semilogy(wf, 2.0/num_samples * np.abs(e1fft[0:num_samples/2]), label = 'e1')
#plt.semilogy(wf, 2.0/num_samples * np.abs(e2fft[0:num_samples/2]), label = 'e2')

#plt.title('Microphone response')
#plt.xlabel('Sample')
#plt.ylabel('Voltage')
#plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
#plt.grid()

#plt.figure(2)
#plt.clf()
#for order in [3, 4, 5]:
    #b, a = butter_bandpass(lowcut, highcut, sample_freq, order=order)
    #w, h = freqz(b, a, worN=2000)
    #plt.plot((sample_freq * 0.5 / np.pi) * w, abs(h), label="bp order = %d" % order)
    #b, a = elliptic_bandpass(lowcut, highcut, sample_freq, order=order)
    #w, h = freqz(b, a, worN=2000)
    #plt.plot((sample_freq * 0.5 / np.pi) * w, abs(h), label="ellip order = %d" % order)

#plt.plot([0, 0.5 * sample_freq], [np.sqrt(0.5), np.sqrt(0.5)],
         #'--', label='sqrt(0.5)')
#plt.xlabel('Frequency (Hz)')
#plt.ylabel('Gain')
#plt.grid(True)
#plt.legend(loc='best')

plt.show()
