import pandas as pd
import numpy as np
from Code.config import get_path
import clean_functions as cf
import sys
import matplotlib.pyplot as plt
import math
from random import choice
import datetime as dt


PATH = get_path()
X_MIN, X_MAX = 0, 3000
Y_MIN, Y_MAX = 0, 1000

# Clean data
ble = cf.clean_ble(PATH, pd.DataFrame(pd.read_csv(PATH+'/Processed/ble_39283.txt', sep='\t'))).dropna()
# Compute distances (in metres) from sensor to beacon
ble = pd.DataFrame(cf.rssi_to_metres(ble)).sort_values('datetime').reset_index(drop=True)
# Convert floats to ints
ble.id_location = ble.id_location.astype(int)

# Grab sensor locations
sensor_coords = pd.DataFrame(pd.read_csv(PATH.replace('BLE/Data', 'Location/', 1) + '/sensor_coords.txt', sep='\t',
                                         usecols=['id_location', 'x', 'y']))
sensor_coords = sensor_coords[sensor_coords['id_location'].isin(pd.unique(ble['id_location']))].reset_index(drop=True)

name_loc = ble[['sensor', 'id_location']].drop_duplicates().sort_values('sensor').reset_index(drop=True)
sensor_coords = name_loc.merge(sensor_coords, on='id_location', how='inner')

tile_size = 10

class Rectangle:
    def __init__(self, tl, br):
        self.tl = tl
        self.br = br
    def centre(self):
        return Point(self.tl[0]+tile_size/2., self.tl[1]-tile_size/2.)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def smart(start, all, x, y):
    a = []
    for i in all:
        a.append(abs(np.floor(i/x)-np.floor(start/x))+abs(np.floor(i/y)-np.floor(start/y)))
    return all[np.argmin(a)]


tiles = []
for i in range(X_MIN, X_MAX, tile_size):
    for j in range(Y_MIN, Y_MAX, tile_size):
        tiles.append(Rectangle((i, j+tile_size), (i+tile_size, j)))


def circum_points(r, y, z, n):
    points = [((math.cos(2*math.pi/n*x)*r+y), (math.sin(2*math.pi/n*x)*r)+z) for x in xrange(0, n+1)]
    points = [i for i in points if i[0]>X_MIN and i[0]<X_MAX]
    return [j for j in points if j[1]>Y_MIN and j[1]<Y_MAX]


def points_to_tiles(points):
    possible_tiles = []
    for point in points:
        possible_tiles.append(int((float(Y_MAX)/tile_size)*math.floor(point.x/float(tile_size))
                                  +
                                  math.floor(point.y/float(tile_size))))
    return possible_tiles


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
data_timestamp = pd.DataFrame()

j = 0
for i in range(len(ble)):

    print i

    signal = ble.iloc[i]

    if (signal.datetime - start).seconds > 600:
        if j == 1:
            break
        j+=1
        print 'NEW JOURNEY'
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

    start = signal.datetime

    mean_dist = data_timestamp.groupby('sensor')['metres'].mean().reset_index()

    all = []
    for sensor in mean_dist['sensor']:

        points = circum_points(np.array(mean_dist[mean_dist['sensor'] == int(sensor)].metres)[0],
                            np.array(sensor_coords[sensor_coords['sensor'] == int(sensor)].x)[0],
                            np.array(sensor_coords[sensor_coords['sensor'] == int(sensor)].y)[0], 20)
        points = pd.unique(points_to_tiles([Point(i[0], i[1]) for i in points]))

        all = np.union1d(all, points)

    # Random
    rand_tile = tiles[int(choice(all))]
    # More intelligent - using previous closest
    start_loc = int(smart(start_loc, all, 10, 30))
    smart_tile = tiles[start_loc]

    journey_rand = journey_rand.append({'x':rand_tile.centre().x, 'y': rand_tile.centre().y}, ignore_index=True)
    journey_smart = journey_smart.append({'x':smart_tile.centre().x, 'y': smart_tile.centre().y}, ignore_index=True)


fig = plt.figure()
ax = fig.add_subplot(111)

c = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'b', 'g', 'r', 'c',
     'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'b', 'g', 'r', 'c',
     'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'b', 'g', 'r', 'c',
     'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'b', 'g', 'r', 'c',
     'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'b', 'g', 'r', 'c',
     'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'b', 'g', 'r', 'c']

for i in range(len(journeys_rand)):
    # plt.plot(journeys_rand[i]['x'], journeys_rand[i]['y'], c=c[i], marker='>', label='Journey: %s' % i)
    plt.plot(journeys_smart[i]['x'], journeys_smart[i]['y'], c=c[i], marker='>', label='Journey: %s' % i)

plt.scatter(sensor_coords['x'], sensor_coords['y'], marker='o', label='Sensors')
plt.xlim([0, 3000]), plt.ylim([0, 1000])
for loc, i,j in zip(sensor_coords['id_location'], sensor_coords['x'], sensor_coords['y']):
    ax.annotate('%s' % loc, xy=(i, j), xytext=(0, 0), textcoords='offset points')


major_ticks = np.arange(0, 3001, tile_size*10)
minor_ticks = np.arange(0, 1001, tile_size*10)

ax.set_xticks(major_ticks)
ax.set_yticks(minor_ticks)
plt.legend()
plt.grid(which='both')
plt.show()




















