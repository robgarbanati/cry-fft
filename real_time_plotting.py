import time
import numpy as np
import matplotlib.pyplot as plt

#plt.axis([0, 1000, 0, 1])
#plt.ion()
#plt.show()

fig, ax = plt.subplots(1, 1)
ax.set_aspect('equal')
ax.set_xlim(0, 255)
ax.set_ylim(0, 255)
ax.hold(True)

plt.show(False)
plt.draw()

x = 1
y = 1

points = ax.plot(x, y, 'o')[0]
tic = time.time()

niter = 254
for ii in xrange(niter):
    x, y = np.random.random()*255, np.random.random()*255
    points.set_data(x, y)
    # redraw everything
    fig.canvas.draw()

plt.close(fig)
