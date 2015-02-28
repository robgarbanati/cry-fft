import Image
import os
from numpy import corrcoef, sum, log, arange
from numpy.random import rand
#from pylab import pcolor, show, colorbar, xticks, yticks
from pylab import *
from matplotlib.colors import LogNorm


data = np.genfromtxt('data.txt', delimiter=' ', names=True, skiprows=2)
list_data = [list(row) for row in data]
matt = np.mat(list_data)
m,n = shape(matt)
#print np.transpose(matt)

#data_2d_list = []
#for j in range(0,n,1):
    ##if j not in data_2d_list:
    #data_2d_list.append([])
    #array_matt = np.array(matt[:,j])
    #for i,row in enumerate(array_matt):
        #for element in row:
            #data_2d_list[j].append(element)
    ##data_2d_list[j] = np.transpose(data_2d_list[j])
    #print 'data_2d_list[%g]' % j
    #print data_2d_list[j]

print 'matt'
print np.array(matt[:,range(0,n-1)])
fixed_array = np.array(matt[:,range(0,n-1)])
#print type(data_2d_list)
#figure(figsize=(12,12))
#subplot(2,1,1)
#pcolor(fixed_array)
#colorbar()

#subplot(2,1,2)
#pcolor(np.array(fixed_array), norm=LogNorm(vmin=fixed_array.min(), vmax=fixed_array.max()))
#colorbar()
#yticks(arange(0.5,10.5),range(0,10))
#xticks(arange(0.5,10.5),range(0,10))
#savefig('left2right_wider.png', format='png')
#Image.open('left2right_wider.png').save('left2right_wider.jpg','JPEG')
#os.remove('left2right_wider.png')
show()
