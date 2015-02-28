import matplotlib.pyplot as plt
import numpy as np

#w, x, y, z, a, b, c, i, j, k = np.loadtxt('test.txt', dtype=int, delimiter=', ',
        #unpack=True, usecols=(0,1,2,3), skiprows=3)

#w, x, y, z, a, b, c = np.loadtxt('test.txt', dtype=int, delimiter=', ',
        #unpack=True, usecols=(0,1,2,3,4,5,6), skiprows=4)

#w, x, y, z, k, l = np.loadtxt('test.txt', dtype=int, delimiter=', ',
        #unpack=True, usecols=(0,1,2,3,4,5), skiprows=2)

w, x, y, z, k = np.loadtxt('test.txt', dtype=int, delimiter=', ',
        unpack=True, usecols=(0,1,2,3,4), skiprows=4)

#w, x, y, z = np.loadtxt('test.txt', dtype=int, delimiter=', ',
        #unpack=True, usecols=(0,1,2,3), skiprows=2)

#w, x, y = np.loadtxt('test.txt', dtype=int, delimiter=', ',
        #unpack=True, usecols=(0,1,2), skiprows=3)

plt.plot(w, x, label = 'A')
plt.plot(w, y, label = 'B')
plt.plot(w, z, label = 'BPA')

#plt.plot(w, a, label = 'BPA')
#plt.plot(w, b, label = 'BPB')
#plt.plot(w, c, label = 'BPC')

#plt.plot(w, i, label = 'A')
#plt.plot(w, j, label = 'B')
plt.plot(w, k, label = 'BPB')

#plt.plot(w[100:200], x[100:200], label = 'A')
#plt.plot(w[100:200], y[100:200], label = 'B')
#plt.plot(w[100:200], z[100:200], label = 'C')

plt.title('Microphone response')
plt.xlabel('Sample')
plt.ylabel('Voltage')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

plt.show()
