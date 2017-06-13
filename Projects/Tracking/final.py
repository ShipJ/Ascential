import pandas as pd
import numpy as np
import psycopg2 as ps
import clean_functions as cf
import scipy.sparse as sp
from scipy import interpolate
import matplotlib.pyplot as plt
import sys
import math
from collections import Iterable
from random import choice

pd.set_option('display.width', 320)

from Code.config import get_path, get_pwd


def read_redshift(pwd):
    conn = ps.connect(
        host='redshift-clustor.cndr1rlsl2px.eu-west-1.redshift.amazonaws.com',
        user='root',
        port=5439,
        password=pwd,
        dbname='autumnfair')
    return pd.read_sql_query("SELECT * FROM bettshowexcel2017.logs_beacons_nikos WHERE type = 'ble'"
                             " AND measuredpower < 0 AND proximity = 'Near'"
                             " AND uuidmm = '699EBC80E1F311E39A0F0CF3EE3BC012:4/40025' LIMIT 100000", conn).dropna()


def sensor_coords(PATH, data):
    sensor_coords = pd.DataFrame(pd.read_csv(PATH.replace('BLE/Data', 'Location/', 1) + '/sensor_coords.txt',
                                             sep='\t',
                                             usecols=['id_location', 'x', 'y']))
    name_loc = data[['sensor', 'id_location']].drop_duplicates().sort_values('sensor').reset_index(drop=True)
    return name_loc.merge(sensor_coords, on='id_location', how='inner')


def near_only(df):
    return df[df['metres'] < 3]


def timestamped(df):
    df = df.sort_values('datetime').reset_index(drop=True)
    start_time = min(df.datetime)
    df['timestamp'] = df.groupby('id')['datetime'].apply(lambda x: (x - start_time).dt.total_seconds() / 60).astype(int)
    return df


def time_to_next(df):
    df = df.sort_values(['id', 'datetime']).reset_index(drop=True)
    df['time_diff'] = df['datetime'].diff().dt.total_seconds().fillna(0)
    journeys, journ = [], 0
    for index, row in df.iterrows():
        if row.time_diff > 600:
            journ += 1
        journeys.append(journ)
    df['journey'] = journeys
    df.loc[df['time_diff'] > 600, 'time_diff'] = 0
    return df


def timegraph(i, data, unique_times, num_sensors):
    timegraph_i = []
    data_i = data[data['id'] == i].reset_index(drop=True)
    for j in range(max(data_i['timestamp'])):
        if j in unique_times:
            t_s = data_i[data_i['timestamp'] == j]
            row = np.array(t_s.sensor)
            col = np.array(t_s.next_sensor)
            val = np.array(t_s.time_diff)
            mtx = np.array(sp.coo_matrix((val, (row, col)), shape=(num_sensors, num_sensors)).todense())
        else:
            row, col, val = [], [], []
            mtx = np.array(sp.coo_matrix((val, (row, col)), shape=(num_sensors, num_sensors)).todense())
        timegraph_i.append(mtx)
    return timegraph_i

def compute_graphs(ids, unique_times, num_sensors):
    timegraphs = []
    for i in sorted(ids):
        print 'Computing network of ID: %d' % i
        timegraph_i = timegraph(i, data, unique_times, num_sensors)
        timegraphs.append(timegraph_i)
    return timegraphs


# Return all points on the circumference of a circle with given centre-coordinates, and radius
def circum_points(r, y, z, n):
    points = [((math.cos(2*math.pi/n*x)*r+y), (math.sin(2*math.pi/n*x)*r)+z) for x in xrange(0, n+1)]
    points = [i for i in points if i[0]>0 and i[0]<3000]
    return [j for j in points if j[1]>0 and j[1]<1000]


def points_to_tiles(points, size):
    """
    Return all possible tiles in which a person could be based on the points given on the circle circumference
    :param points: List of Point data structures
    :param size: Set tile size
    :return: 
    """
    tiles = []
    for point in points:
        tiles.append(int((float(1000)/size)*math.floor(point.x/float(size)) + math.floor(point.y/float(250))))
    return tiles


# Compute list of possible tiles
def f(x):
    points = circum_points(x[1],
                           sensor_coords[sensor_coords['sensor'] == [int(x[0])]].values[0][2],
                           sensor_coords[sensor_coords['sensor'] == [int(x[0])]].values[0][3],
                           30)
    return list(pd.unique(points_to_tiles([Point(i[0], i[1]) for i in points], 250)))


