# ellip_bandpass_filter uses python modules to design an elliptic filter with specific
# attributes.
#
# robs_lfilter implements that filter and runs the data through it, returning the
# filtered data.
#
# The main code at the bottom reads data from a file, runs ellip_bandpass_filter on it,
# then produces graphs of the input and filtered result.

import scipy.io.wavfile
import time
import numpy as np
import matplotlib.pyplot as plt
import pylab
from scipy.signal import butter, lfilter, iirdesign
from pylab import *
import scipy.signal as signal
from scipy.fftpack import fft, ifft



# Create a filter of the form:
# a[0]*y[n] = b[0]*x[n] + b[1]*x[n-1] + ... + b[nb]*x[n-nb]
#                       - a[1]*y[n-1] - ... - a[na]*y[n-na]
# Run the data through this filter
def robs_lfilter(b, a, x):
    max_asum = 0
    max_bsum = 0
    lenx = len(x)
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



# run a bandpass filter on data.
def ellip_bandpass_filter(data):
    #print data

    # Make sure data type is good (int64)
    print type(data[1])

    # We want to generate ints for use in c code, so multiply results by these gains.
    bgain = 100000000
    again = 100000000

    # The passband is from lowcut to highcut.
    lowcut = 1000.0
    highcut = 2300.0
    passband = [lowcut/4000, highcut/4000]

    # Each transition band right now is 20% of the values of the cutoff frequencies.
    # The stopband is every frequency outside of the passband and transition bands.
    stopband = [lowcut*0.8/4000, highcut*1.2/4000]
    print 'passband'
    print passband
    print 'stopband'
    print stopband

    # Design an elliptic filter (A type of IIR filter with very desirable properties.
    # Butterworth and Chebyshev filters are both elliptic filters)
    # gstop is the (negative) gain of the stopband. Ex: 50 means a 50dB reduction.
    # gpass is maximum ripple in passband. Ex: 6 means maximum 6dB of ripple is allowed.
    # a and b arrays are our filters. They will be convolved with our input and
    # output data to produce our filtered data.
    b,a = iirdesign(wp = passband, ws= stopband, gstop= 50, gpass=6, ftype='ellip') # 8000 hz version

    # Turn all those almost 0 floats into hard 0s.
    # Convert each element into an int64.
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

    # Print a and b arrays as int64s in a form directly copy-able into our c file.
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

    # Run the data through our filter
    y = robs_lfilter(b, a, data)

    #for i,num in enumerate(y):
	#y[i] = y[i]/100000000
	#y[i] = y[i]


    # Return filtered data
    return y


############
### MAIN ###
############

# Both files are legitimate.
data = np.genfromtxt('workdocuments/data.txt', delimiter=', ', names=True, skiprows=5)
#data = np.genfromtxt('data.txt', delimiter=', ', names=True, skiprows=5)

# Convert the data into a numpy matrix
list_data = [list(row) for row in data]
data_mat = np.mat(list_data)

# This list will be filled in with the input and output in the time domain.
data_2d_list = []

# This list will be filled in with the input and output in the freqeuncy domain.
fft_2d_list = []

# just look at the index (zeroth) and the unfiltered data (first) columns
num_columns = 2

# generate fft variables
array_matt1 = np.array(data_mat[:,1])
num_samples = len(array_matt1)
sample_freq = 8000
nyquist_freq = sample_freq / 2

# Generate frequency domain.
wf = np.linspace(0.0, nyquist_freq, num_samples/2)


# TODO this whole loop is a mess
for j in range(0,num_columns,1):

    # data_2d_list should have as many columns as the data
    data_2d_list.append([])

    # convert each column into an array
    data_array = np.array(data_mat[:,j])
    # convert each element in the array to an int64 (multiplied by gain)
    for i,row in enumerate(data_array):
        for element in row:
	    data_2d_list[j].append(int64(element*100000000))

    # fft_2d_list should have as many columns as the data
    fft_2d_list.append([])
    # run an fft on the data
    fft_temp_list = fft(data_2d_list[j])
    # add fft of input data to fft_2d_list
    for i,element in enumerate(fft_temp_list):
        fft_2d_list[j].append(element)


    if j != 0:
        # Plot fft of input data.
        plt.semilogy(wf, 2.0/num_samples * np.abs(fft_2d_list[j][0:num_samples/2]), label = str(j))

        # This is where the magic happens: generate filtered data.
        filtered_snippet = ellip_bandpass_filter(data_2d_list[j])
        # Run an fft on filtered data
        fft_filtered_snippet = fft(filtered_snippet)

        # Plot fft of filtered data.
        plt.semilogy(wf, 2.0/num_samples * np.abs(fft_filtered_snippet[0:num_samples/2]), label = str(j))

plt.show()



