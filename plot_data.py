import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft

data = np.genfromtxt('data.txt', delimiter=', ', names=True, skiprows=4)
list_data = [list(each) for each in data]
matt = np.mat(list_data)
columns = []

for i,row in enumerate(list_data):
    for element in row:
	if i not in columns:
	   columns.append([])
	columns[i].append(element)


#print data[0][1]
#print data
#print data[:2]

#plt.plot(matt[:,1])
#plt.plot(matt[:,2])
#plt.plot(matt[:,3])
#plt.ylabel('some numbers')

fft_matt1 = fft(matt[:,1])
fft_matt2 = fft(matt[:,2])
fft_matt3 = fft(matt[:,3])

#plt.plot(fft_matt1)
#plt.plot(fft_matt2)
#plt.plot(fft_matt3)
#plt.show()


from scipy.fftpack import fft
# Number of samplepoints
N = fft_matt1

# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, N*T, N)
y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
yf = fft(y)
xf = np.linspace(0.0, 45714/2.0, N/2)
import matplotlib.pyplot as plt
plt.plot(xf, 2.0/N * np.abs(yf[0:N/2]))
plt.grid()
plt.show()
