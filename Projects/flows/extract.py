import sys
import pandas as pd

import matplotlib.pyplot as plt

from Code.config import get_path, get_pwd
from Code.Projects.Tracking3.data_funcs import read_redshift
pd.set_option('display.width', 320)


def main():

    path = get_path()  # File path to data store
    delegate_ids = list(pd.read_csv('ids.csv').uuidmm)  # List of delegate IDs

    sensor_loc = pd.DataFrame(pd.read_csv(path.replace('BLE', 'Location', 1) + '/sensor_locations.txt', sep='\t'))
    stand_loc = pd.DataFrame(pd.read_csv(path.replace('BLE', 'Location', 1) + '/stand_locations.txt', sep='\t'))
    sensor_coords = pd.DataFrame(pd.read_csv(path.replace('BLE', 'Location', 1) + '/sensor_coords.txt', sep='\t'))

    stands = stand_loc[stand_loc['type'] != 'single_point']
    sensors = stand_loc[stand_loc['type'] == 'single_point']

    stands = stands.merge(sensor_coords, left_on='id', right_on='id_location', how='inner')
    sensors = sensors.merge(sensor_coords, left_on='id', right_on='id_location', how='inner')




    for delegate in delegate_ids:

        # Ignore syntax warning
        query = "SELECT * FROM bettshowexcel2017.logs_beacons_nikos WHERE type = 'ble' AND measuredpower < 0" \
                " AND proximity = 'Near' AND uuidmm = ('%s')" % delegate

        print 'Reading data for Delegate: %s...\n' % delegate
        raw = read_redshift(get_pwd(), query)
        if raw.empty:
            print 'No beacon data exists for Delegate: %s\n' % delegate
            return None




if __name__ == '__main__':
    main()