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

tile_size = 100

# Arena dimensions (may be altered to include inaccessible regions?)
X_MIN, X_MAX = 0, 3000
Y_MIN, Y_MAX = 0, 1000

# Apply function to clean the data
ble = cf.clean_ble(PATH, pd.DataFrame(pd.read_csv(PATH+'/Processed/ble_39283.txt', sep='\t'))).dropna()
# Apply function to compute distances (in metres) from signals to beacons
ble = pd.DataFrame(cf.rssi_to_metres(ble))
ble=ble[ble['metres'] < 3].sort_values('datetime').reset_index(drop=True)

journey, current = [], 0
start = ble['datetime'][0]
for i in range(len(ble)):
    next = ble['datetime'][i]

    if (next-start).seconds > 600:
        current += 1
        journey.append(current)
    else:
        journey.append(current)
    start = next

ble['journey'] = np.array(journey)

def f(x):
    if len(x) == 1:
        return 0
    else:
        return (x.reset_index().tail(1).values[0][1] - x.reset_index().loc[0].values[1]).seconds

a = ble.groupby(['sensor', 'journey'])['datetime'].apply(f).reset_index().sort_values('journey').reset_index(drop=True)
print np.unique(a[['sensor', 'next_sensor']])


sensor_coords = pd.DataFrame(pd.read_csv(PATH.replace('BLE/Data', 'Location/', 1) + '/sensor_coords.txt',
                                         sep='\t',
                                         usecols=['id_location', 'x', 'y']))
# Only get locations of sensors within the given data set
sensor_coords = sensor_coords[sensor_coords['id_location'].isin(pd.unique(ble['id_location']))].reset_index(drop=True)
# Associate sensor names with locations
name_loc = ble[['sensor', 'id_location']].drop_duplicates().sort_values('sensor').reset_index(drop=True)
sensor_coords = name_loc.merge(sensor_coords, on='id_location', how='inner')


# Return all points on the circumference of a circle with given centre-coordinates, and radius
def circum_points(r, y, z, n):
    points = [((math.cos(2*math.pi/n*x)*r+y), (math.sin(2*math.pi/n*x)*r)+z) for x in xrange(0, n)]
    points = [i for i in points if i[0]>X_MIN and i[0]<X_MAX]
    return [j for j in points if j[1]>Y_MIN and j[1]<Y_MAX]



class Point:
    """
    A coordinate of a given location within the arena
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

def points_to_tiles(points, size):
    """
    Return all possible tiles in which a person could be based on the points given on the circle circumference
    :param points: List of Point data structures
    :param size: Set tile size
    :return: 
    """
    tiles = []
    for point in points:
        tiles.append(int(
            (float(Y_MAX) / size) * math.floor(point.x / float(size)) + math.floor(point.y / float(tile_size))))
    return tiles


three = []
for i in range(1, 4):
    three.append(pd.unique(points_to_tiles([Point(i[0], i[1]) for i in circum_points(i*100,
                        sensor_coords[sensor_coords['sensor'] == 2]['x'][0],
                        sensor_coords[sensor_coords['sensor'] == 2]['y'][0],
                        8)], tile_size)))


zero = ble[ble['journey'] == 0]
zero['bin'] = pd.cut(zero['metres'], bins=[0, 1, 2, 3], labels=[0, 1, 2])
val_counts = zero['bin'].value_counts()























