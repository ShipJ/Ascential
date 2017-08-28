import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt

import networkx as nx

from data_funcs import read_redshift, cleaned, engineered, timestamped
from Code.config import get_path, get_pwd


def main():
    path = get_path()
    delegate_ids = list(pd.read_csv('ids.csv').uuidmm)

    stand_loc = pd.DataFrame(pd.read_csv(path.replace('BLE','Location',1)+'/stand_locations.txt', sep='\t'))
    sensor_loc = pd.DataFrame(pd.read_csv(path.replace('BLE', 'Location', 1)+'/sensor_locations.txt', sep='\t'))
    sensor_coords = pd.DataFrame(pd.read_csv(path.replace('BLE','Location',1)+'/sensor_coords.txt', sep='\t'))

    sensors = sensor_coords.merge(sensor_loc, on='id_location', how='inner').merge(stand_loc,
                                                                                   left_on='id_location', right_on='id',
                                                                                   how='inner').drop(['id_points', 'id_map', 'id_sensor', 'sequence_number', 'id_location', 'type'], axis=1)

    sensor_map = {sensor: j for j, sensor in enumerate(set(sensors['name']))}
    sensors['sensor'] = sensors['name'].map(sensor_map)

    top_10 = []
    for delegate in delegate_ids[:10]:
        query = "SELECT * FROM bettshowexcel2017.logs_beacons_nikos WHERE type = 'ble' AND measuredpower < 0" \
                " AND proximity = 'Near' AND uuidmm = ('%s')" % delegate
        raw = read_redshift(get_pwd(), query, source='1')
        clean = cleaned(raw)
        eng = engineered(clean)
        time = timestamped(eng)

        agg = time.groupby(['id', 'sensor', 'timestamp', 'journey'])['time_diff'].sum().reset_index()

        init_sense = agg.ix[0].sensor
        arr = np.zeros((len(sensors), len(sensors), 17000))
        for idx, row in agg.iterrows():
            next_sense = row.sensor
            a = sensor_map.get(init_sense, np.nan)
            b = sensor_map.get(next_sense, np.nan)
            if ~np.isnan(a) and ~np.isnan(b):
                if init_sense == next_sense:
                    arr[a, b, row.timestamp] += 1
                else:
                    arr[a, b, row.timestamp] += 1
                init_sense = next_sense

        arr = arr.sum(axis=2)
        top_10.append(arr)
    j = top_10[0]
    for i in range(1, 10):
        j += top_10[i]

    G = nx.DiGraph(j)
    a = pd.DataFrame(nx.to_edgelist(G))

    a.to_csv('/Users/JackShipway/Desktop/flows.csv', index=None)








if __name__ == '__main__':
    main()