import scipy.io.wavfile
import time
import numpy as np
import matplotlib.pyplot as plt
import pylab
from scipy.signal import butter, lfilter, iirdesign
from pylab import *
import scipy.signal as signal
from scipy.fftpack import fft, ifft

def fir_bandpass_filter(data, lowcut, highcut):
    d = initialize_fir_bp_filter(lowcut)
    print 'd'
    print d
    y = scipy.signal.convolve(data, d)
    #print 'firy'
    #print y
    return y

def initialize_fir_bp_filter(lowcut):
    n = 1280
    #lowpass filter
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

#def ellip_bandpass_filter(data):
    #b,a = iirdesign(wp = 0.046, ws= 0.055, gstop= 50, gpass=6, ftype='ellip') # 44100 hz version
    #y = robs_lfilter(b, a, data)
    ##y = lfilter(b, a, data)
    #return y

def ellip_bandpass_filter(data):
    #print data
    print type(data[1])
    bgain = 100000000
    again = 100000000
    #b,a = iirdesign(wp = [0.2, 0.225], ws= [0.19, 0.23], gstop= 50, gpass=6, ftype='ellip') # 8000 hz version
    #b,a = iirdesign(wp = [0.25, 0.75], ws= [0.23, 0.77], gstop= 50, gpass=6, ftype='ellip') # 8000 hz version
    #b,a = iirdesign(wp = 0.25, ws= 0.30, gstop= 50, gpass=6, ftype='ellip') # 8000 hz version
    b,a = iirdesign(wp = 0.046, ws= 0.055, gstop= 50, gpass=6, ftype='ellip') # 44100 hz version
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
    #y = lfilter(b, a, data)
    #for i,num in enumerate(y):
	#y[i] = y[i]/100000000
	#y[i] = y[i]
    return y



pylab.figure(figsize=(12,9))
data = np.genfromtxt('test.txt', delimiter=', ', names=True, skiprows=0)
#print data
#list_data = [list(row) for row in data]
list_data = []
#print list_data
for i,row in enumerate(data):
    for element in row:
	list_data.append(element*100000000)

filtered_data = ellip_bandpass_filter(list_data)
#filtered_data = fir_bandpass_filter(list_data, 0.1, 0.2)
#filtered_data = butter_lowpass_filter(list_data, 0.1, 1)

fft_data = fft(list_data)
fft_filtered_data = fft(filtered_data)

num_samples = len(data)
sample_freq = 44100
nyquist_freq = sample_freq / 2

wf = np.linspace(0.0, nyquist_freq, num_samples/2)
#plt.plot(list_data, label = 'list_data')
#plt.plot(filtered_data, label = 'filtered_data')
plt.semilogy(wf, 2.0/num_samples * np.abs(fft_data[0:num_samples/2]), label = 'list_data')
plt.semilogy(wf, 2.0/num_samples * np.abs(fft_filtered_data[0:num_samples/2]), label = 'filtered_data')

plt.show()

