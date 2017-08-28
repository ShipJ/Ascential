import pandas as pd
import objects as ob
from Code.config import get_path
from event_map import density_map

pd.set_option('display.width', 320)


def main():

    path = get_path()  # File path to data store
    delegate_ids = list(pd.read_csv('ids.csv').uuidmm)  # List of delegate IDs

    # Set arena size and tile size (granularity) manually
    print 'Constructing Arena...\n'
    tile_size = 25

    for delegate in delegate_ids[300:]:

        # Ignore syntax warning
        query = "SELECT * FROM bettshowexcel2017.logs_beacons_nikos WHERE type = 'ble' AND measuredpower < 0" \
                " AND proximity = 'Near' AND uuidmm = ('%s')" % delegate

        # Create, analyse and plot an event map for each delegate
        density_map(path, delegate, query, tile_size)


if __name__ == '__main__':
    main()