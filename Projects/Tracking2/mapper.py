import pandas as pd
pd.set_option('display.width', 320)
import objects as ob
from collections import Counter

from Code.config import get_path
from data_funcs import event_map


def main():

    path = get_path()  # Path to data store
    delegate_ids = list(pd.read_csv('ids.csv').uuidmm)  # List of delegate IDs

    print 'Constructing Arena...\n'
    tile_size = 25
    x_min, x_max = 0, 3000
    y_min, y_max = 0, 1000

    # Construct event arena
    arena = ob.EventArena(x_min, x_max, y_min, y_max, tile_size)
    tiles = arena.enum_tiles()
    mapper = {i: (tiles[i].centre().x, tiles[i].centre().y) for i in range(len(tiles))}

    for delegate in delegate_ids[100:]:

        # Ignore SQL syntax Warning
        query = "SELECT * FROM bettshowexcel2017.logs_beacons_nikos WHERE type = 'ble' AND measuredpower < 0" \
                " AND proximity = 'Near' AND uuidmm = ('%s')" % delegate

        # Create, analyse and plot an event map for each delegate
        event_map(path, delegate, query, arena, tiles, mapper)


if __name__ == '__main__':
    main()