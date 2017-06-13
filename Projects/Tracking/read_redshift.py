import sys
import math
import pandas as pd
import numpy as np
import clean_functions as cf
from Code.config import get_path, get_pwd
import scipy.sparse as sp
import psycopg2 as ps
import networkx as nx
import matplotlib.pyplot as plt


# Path to data
PATH = get_path()

# Arena dimensions (may be altered to include inaccessible regions?)
TILE_SIZE = 500
X_MIN, X_MAX = 0, 3000
Y_MIN, Y_MAX = 0, 1000

# Grab sensor locations
sensor_coords = pd.DataFrame(pd.read_csv(PATH.replace('BLE/Data', 'Location/', 1) + '/sensor_coords.txt',
                                         sep='\t',
                                         usecols=['id_location', 'x', 'y']))

conn = ps.connect(
    host='redshift-clustor.cndr1rlsl2px.eu-west-1.redshift.amazonaws.com',
    user='root',
    port=5439,
    password=get_pwd(),
    dbname='autumnfair')

cur = conn.cursor()

ble = cf.clean_ble(PATH, pd.read_sql_query("SELECT * FROM bettshowexcel2017.logs_beacons_nikos"
                                          " WHERE type = 'ble' AND measuredpower < 0"
                                          " AND proximity = 'Near' LIMIT 100000", conn)).dropna()

# Associate sensor names with locations
name_loc = ble[['sensor', 'id_location']].drop_duplicates().sort_values('sensor').reset_index(drop=True)
sensor_coords = name_loc.merge(sensor_coords, on='id_location', how='inner')


ble = ble.sort_values('datetime').reset_index(drop=True)


# Apply function to compute distances (in metres) from signals to beacons
ble = pd.DataFrame(cf.rssi_to_metres(ble))
ble=ble[ble['metres'] < 10].sort_values('datetime').reset_index(drop=True)[['id', 'datetime', 'sensor', 'metres']]
ble = ble.sort_values('datetime')
ble['metres'] = pd.to_numeric(ble['metres'])
ble['next_sensor'] = np.append(ble['sensor'][1:], ble.iloc[-1]['sensor'])
ble['timestamp'] = ble.groupby('id')['datetime'].apply(lambda x: (x - x.dt.round('1min').iloc[0]).dt.total_seconds()/60).astype(int)
ble['datetime'] = ble['datetime'].diff().dt.total_seconds().fillna(0)
ble.loc[ble['datetime'] > 600, 'datetime'] = 0

# Final data set
data = ble.sort_values('timestamp').reset_index(drop=True)
data = data.groupby(['id', 'sensor', 'next_sensor', 'timestamp'])['metres'].mean().reset_index().sort_values(['id', 'timestamp']).reset_index(drop=True)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
def circum_points(r, y, z, n):
    points = [((math.cos(2*math.pi/n*x)*r+y), (math.sin(2*math.pi/n*x)*r)+z) for x in xrange(0, n)]
    points = [i for i in points if i[0]>X_MIN and i[0]<X_MAX]
    return [j for j in points if j[1]>Y_MIN and j[1]<Y_MAX]
def points_to_tiles(points, size):
    tiles = []
    for point in points:
        tiles.append(int((float(Y_MAX)/size)*math.floor(point.x/float(size)) + math.floor(point.y/float(TILE_SIZE))))
    return tiles
def f(x):
    points = circum_points(x[2]*100, sensor_coords[sensor_coords['sensor'] == [int(x[1])]].values[0][2],
                           sensor_coords[sensor_coords['sensor'] == [int(x[1])]].values[0][3], 50)
    return list(pd.unique(points_to_tiles([Point(i[0], i[1]) for i in points], TILE_SIZE)))

data = data[data['id'] == 0]

data['poss_tiles'] = data[['id', 'sensor', 'metres']].apply(f, axis=1)

print data

sys.exit()


uniques = pd.unique(data['timestamp'])
unique_ids = pd.unique(data['id'])
num_sensors = np.max(np.max(data[['sensor', 'next_sensor']]))+1

time_graphs = []
for j in unique_ids:
    print j
    time_graph_i = []
    data_i = data[data['id'] == j].reset_index(drop=True)
    for i in range(max(data_i['timestamp'])):
        if i in uniques:
            t_s = data_i[data_i['timestamp'] == i]
            row = np.array(t_s.sensor)
            col = np.array(t_s.next_sensor)
            val = np.array(t_s.datetime)
            mtx = sp.coo_matrix((val, (row, col)), shape=(num_sensors, num_sensors))
        else:
            row, col, val = [], [], []
            mtx = sp.coo_matrix((val, (row, col)), shape=(num_sensors, num_sensors))
        time_graph_i.append(mtx)

    aggregate = sp.coo_matrix((num_sensors, num_sensors))
    for i in time_graph_i:
        aggregate += i
    a = aggregate.todense().reshape(num_sensors, num_sensors)
    G = nx.DiGraph(a)

    nx.draw(G, with_labels=True)
    plt.show()

print time_graphs
















