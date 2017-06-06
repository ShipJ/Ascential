import sys
import math
import pandas as pd
import numpy as np
import clean_functions as cf
import matplotlib.pyplot as plt
import datetime as dt
from Code.config import get_path
from random import choice

# Path to data
PATH = get_path()

# Arena dimensions (may be altered to include inaccessible regions?)
X_MIN, X_MAX = 0, 3000
Y_MIN, Y_MAX = 0, 1000

# Apply function to clean the data
ble = cf.clean_ble(PATH, pd.DataFrame(pd.read_csv(PATH+'/Processed/ble_39283.txt', sep='\t'))).dropna()

# Apply function to compute distances (in metres) from signals to beacons
ble = pd.DataFrame(cf.rssi_to_metres(ble)).sort_values('datetime').reset_index(drop=True)

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
tile_size = 100

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

def smart(start, all, height):
    """
    Function that selects the closest tile, based on the previous tile, rather than random
    :param start: Tile number at the start of the algo
    :param all: List of all possible 'next' tiles
    :param height: number of tiles in the y-axis (Y_MAX / tile_size)
    :return: 
    """
    a = []
    for i in all:
        a.append(abs(np.floor(i/height)-np.floor(start/height))+abs(np.mod(i, height)-np.mod(start, height)))
    return all[np.argmin(a)]

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


def drop_old(old_timefame):
    old_timefame['datetime'] = pd.to_datetime(old_timefame['datetime'])
    most_recent = old_timefame.iloc[-1].datetime
    mask = (old_timefame['datetime'] > most_recent-dt.timedelta(seconds=30)) & (old_timefame['datetime'] <= most_recent)
    new_timeframe = old_timefame.loc[mask]
    return pd.DataFrame(new_timeframe)

journeys_rand, journeys_smart = [], []
journey_rand, journey_smart = pd.DataFrame(), pd.DataFrame()

start_loc = 0
start = ble.iloc[0].datetime
start_x = 705
start_y = 855
data_timestamp = pd.DataFrame()
smart_tiles = pd.DataFrame()

j = 0
for i in range(len(ble)):

    print i

    signal = ble.iloc[i]

    if (signal.datetime - start).seconds > 600:
        if j == 3:
            break
        j+=1
        print 'NEW JOURNEY'
        signal = ble.iloc[i+1]
        start_x = 705
        start_y = 855
        journeys_rand.append(journey_rand)
        journey_rand = pd.DataFrame()
        journeys_smart.append(journey_smart)
        journey_smart = pd.DataFrame()

    # Add new signal
    data_timestamp = data_timestamp.append({'sensor': signal.sensor,
                                            'datetime': signal.datetime,
                                            'metres': signal.metres}, ignore_index=True)

    # Remove any from previous time window
    data_timestamp = drop_old(data_timestamp)

    mean_dist = data_timestamp.groupby('sensor')['metres'].mean().reset_index()

    all = []
    for sensor in mean_dist['sensor']:

        points = circum_points(np.array(mean_dist[mean_dist['sensor'] == int(sensor)].metres)[0],
                            np.array(sensor_coords[sensor_coords['sensor'] == int(sensor)].x)[0],
                            np.array(sensor_coords[sensor_coords['sensor'] == int(sensor)].y)[0], 20)
        points = pd.unique(points_to_tiles([Point(i[0], i[1]) for i in points], tile_size))

        all = np.union1d(all, points)

    # Random
    rand_tile = tiles[int(choice(all))]
    # More intelligent - using previous closest
    start_loc = int(smart(start_loc, all, float(Y_MAX)/tile_size))
    smart_tile = tiles[start_loc]

    time_to_next = (signal.datetime - start).seconds
    if time_to_next > 0:
        xv = abs(rand_tile.centre().x-start_x)/float(time_to_next)/1000.
        yv = abs(rand_tile.centre().y-start_y)/float(time_to_next)/1000.
    else:
        xv = 0
        yv = 0

    journey_rand = journey_rand.append({'x':rand_tile.centre().x, 'y': rand_tile.centre().y,
                                        'secs': (signal.datetime - start).seconds,
                                        'x_v': xv,
                                        'y_v': yv},
                                       ignore_index=True)
    journey_smart = journey_smart.append({'x':smart_tile.centre().x, 'y': smart_tile.centre().y,
                                          'secs': (signal.datetime - start).seconds}, ignore_index=True)

    smart_tiles = smart_tiles.append({'tile':start_loc, 'dt': (signal.datetime - start).seconds}, ignore_index=True)
    start = signal.datetime
    start_x = rand_tile.centre().x
    start_y = rand_tile.centre().y



change = []
group = []
start = smart_tiles['tile'][0]
j = 0
for i in range(len(journeys_smart[0])):
    if smart_tiles['dt'][i] > 30:
        pass
    else:
        next = smart_tiles['tile'][i]
        if next == start:
            group.append(j)
        else:
            change.append(smart_tiles['dt'][i])
            j += 1
            group.append(j)
        start = next

smart_tiles['group'] = np.array(group)

print change
print smart_tiles.groupby('group')['dt'].sum().reset_index()




#
# fig = plt.figure()
# ax = fig.add_subplot(111)
#
# c = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'm', 'b', 'g', 'r', 'c',
#      'b', 'g', 'r', 'c', 'm', 'y', 'k', 'm', 'b', 'g', 'r', 'c',
#      'b', 'g', 'r', 'c', 'm', 'y', 'k', 'm', 'b', 'g', 'r', 'c',
#      'b', 'g', 'r', 'c', 'm', 'y', 'k', 'm', 'b', 'g', 'r', 'c',
#      'b', 'g', 'r', 'c', 'm', 'y', 'k', 'm', 'b', 'g', 'r', 'c',
#      'b', 'g', 'r', 'c', 'm', 'y', 'k', 'm', 'b', 'g', 'r', 'c']
#
# for i in range(len(journeys_smart)):
#     # plt.plot(journeys_rand[6]['x'], journeys_rand[6]['y'], c=c[0], marker='x', label='Journey: %s' % i)
#     plt.plot(journeys_smart[i]['x'], journeys_smart[i]['y'], c=c[i], marker='>', label='Journey: %s' % i)
#
# plt.scatter(sensor_coords['x'], sensor_coords['y'], marker='o', label='Sensors')



























