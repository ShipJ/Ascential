import sys
import math
import pandas as pd
import numpy as np
import clean_functions as cf
import matplotlib.pyplot as plt
import datetime as dt
from Code.config import get_path
from random import choice
from collections import Iterable

# Path to data
PATH = get_path()

# Arena dimensions (may be altered to include inaccessible regions?)
X_MIN, X_MAX = 0, 3000
Y_MIN, Y_MAX = 0, 1000

# Apply function to clean the data
ble = cf.clean_ble(PATH, pd.DataFrame(pd.read_csv(PATH+'/Processed/ble_39283.txt', sep='\t'))).dropna()

# Apply function to compute distances (in metres) from signals to beacons
ble = pd.DataFrame(cf.rssi_to_metres(ble)).sort_values('datetime').reset_index(drop=True)

# Round all times to nearest 30 seconds
ble['datetime'] = ble['datetime'].dt.round('0.5min')
ble['metres'] = pd.to_numeric(ble['metres'])
ble_round = pd.DataFrame(ble.groupby(['id', 'datetime', 'sensor'])['metres'].mean().reset_index())


ble_round = pd.DataFrame(ble_round.loc[0:5000]).sort_values('datetime')

# Grab sensor locations
sensor_coords = pd.DataFrame(pd.read_csv(PATH.replace('BLE/Data', 'Location/', 1) + '/sensor_coords.txt',
                                         sep='\t',
                                         usecols=['id_location', 'x', 'y']))
# Only get locations of sensors within the given data set
sensor_coords = sensor_coords[sensor_coords['id_location'].isin(pd.unique(ble['id_location']))].reset_index(drop=True)

# Associate sensor names with locations
name_loc = ble[['sensor', 'id_location']].drop_duplicates().sort_values('sensor').reset_index(drop=True)
sensor_coords = name_loc.merge(sensor_coords, on='id_location', how='inner')

# Granularity of the arena when split into squares of this size (in centimetres)
tile_size = 10

class Tile:
    """
    A single square of the arena of 'tile_size' width and height. 'tl' and 'br' describe the top-left and 
    bottom-right coordinates of the Tile, uniquely identifying it. The centre of the tile can also be obtained,
    returned as a Point data structure.
    """
    def __init__(self, tl, br):
        self.tl = tl
        self.br = br
    def centre(self):
        return Point(self.tl[0]+tile_size/2., self.tl[1]-tile_size/2.)

class Point:
    """
    A coordinate of a given location within the arena
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Enumerate all tiles of the arena
tiles = []
for i in range(X_MIN, X_MAX, tile_size):
    for j in range(Y_MIN, Y_MAX, tile_size):
        tiles.append(Tile((i, j+tile_size), (i+tile_size, j)))

# Return all points on the circumference of a circle with given centre-coordinates, and radius
def circum_points(r, y, z, n):
    points = [((math.cos(2*math.pi/n*x)*r+y), (math.sin(2*math.pi/n*x)*r)+z) for x in xrange(0, n+1)]
    points = [i for i in points if i[0]>X_MIN and i[0]<X_MAX]
    return [j for j in points if j[1]>Y_MIN and j[1]<Y_MAX]

def points_to_tiles(points, size):
    """
    Return all possible tiles in which a person could be based on the points given on the circle circumference
    :param points: List of Point data structures
    :param size: Set tile size
    :return: 
    """
    tiles = []
    for point in points:
        tiles.append(int((float(Y_MAX)/size)*math.floor(point.x/float(size)) + math.floor(point.y/float(tile_size))))
    return tiles

# Compute list of possible tiles
def f(x):
    points = circum_points(x[1],
                           sensor_coords[sensor_coords['sensor'] == [int(x[0])]].values[0][2],
                           sensor_coords[sensor_coords['sensor'] == [int(x[0])]].values[0][3],
                           30)
    return list(pd.unique(points_to_tiles([Point(i[0], i[1]) for i in points], tile_size)))

ble_round['poss_tiles'] = ble_round[['sensor', 'metres']].apply(f, axis=1)


def flatten(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, basestring):
            for x in flatten(item):
                yield x
        else:
            yield item

def g(x):
    if len(x) == 0:
        return x

    if len(x) == 1:
        possible = list(flatten(x.reset_index().loc[0].values[1]))
        if not possible:
            return x
        else:
            return choice(possible)

    if len(x) == 2:
        pair = list(flatten(np.intersect1d(x.reset_index().loc[0].values[1], x.reset_index().loc[1].values[1])))
        if len(pair) == 0:
            return choice(list(flatten(x)))
        elif len(pair) == 1:
            return pair[0]
        else:
            return choice(pair)

    if len(x) > 2:
        possible = list(flatten(x.reset_index().loc[0].values[1]))
        return choice(possible)


ble_round = ble_round.groupby(['id', 'datetime'])['poss_tiles'].apply(g).reset_index()


start_time = ble_round.iloc[0].datetime
new_journeys = [0]
for i in range(len(ble_round)):
    next_time = ble_round.iloc[i].datetime
    if (next_time - start_time).seconds > 600:
        new_journeys.append(i-1)
    start_time = next_time


journeys = []
for i in range(len(new_journeys)-1):
    journeys.append(ble_round.ix[new_journeys[i]+1:new_journeys[i+1]])

# Enumerate all tiles of the arena
tiles = []
for i in range(X_MIN, X_MAX, tile_size):
    for j in range(Y_MIN, Y_MAX, tile_size):
        tiles.append(Tile((i, j+tile_size), (i+tile_size, j)))


fig = plt.figure()
ax = fig.add_subplot(111)

c = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'm', 'b', 'g', 'r', 'c',
     'b', 'g', 'r', 'c', 'm', 'y', 'k', 'm', 'b', 'g', 'r', 'c',
     'b', 'g', 'r', 'c', 'm', 'y', 'k', 'm', 'b', 'g', 'r', 'c',
     'b', 'g', 'r', 'c', 'm', 'y', 'k', 'm', 'b', 'g', 'r', 'c',
     'b', 'g', 'r', 'c', 'm', 'y', 'k', 'm', 'b', 'g', 'r', 'c',
     'b', 'g', 'r', 'c', 'm', 'y', 'k', 'm', 'b', 'g', 'r', 'c']

for i in range(len(journeys)):
    if len(journeys[i]) < 5:
        pass
    else:
        x = [tiles[j].centre().x for j in journeys[i]['poss_tiles']]
        y = [tiles[j].centre().y for j in journeys[i]['poss_tiles']]
        plt.plot(x,y, c=c[i], label='Journey %d' % (i+1), marker='o')

plt.scatter(sensor_coords.x, sensor_coords.y, marker='x')
plt.xlim([0, 3000]), plt.ylim([0, 1000])
for loc, i,j in zip(sensor_coords['id_location'], sensor_coords['x'], sensor_coords['y']):
    ax.annotate('%s' % loc, xy=(i, j), xytext=(0, 0), textcoords='offset points')

major_ticks = np.arange(0, 3001, tile_size*10)
minor_ticks = np.arange(0, 1001, tile_size*10)

ax.set_xticks(major_ticks)
ax.set_yticks(minor_ticks)
plt.grid(which='both')
plt.legend()
plt.show()





# Collect groups, store time difference: 'dwell', delete toggles: 'moving'





