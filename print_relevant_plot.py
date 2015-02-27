import scipy.io.wavfile
import time
import numpy as np
import matplotlib.pyplot as plt
import pylab
from scipy.signal import butter, lfilter, iirdesign
from pylab import *
import scipy.signal as signal
from scipy.fftpack import fft, ifft


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

	#y[n] = (b*x - a*y)/2
	#y[n] = (b[0]*x[n] + b[1]*x[n-1] + b[2]*x[n-2] - a[1]*y[n-1] -a[2]*y[n-2])/2
    print 'max %g %g' % (max_asum, max_bsum)
    return y

#a[0]*y[n] = b[0]*x[n] + b[1]*x[n-1] + ... + b[nb]*x[n-nb]
                        #- a[1]*y[n-1] - ... - a[na]*y[n-na]

def makegraph(data, filename):
    plt.clf()
    plt.plot(data)
    plt.savefig(filename)

def ellip_bandpass_filter(data):
    bgain = 100000000
    again = 100000000
    b,a = iirdesign(wp = [0.2, 0.225], ws= [0.19, 0.23], gstop= 50, gpass=6, ftype='ellip') # 8000 hz version
    for i,number in enumerate(b):
	if abs(number) < 1e-15:
	    b[i] = 0
	else:
	    #b[i] = round(number,8)
	    b[i] = int(number*bgain)
    for i,number in enumerate(a):
	if abs(number) < 1e-15:
	    a[i] = 0
	else:
	    #a[i] = round(number,8)
	    a[i] = int(number*again)
    #y = lfilter(b, a, data)
    #return y
    y = robs_lfilter(b, a, data)
    for i,num in enumerate(y):
	y[i] = y[i]/100000000
    #for i,num in enumerate(y):
    #for i in range(0,10):
	#print 'y\t%g\t%g' % (y[i], robs_y[i])
    return y






def FIR_bandpass_filter(data, lowcut, highcut):
    y = scipy.signal.convolve(data, d)
    print 'FIRy'
    print y
    return y

def initialize_FIR_BP_filter():
    n = 63
    #Lowpass filter
    a = signal.firwin(n, cutoff = 0.2, window = ('kaiser', 1.0))
    for i,number in enumerate(a):
	if abs(number) < 1e-15:
	    a[i] = 0

    #Highpass filter with spectral inversion
    b = - signal.firwin(n, cutoff = 0.225, window = ('kaiser', 1.0)); b[n/2] = b[n/2] + 1
    for i,number in enumerate(b):
	if abs(number) < 1e-15:
	    b[i] = 0

    FIR_filt = - (a+b); FIR_filt[n/2] = FIR_filt[n/2] + 1
    #print 'FIR_filt'
    #print FIR_filt
    return FIR_filt




#sound_tup = scipy.io.wavfile.read('/mnt/hgfs/vmware_share/Unacuna Cry Analyzer Tests/short rohan.wav', 'r')
#sound_tup = scipy.io.wavfile.read('/mnt/hgfs/vmware_share/modded baby sound effect.wav', 'r')
#sound_tup = scipy.io.wavfile.read('/mnt/hgfs/vmware_share/Unacuna Cry Analyzer Tests/short pearl.wav', 'r')
#sound_tup = scipy.io.wavfile.read('/mnt/hgfs/vmware_share/Unacuna Cry Analyzer Tests/short ben.wav', 'r')
#sound_tup = scipy.io.wavfile.read('/mnt/hgfs/vmware_share/Unacuna Cry Analyzer Tests/short ben 8 bit 8000.wav', 'r')
sound_tup = scipy.io.wavfile.read('/mnt/hgfs/vmware_share/Unacuna Cry Analyzer Tests/short rohan 16 bit 8000.wav', 'r')

sound_data = list(sound_tup[1])
print len(sound_data)

snippet_length = 600
num_samples = snippet_length
sample_freq = 8000
nyquist_freq = sample_freq / 2


#ben_times_of_interest = [0.299, 2.105, 3.422, 5.104, 9.160, 9.786, 10.742, 6.935, 7.020, 7.078, 7.161]
#rohan_times_of_interest = [1.6880, 2.953, 5.468, 5.790, 6.756, 7.307, 7.493, 7.522, 7.593, 7.629]
rohan_times_of_interest = [5.790]
times_of_interest = rohan_times_of_interest
samples_of_interest = [(int) (x*sample_freq - snippet_length/2) for x in times_of_interest]

thefile = open('test.txt', 'w')

firfilt = initialize_FIR_BP_filter()

for i in samples_of_interest:
    sound_data_snippet = sound_data[i:i+snippet_length]
    for item in sound_data_snippet:
	print>>thefile, item
    for i,sample in enumerate(sound_data_snippet):
	sound_data_snippet[i] = sound_data_snippet[i]*100000000
    filtered_snippet = ellip_bandpass_filter(sound_data_snippet)
    for i,sample in enumerate(sound_data_snippet):
	sound_data_snippet[i] = sound_data_snippet[i]/100000000
    #FIR_filtered_snippet = convolve(sound_data_snippet, firfilt)
    fft_of_sound = fft(sound_data_snippet)

    fft_of_filtered_sound = fft(filtered_snippet)
    #fft_of_FIR_filtered_sound = fft(FIR_filtered_snippet)
    sum_of_filter = 0
    for number in fft_of_filtered_sound:
        sum_of_filter = sum_of_filter + np.abs(number)
    print sum_of_filter
    #print 'fft'
    #print np.abs(fft_of_filtered_sound)


    #ax = plt.subplot(1,1,1)
    wf = np.linspace(0, nyquist_freq, num_samples/2)
    #plt.cla()
    #plt.axis([0, 12000, 0, max(fft_of_sound)])
    try:
	#plt.figure(i)
	pylab.figure(figsize=(12,9))
	#plt.plot(sound_data_snippet)
	#plt.plot(filtered_snippet)
	#pylab.figure(figsize=(12,9))
	plt.semilogy(wf[1:num_samples/2], 2.0/num_samples * np.abs(fft_of_sound[1:num_samples/2]))
	plt.semilogy(wf[1:num_samples/2], 2.0/num_samples * np.abs(fft_of_filtered_sound[1:num_samples/2]))
	#plt.semilogy(wf[1:num_samples/2], 2.0/num_samples * np.abs(fft_of_FIR_filtered_sound[1:num_samples/2]))
    except ValueError:
	print "not plotting because data is all zeroes"
    pylab.xlim([0,4000])
    #pylab.xlim([500,1500])
    plt.grid()


plt.show()

