import sys
import math
import pandas as pd
import numpy as np
import clean_functions as cf
from Code.config import get_path, get_pwd
import scipy.sparse as sp
import scipy.ndimage as sc
import psycopg2 as ps
import networkx as nx
import matplotlib.pyplot as plt


# Path to data
PATH = get_path()

# Arena dimensions (may be altered to include inaccessible regions?)
TILE_SIZE = 100
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

ble = cf.clean(PATH, pd.read_sql_query("SELECT * FROM bettshowexcel2017.logs_beacons_nikos"
                                          " WHERE type = 'ble' AND measuredpower < 0"
                                          " AND proximity = 'Near'"
                                          " AND uuidmm = '699EBC80E1F311E39A0F0CF3EE3BC012:4/39283'"
                                          " LIMIT 1000000", conn)).dropna()

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

uniques = pd.unique(data['timestamp'])
unique_ids = pd.unique(data['id'])
num_sensors = np.max(np.max(data[['sensor', 'next_sensor']]))+1


print data
sys.exit()

time_graphs = []
for j in sorted(unique_ids):
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

    full = aggregate.todense()


    # nx.draw(G, with_labels=True)
    # plt.show()



