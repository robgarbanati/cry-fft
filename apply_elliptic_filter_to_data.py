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

    print 'max %g %g' % (max_asum, max_bsum)
    return y

#def ellip_bandpass_filter(data):
    #b,a = iirdesign(wp = 0.046, ws= 0.055, gstop= 50, gpass=6, ftype='ellip') # 44100 hz version
    ##y = robs_lfilter(b, a, data)
    #y = lfilter(b, a, data)
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
        print '%.0f,' % num,
    print '\b\b };'
    print 'int64_t b[] = ',
    print '{',
    for num in b:
        print('%.0f,' % num),
    print '\b\b };'
    print len(a)
    print len(b)
    y = robs_lfilter(b, a, data)
    #y = lfilter(b, a, data)
    #for i,num in enumerate(y):
	#y[i] = y[i]/100000000
	#y[i] = y[i]
    return y


#pylab.figure(figsize=(12,9))
#data = np.genfromtxt('workdocuments/data.txt', delimiter=', ', names=True, skiprows=3)
#list_data = [list(row) for row in data]
#matt = np.mat(list_data)

#list_data = []
#for i,row in enumerate(matt[:,1]):
    #for element in row:
	#list_data.append(int64(element*100000000))

#print 'list_data'
#print list_data
#summer = 0
#for i,row in enumerate(list_data):
    #summer += row
#average = summer/len(list_data)
#print 'average'
#print average
#for i,row in enumerate(list_data):
    #list_data[i] -= average

#filtered_data = ellip_bandpass_filter(list_data)

#fft_data = fft(list_data)
#fft_filtered_data = fft(filtered_data)

#num_samples = len(list_data)
#print 'num_samples'
#print num_samples
#sample_freq = 44100
#nyquist_freq = sample_freq / 2

#wf = np.linspace(0.0, nyquist_freq, num_samples/2)
##plt.plot(list_data)
##plt.plot(filtered_data)
#plt.semilogy(wf, 2.0/num_samples * np.abs(fft_data[0:num_samples/2]), label = 'list_data')
#plt.semilogy(wf, 2.0/num_samples * np.abs(fft_filtered_data[0:num_samples/2]), label = 'fft_data')


# dynamic version
data = np.genfromtxt('workdocuments/data.txt', delimiter=', ', names=True, skiprows=3)
list_data = [list(row) for row in data]
matt = np.mat(list_data)

data_2d_list = []
fft_2d_list = []

num_columns = 2

num_samples = len(matt)
print 'num_samples'
print num_samples

sample_freq = 44100
nyquist_freq = sample_freq / 2

wf = np.linspace(0.0, nyquist_freq, num_samples/2)
for j in range(0,num_columns,1):
    summer = 0
    #if j not in data_2d_list:
    data_2d_list.append([])
    array_matt = np.array(matt[:,j])
    for i,row in enumerate(array_matt):
	for element in row:
	    data_2d_list[j].append(int64(element*100000000))
	    summer += data_2d_list[j][i]
    average = summer/len(data_2d_list[j])
    for i,row in enumerate(data_2d_list[j]):
	data_2d_list[j][i] -= average
    fft_2d_list.append([])
    fft_temp_list = fft(data_2d_list[j])
    for i,element in enumerate(fft_temp_list):
	fft_2d_list[j].append(element)
    #if j != 0:
	#plt.plot(data_2d_list[j], label = str(j))
	#plt.semilogy(wf, 2.0/num_samples * np.abs(fft_2d_list[j][0:num_samples/2]), label = str(j))
    if j in [1,2]:
	##plt.plot(data_2d_list[j], label = str(j))
	plt.semilogy(wf, 2.0/num_samples * np.abs(fft_2d_list[j][0:num_samples/2]), label = str(j))
	#for i,sample in enumerate(data_2d_list[j]):
	    #data_2d_list[j][i] = data_2d_list[j][i]*100000000
	filtered_snippet = ellip_bandpass_filter(data_2d_list[j])
	fft_filtered_data = fft(filtered_snippet)
	#plt.plot(filtered_snippet)
	plt.semilogy(wf, 2.0/num_samples * np.abs(fft_filtered_data[0:num_samples/2]), label = str(j))


plt.show()

