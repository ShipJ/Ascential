import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from final import sensor_coords
from Code.config import get_path
import math


PATH = get_path()

# sensor_coords = sensor_coords(PATH, data)


mymap = {0: np.array([250, 125]), 1: np.array([250, 375]), 2: np.array([250, 625]), 3: np.array([250, 875]),
         4: np.array([750, 125]), 5: np.array([750, 375]), 6: np.array([750, 625]), 7: np.array([750, 875]),
         8: np.array([1250, 125]), 9: np.array([1250, 375]), 10: np.array([1250, 625]), 11: np.array([1250, 875]),
         12: np.array([1750, 125]), 13: np.array([1750, 375]), 14: np.array([1750, 625]), 15: np.array([1750, 875]),
         16: np.array([2250, 125]), 17: np.array([2250, 375]), 18: np.array([2250, 625]), 19: np.array([2250, 875]),
         20: np.array([2750, 125]), 21: np.array([2750, 375]), 22: np.array([2750, 625]), 23: np.array([2750, 875])}


a = np.array([0, 1, 1, 2, 3, 7, 7, 2, 3, 7, 6, 5, 5, 9, 9, 10, 11, 15, 19, 23, 19, 23, 22, 21, 17, 20, 16, 16])
b = [mymap[i] for i in a]

diff = [1 for i in range(len(a))]

def meannext(i):
    if len(i) > 2:
        return [np.mean(i[:, 0]), np.mean(i[:, 1])]
    else:
        return i

mean_next = []
for i in range(len(a)):
    mean_next.append(meannext(b[i]))


w_avg = [mean_next[0]]
for i in range(len(b)-1):
    conf = (1./(1+diff[i]))
    w_avg.append(np.multiply(conf, mean_next[i]) + np.multiply(1 - conf, mean_next[i+1]))

x = np.array([i[0] for i in w_avg])
y = np.array([i[1] for i in w_avg])

w = [i[0] for i in mean_next]
z = [i[1] for i in mean_next]

names = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12']


import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt

noise = np.divide(np.random.normal(0, 1, len(x)), 1000.)
x+= noise
y+= noise

tck,u = interpolate.splprep([x, y], s=0)


xi, yi = interpolate.splev(np.linspace(0, 1, 1000), tck)

fig, ax = plt.subplots(1, 1)
ax.plot(x, y, 'or')
ax.plot(xi, yi, '-b')
plt.show()

# X_MIN, X_MAX, Y_MIN, Y_MAX = 0, 3000, 0, 1000
# tile_size = 100
#
#
# class Tile:
#     def __init__(self, tl, br, tile_size):
#         self.tl = tl
#         self.br = br
#         self.tile_size = tile_size
#     def centre(self):
#         return Point(self.tl[0]+self.tile_size/2., self.tl[1]-self.tile_size/2.)
#
#
# class Point:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#
# class EventArena:
#     def __init__(self, x_min, x_max, y_min, y_max, tile_size):
#         self.x_min = x_min
#         self.x_max = x_max
#         self.y_min = y_min
#         self.y_max = y_max
#         self.tile_size = tile_size
#     def enum_tiles(self):
#         ts = self.tile_size
#         tiles = []
#         for i in range(self.x_min, self.x_max, ts):
#             for j in range(self.y_min, self.y_max, ts):
#                 tiles.append(Tile((i, j+ts), (i+ts, j), ts))
#         return tiles
#     def num_tiles(self):
#         return (self.x_max/self.tile_size) * (self.y_max / self.tile_size)
#     def point_in_tile(self, point):
#         return int(((self.y_max/self.tile_size)*math.floor(point.x/self.tile_size))+math.floor(point.y/self.tile_size))
#
#
# a = EventArena(0, 3000, 0, 1000, 100)
# tiles = a.enum_tiles()













