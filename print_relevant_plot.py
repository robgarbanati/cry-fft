import scipy.io.wavfile
import time
import numpy as np
import matplotlib.pyplot as plt
import pylab
from scipy.signal import butter, lfilter, iirdesign
from pylab import *
import scipy.signal as signal
from scipy.fftpack import fft, ifft

def FIR_bandpass_filter(data, lowcut, highcut):
    d = initialize_FIR_BP_filter(lowcut)
    print 'd'
    print d
    y = scipy.signal.convolve(data, d)
    #print 'FIRy'
    #print y
    return y

def initialize_FIR_BP_filter(lowcut):
    n = 1280
    #Lowpass filter
    a = signal.firwin(n, cutoff = lowcut, window = ('kaiser', 1.0))
    for i,number in enumerate(a):
	if abs(number) < 1e-15:
	    a[i] = 0

    ##Highpass filter with spectral inversion
    #b = - signal.firwin(n, cutoff = 0.225, window = ('kaiser', 1.0)); b[n/2] = b[n/2] + 1
    #for i,number in enumerate(b):
	#if abs(number) < 1e-15:
	    #b[i] = 0

    #FIR_filt = - (a+b); FIR_filt[n/2] = FIR_filt[n/2] + 1
    #print 'FIR_filt'
    #print FIR_filt
    #return FIR_filt
    return a

def robs_lfilter(b, a, x):
    max_asum = 0
    max_bsum = 0
    lenx = len(x)
    #lenx = 13
    y = [0 for i in range(0,lenx)]
    for n in range(0,lenx):
	bsum = 0
	asum = 0
	#print 'n %g' % n
	for nb,num in enumerate(b):
	    #print 'nb %g' % nb
	    if (n-nb) < 0:
		bsum += 0
		#print 'b[%g] %g, x[%g] %g, term %g, bsum %g' % (nb, b[nb], n-nb, 0, 0, bsum)
	    else:
		bsum += b[nb]*x[n-nb]
		#print 'b[%g] %g, x[%g] %g, term %g, bsum %g' % (nb, b[nb], n-nb, x[n-nb], b[nb]*x[n-nb], bsum)
	for na,num in enumerate(a[1:]):
	    rna = na+1
	    if (n-rna) < 0:
		asum += 0
		#print 'a[%g] %g, y[%g] %g, term %g, asum %g' % (rna, a[rna], n-rna, 0, 0, asum)
	    else:
		asum += a[rna]*y[n-rna]
		#print 'a[%g] %g, y[%g] %g, term %g, asum %g' % (rna, a[rna], n-rna, y[n-rna], a[rna]*y[n-rna], asum)
	    #print 'term %g' % a[rna]*y[n-rna]
	y[n] = int(((int(bsum) - int(asum)) / int(a[0])))
	if max_asum < asum:
	    max_asum = asum
	if max_bsum < bsum:
	    max_bsum = bsum
	#print 'bsum %.1f asum %.1f y[%g] %.1f' % (bsum, asum, n, y[n])
	#print 'y[%g] %g' % (n, y[n])

    print 'max %g %g' % (max_asum, max_bsum)
    return y

#a[0]*y[n] = b[0]*x[n] + b[1]*x[n-1] + ... + b[nb]*x[n-nb]
                        #- a[1]*y[n-1] - ... - a[na]*y[n-na]

def makegraph(data, filename):
    plt.clf()
    plt.plot(data)
    plt.savefig(filename)

