import sys
import math
import pandas as pd
import numpy as np
import clean_functions as cf
from Code.config import get_path, get_pwd
import scipy.sparse as sp
import psycopg2 as ps

# Path to data
PATH = get_path()

# Arena dimensions (may be altered to include inaccessible regions?)
tile_size = 100
X_MIN, X_MAX = 0, 3000
Y_MIN, Y_MAX = 0, 1000

# Apply function to clean the data
ble = cf.clean_ble(PATH, pd.DataFrame(pd.read_csv(PATH+'/Processed/ble_39283.txt', sep='\t'))).dropna()
# Apply function to compute distances (in metres) from signals to beacons
ble = pd.DataFrame(cf.rssi_to_metres(ble))
ble=ble[ble['metres'] < 10].sort_values('datetime').reset_index(drop=True)[['id', 'datetime', 'sensor', 'metres']]

ble = ble.sort_values('datetime')
ble['metres'] = pd.to_numeric(ble['metres'])
ble['next_sensor'] = np.append(ble['sensor'][1:], ble.iloc[-1]['sensor'])

ble['timestamp'] = ble.groupby('id')['datetime'].apply(lambda x: (x - x.dt.round('1min').iloc[0]).dt.total_seconds()/60).astype(int)
ble['datetime'] = ble['datetime'].diff().dt.total_seconds().fillna(0)
ble.loc[ble['datetime'] > 600, 'datetime'] = 0


print ble






sys.exit()








#### DATA FINAL ####
data = ble.groupby(['id', 'sensor', 'next_sensor', 'timestamp'])['datetime'].sum().reset_index().sort_values('timestamp').reset_index(drop=True)

uniques = pd.unique(data['timestamp'])
num_sensors = np.max(np.max(data[['sensor', 'next_sensor']]))+1


time_graphs = []
for i in range(max(data['timestamp'])):
    if i in uniques:
        t_s = data[data['timestamp'] == i]

        row = np.array(t_s.sensor)
        col = np.array(t_s.next_sensor)
        val = np.array(t_s.datetime)

        mtx = sp.coo_matrix((val, (row, col)), shape=(num_sensors, num_sensors))

    else:
        row, col, val = [], [], []
        mtx = sp.coo_matrix((val, (row, col)), shape=(num_sensors, num_sensors))

    time_graphs.append(mtx)

aggregate = sp.coo_matrix((num_sensors, num_sensors))
for i in time_graphs:
    aggregate += i


a = aggregate.todense().reshape(num_sensors, num_sensors)

print a