def sensor_to_area(df):
    df = df.groupby(['sensor', 'timestamp', 'journey']).agg({'metres': np.mean, 'time_diff': sum}).reset_index().sort_values('timestamp').reset_index(drop=True)
    df['poss_tiles'] = df[['sensor', 'metres']].apply(f, axis=1)
    return df


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

def triangulate(df):
    df = df.groupby(['timestamp', 'journey'])['poss_tiles'].apply(g).reset_index()
    return df


class Tile:
    def __init__(self, tl, br, tile_size):
        self.tl = tl
        self.br = br
        self.tile_size = tile_size
    def centre(self):
        return Point(self.tl[0]+self.tile_size/2., self.tl[1]-self.tile_size/2.)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class EventArena:
    def __init__(self, x_min, x_max, y_min, y_max, tile_size):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.tile_size = tile_size
    def enum_tiles(self):
        ts = self.tile_size
        tiles = []
        for i in range(self.x_min, self.x_max, ts):
            for j in range(self.y_min, self.y_max, ts):
                tiles.append(Tile((i, j+ts), (i+ts, j), ts))
        return tiles
    def num_tiles(self):
        return (self.x_max/self.tile_size) * (self.y_max / self.tile_size)
    def point_in_tile(self, point):
        return int(((self.y_max/self.tile_size)*math.floor(point.x/self.tile_size))+math.floor(point.y/self.tile_size))


if __name__ == '__main__':

    # System path to data directory
    PATH = get_path()

    print 'Reading Data...\n'
    data = read_redshift(get_pwd())

    print 'Cleaning Data...\n'
    data = cf.clean(PATH, data)

    print 'Engineering Data'
    data = cf.rssi_to_metres(data)
    data = near_only(data)

    print 'Converting times to timestamps...\n'
    data = timestamped(data)
    print 'Computing time to next reading...\n'
    data = time_to_next(data)

    sensor_coords = sensor_coords(PATH, data)

    print 'Converting nearest sensor to area...\n'
    data = sensor_to_area(data)
    data = triangulate(data)

    # Arena dimensions (assuming rectangular, 30m x 10m)
    TILE_SIZE = 250
    X_MIN, X_MAX = 0, 3000
    Y_MIN, Y_MAX = 0, 1000

    arena = EventArena(X_MIN, X_MAX, Y_MIN, Y_MAX, TILE_SIZE)

    # Enumerate tiles
    tiles = arena.enum_tiles()

    # Map of tile to centre-coordinates
    # mapper = {i: (sensor_coords[sensor_coords['sensor'] == i].x.values[0],
    #               sensor_coords[sensor_coords['sensor'] == i].y.values[0]) for i in np.unique(sensor_coords.sensor)}
    mapper = {i: (tiles[i].centre().x, tiles[i].centre().y) for i in range(len(tiles))}

    for j in range(26):

        sensor_path = np.array(data[data['journey'] == j].poss_tiles)

        if len(sensor_path) > 3:

            b = [mapper[i] for i in sensor_path]
            diff = [1 for i in range(len(sensor_path))]

            def meannext(i):
                if len(i) > 2:
                    return [np.mean(i[:, 0]), np.mean(i[:, 1])]
                else:
                    return i


            mean_next = []
            for i in range(len(sensor_path)):
                mean_next.append(meannext(b[i]))

            w_avg = [mean_next[0]]
            for i in range(len(b) - 1):
                conf = (1. / (1 + diff[i]))
                w_avg.append(np.multiply(conf, mean_next[i]) + np.multiply(1 - conf, mean_next[i + 1]))

            x = np.array([i[0] for i in w_avg])
            y = np.array([i[1] for i in w_avg])

            w = [i[0] for i in mean_next]
            z = [i[1] for i in mean_next]

            noise = np.divide(np.random.normal(0, 1, len(x)), 10.)
            x += noise
            y += noise

            tck, u = interpolate.splprep([x, y], k = 3, s=0)

            xi, yi = interpolate.splev(np.linspace(0, 1, 1000), tck)

            print xi

            print yi


            fig, ax = plt.subplots(1, 1)
            plt.xlim([0, 3000]), plt.ylim([0, 1000])

            ax.plot(x, y, 'or')
            ax.plot(xi, yi, '-b')

            plt.scatter(sensor_coords.x, sensor_coords.y, marker='x', c='k')
            plt.show()


























    # # Use analogous for next area later
    # ble['next_sensor'] = np.append(ble['sensor'][1:], ble.iloc[-1]['sensor'])