def ellip_bandpass_filter(data):
    #print data
    print type(data[1])
    bgain = 100000000
    again = 100000000
    #lowcut = 2000.0
    #highcut = 2300.0
    lowcut = 1000.0
    highcut = 2300.0
    passband = [lowcut/4000, highcut/4000]
    stopband = [lowcut*0.8/4000, highcut*1.2/4000]
    #passband = [lowcut*2/45714, highcut*2/45714]
    #stopband = [lowcut*2*0.6/45714, highcut*2*1.4/45714]
    print 'passband'
    print passband
    print 'stopband'
    print stopband
    #b,a = iirdesign(wp = [0.2, 0.225], ws= [0.19, 0.23], gstop= 50, gpass=6, ftype='ellip') # 8000 hz version
    b,a = iirdesign(wp = passband, ws= stopband, gstop= 40, gpass=6, ftype='ellip') # 8000 hz version
    #b,a = iirdesign(wp = 0.25, ws= 0.30, gstop= 50, gpass=6, ftype='ellip') # 8000 hz version
    #b,a = iirdesign(wp = 0.046, ws= 0.055, gstop= 50, gpass=6, ftype='ellip') # 44100 hz version
    #b,a = iirdesign(wp = 0.033, ws= 0.041, gstop= 50, gpass=6, ftype='ellip') # 44100 hz version
    #b,a = iirdesign(wp = [0.61, 0.67], ws= [0.63, 0.65], gstop= 50, gpass=6, ftype='ellip') # notch
    for i,number in enumerate(b):
	if abs(number) < 1e-15:
	    b[i] = 0
	else:
	    b[i] = int(number*bgain)
    for i,number in enumerate(a):
	if abs(number) < 1e-15:
	    a[i] = 0
	else:
	    a[i] = int(number*again)
    print 'int64_t a[] = ',
    print '{',
    for num in a:
        print '%g,' % num,
    print '\b\b };'
    print 'int64_t b[] = ',
    print '{',
    for num in b:
        print('%g,' % num),
    print '\b\b };'
    print len(a)
    print len(b)
    y = robs_lfilter(b, a, data)
    #for i,num in enumerate(y):
	#y[i] = y[i]/100000000
	#y[i] = y[i]
    return y

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_lowpass(lowcut, order=5):
    b, a = butter(order, lowcut, btype='low')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_lowpass_filter(data, lowcut, order=5):
    b, a = butter_lowpass(lowcut, order=order)
    y = lfilter(b, a, data)
    return y



data = np.genfromtxt('workdocuments/data.txt', delimiter=', ', names=True, skiprows=5)
list_data = [list(row) for row in data]
matt = np.mat(list_data)

array_matt1 = np.array(matt[:,1])

data_2d_list = []
fft_2d_list = []

num_columns = 3

num_samples = len(array_matt1)

sample_freq = 8000
#sample_freq = 45714
nyquist_freq = sample_freq / 2

wf = np.linspace(0.0, nyquist_freq, num_samples/2)
for j in range(0,num_columns,1):
    #if j not in data_2d_list:
    data_2d_list.append([])
    array_matt = np.array(matt[:,j])
    for i,row in enumerate(array_matt):
        for element in row:
	    data_2d_list[j].append(int64(element*100000000))
    fft_2d_list.append([])
    fft_temp_list = fft(data_2d_list[j])
    for i,element in enumerate(fft_temp_list):
        fft_2d_list[j].append(element)
    if j != 0:
	#plt.plot(data_2d_list[j], label = str(j))
	#plt.semilogy(wf, 2.0/num_samples * np.abs(fft_2d_list[j][0:num_samples/2]), label = str(j))
    #if j in [1,2]:
	#plt.plot(data_2d_list[j], label = str(j))
        plt.semilogy(wf, 2.0/num_samples * np.abs(fft_2d_list[j][0:num_samples/2]), label = str(j))
	#for i,sample in enumerate(data_2d_list[j]):
	    #data_2d_list[j][i] = data_2d_list[j][i]*100000000
	filtered_snippet = ellip_bandpass_filter(data_2d_list[j])
	#filtered_snippet = FIR_bandpass_filter(data_2d_list[j], 0.1, 0.2)
	#filtered_snippet = butter_lowpass_filter(data_2d_list[j], 0.3, 2)
	fft_filtered_snippet = fft(filtered_snippet)
	#plt.plot(filtered_snippet)
        #plt.semilogy(wf, 2.0/num_samples * np.abs(fft_filtered_snippet[0:num_samples/2]), label = str(j))

plt.show()



