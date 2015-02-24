import scipy.io.wavfile
import time
import numpy as np
import matplotlib.pyplot as plt
import pylab
from scipy.signal import butter, lfilter, iirdesign

def makegraph(data, filename):
    plt.clf()
    plt.plot(data)
    plt.savefig(filename)


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a



def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    #b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    #b,a = iirdesign(wp = [0.027, 0.045], ws= [0.022, 0.050], gstop= 50, gpass=6, ftype='ellip')
    b,a = iirdesign(wp = [0.036, 0.041], ws= [0.031, 0.046], gstop= 50, gpass=6, ftype='ellip')

    print 'b'
    print b
    print 'a'
    print a
    y = lfilter(b, a, data)
    #robs_y = robs_lfilter(b, a, data)
    #plt.plot(t, y, label='lfiltered signal (%g Hz)' % f0)
    #plt.plot(t, robs_y, label='robs_lfiltered signal (%g Hz)' % f0)
    return y


sound_tup = scipy.io.wavfile.read('/mnt/hgfs/vmware_share/Unacuna Cry Analyzer Tests/short rohan.wav', 'r')
#sound_tup = scipy.io.wavfile.read('/mnt/hgfs/vmware_share/modded baby sound effect.wav', 'r')
#sound_tup = scipy.io.wavfile.read('/mnt/hgfs/vmware_share/Unacuna Cry Analyzer Tests/short pearl.wav', 'r')
#sound_tup = scipy.io.wavfile.read('/mnt/hgfs/vmware_share/Unacuna Cry Analyzer Tests/short ben.wav', 'r')
#sound_tup = scipy.io.wavfile.read('/mnt/hgfs/vmware_share/Unacuna Cry Analyzer Tests/short ben 8 bit 8000.wav', 'r')
#sound_tup = scipy.io.wavfile.read('/mnt/hgfs/vmware_share/Unacuna Cry Analyzer Tests/short rohan 8 bit 8000.wav', 'r')

#print sound_tup[1]
sound_data = list(sound_tup[1])
print len(sound_data)
#print sound_tup[1][1][1]

#sound_data = []

#for i,row in enumerate(sound_tup[1]):
    #sound_data.append(row[0])


from scipy.fftpack import fft, ifft

#plt.ion()
#plt.show()

snippet_length = 1600
num_samples = snippet_length
sample_freq = 44100
#sample_freq = 8000
nyquist_freq = sample_freq / 2


#time_of_interest = 0.319
#ben_times_of_interest = [0.299, 2.105, 3.422, 5.104, 9.160, 9.786, 10.742, 6.935, 7.020, 7.078, 7.161]
rohan_times_of_interest = [1.6880, 2.953, 5.468, 5.790, 6.756, 7.307, 7.493, 7.522, 7.593, 7.629]
#rohan_times_of_interest = [1.6880]
times_of_interest = rohan_times_of_interest
#sample_of_interest = (int) (sample_freq*time_of_interest)
samples_of_interest = [(int) (x*sample_freq - snippet_length/2) for x in times_of_interest]
#samples_of_interest = (x*sample_freq) for x in times_of_interest

i = 44100*7.90
#for i in range(sample_of_interest - snippet_length/2, sample_of_interest - snippet_length/2, snippet_length/8):
for i in samples_of_interest:
    #print i
    sound_data_snippet = sound_data[i:i+snippet_length]
    filtered_snippet = butter_bandpass_filter(sound_data_snippet, 2000, 2900, 5)
    fft_of_sound = fft(sound_data_snippet)
    fft_of_filtered_sound = fft(filtered_snippet)
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
	plt.semilogy(wf[1:num_samples/2], 2.0/num_samples * np.abs(fft_of_sound[1:num_samples/2]))
	plt.semilogy(wf[1:num_samples/2], 2.0/num_samples * np.abs(fft_of_filtered_sound[1:num_samples/2]))
    except ValueError:
	print "not plotting because data is all zeroes"
    pylab.xlim([0,12000])
    #pylab.xlim([500,1500])
    plt.grid()


#plt.show()

