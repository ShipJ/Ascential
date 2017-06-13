import pandas as pd
import numpy as np
from scipy import interpolate
import sys
import matplotlib.pyplot as plt
import math

pd.set_option('display.width', 320)

from Code.config import get_path, get_pwd

PATH = get_path()


X_MIN, X_MAX, Y_MIN, Y_MAX = 0, 3000, 0, 1000
tile_size = 100





# Construct event arena of specific size
a = EventArena(X_MIN, X_MAX, Y_MIN, Y_MAX, 100)
tiles = a.enum_tiles()



# Load sensor data
id1 = np.load('id1_next.npy')
# Grab sensor locations
sensor_coords = pd.DataFrame(pd.read_csv(PATH.replace('BLE/Data', 'Location/', 1) + '/sensor_coords.txt',
                                         sep='\t',
                                         usecols=['id_location', 'x', 'y']))

my = [2580, 2564, 2572, 2508, 2528, 2604, 2560, 2556, 2496, 2584, 2548, 2524, 2512, 2592,
      2600, 2576, 2516, 2484, 2532, 2588, 2568, 2540, 2492, 2544, 2480, 2500, 2536, 2596, 2608]
sensor_coords = sensor_coords[sensor_coords['id_location'].isin(my)]


b = [mapper[i] for i in id1]

diff = [1 for i in range(len(id1))]


def meannext(i):
    if len(i) > 2:
        return [np.mean(i[:, 0]), np.mean(i[:, 1])]
    else:
        return i


mean_next = []
for i in range(len(id1)):
    mean_next.append(meannext(b[i]))

w_avg = [mean_next[0]]
for i in range(len(b) - 1):
    conf = (1. / (1 + diff[i]))
    w_avg.append(np.multiply(conf, mean_next[i]) + np.multiply(1 - conf, mean_next[i + 1]))

x = np.array([i[0] for i in w_avg])
y = np.array([i[1] for i in w_avg])

w = [i[0] for i in mean_next]
z = [i[1] for i in mean_next]

noise = np.divide(np.random.normal(0, 1, len(x)), 1000.)
x += noise
y += noise

tck, u = interpolate.splprep([x, y], s=0)

xi, yi = interpolate.splev(np.linspace(0, 1, 1000), tck)

fig, ax = plt.subplots(1, 1)
plt.xlim([0, 3000]), plt.ylim([0, 1000])
ax.plot(x, y, 'or')
ax.plot(xi, yi, '-b')
plt.scatter(sensor_coords.x, sensor_coords.y, marker='x')
for loc, i,j in zip(sensor_coords['id_location'], sensor_coords['x'], sensor_coords['y']):
    ax.annotate('%s' % loc, xy=(i, j), xytext=(0, 0), textcoords='offset points')
plt.show()


print np.unique(id1)
























