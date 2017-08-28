import pandas as pd
import numpy as np
from pylab import *
from Code.config import get_path, get_pwd
from Code.Projects.Tracking3.data_funcs import read_redshift, cleaned2, engineered2, timestamped

rcParams['figure.figsize'] = 12, 8
pd.set_option('display.width', 320)


def main():
    path = get_path()
    delegate_ids = list(pd.read_csv('ids.csv').uuidmm)

    top_3 = []
    for delegate in delegate_ids[11:20]:
        query = "SELECT * FROM bettshowexcel2017.logs_beacons_nikos WHERE type = 'ble' AND measuredpower < 0" \
                " AND proximity = 'Near' AND uuidmm = ('%s')" % delegate

        raw = read_redshift(get_pwd(), query)
        clean = cleaned2(path, raw)
        data = engineered2(clean)
        time = timestamped(data)

        agg = time.groupby(['id', 'sensor', 'id_location', 'timestamp', 'journey']).agg(
            {'time_diff': sum}).reset_index().sort_values('timestamp').reset_index(drop=True)

        init_sense = agg.ix[0].sensor
        arr = np.zeros((35, 35, 17000))
        for idx, row in agg.iterrows():
            next_sense = row.sensor
            if init_sense == next_sense:
                arr[init_sense, init_sense, row.timestamp] += 1
            else:
                arr[init_sense, next_sense, row.timestamp] += 1
            init_sense = next_sense
        top_3.append(arr)


if __name__ == '__main__':
    main()
