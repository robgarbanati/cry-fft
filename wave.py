import scipy.io.wavfile
import time
import numpy as np
import matplotlib.pyplot as plt

sound_tup = scipy.io.wavfile.read('/mnt/hgfs/vmware_share/Unacuna Cry Analyzer Tests/short rohan.wav', 'r')
#sound_tup = scipy.io.wavfile.read('/mnt/hgfs/vmware_share/modded baby sound effect.wav', 'r')
#sound_tup = scipy.io.wavfile.read('/mnt/hgfs/vmware_share/Unacuna Cry Analyzer Tests/short pearl.wav', 'r')

#print sound_tup[1]
sound_data = list(sound_tup[1])
print len(sound_data)
#print sound_tup[1][1][1]

#sound_data = []

#for i,row in enumerate(sound_tup[1]):
    #sound_data.append(row[0])


from scipy.fftpack import fft, ifft

plt.ion()
plt.show()

snippet_length = 1600
num_samples = snippet_length
sample_freq = 44100
nyquist_freq = sample_freq / 2
#nyquist_freq = 10000

i = 0
while i < len(sound_data):
    sound_data_snippet = sound_data[snippet_length*i:snippet_length*(i+1)]
    fft_of_sound = fft(sound_data_snippet)

    wf = np.linspace(0, nyquist_freq, num_samples/2)
    plt.cla()
    plt.axis([0, nyquist_freq, 0, max(sound_data_snippet)])
    try:
        plt.semilogy(wf[1:num_samples/2], 2.0/num_samples * np.abs(fft_of_sound[1:num_samples/2]))
    except ValueError:
        print "not plotting because data is all zeroes"
    try:
        plt.draw()
    except ValueError:
        print "not plotting because data is all zeroes"
    plt.grid()
    #plt.show()
    #time.sleep(0.05)
    i = i+1
    print i


plt.axis([0, 1000, 0, 1])
plt.ion()
plt.show()

for i in range(1000):
    y = np.random.random()
    plt.cla()
    plt.scatter(i, y)
    plt.axis([0, 1000, 0, 1])
    plt.draw()
    time.sleep(0.05)

