import pandas as pd
pd.set_option('display.width', 320)
import objects as ob
from collections import Counter

from Code.config import get_path
from data_funcs import event_map


def main():

    path = get_path() # Path to data store
    delegate_ids = list(pd.read_csv('ids.csv').uuidmm) # List of delegate IDs

    print 'Constructing Arena...\n'
    TILE_SIZE = 20
    X_MIN, X_MAX = 0, 3000
    Y_MIN, Y_MAX = 0, 1000

    # Construct event arena
    arena = ob.EventArena(X_MIN, X_MAX, Y_MIN, Y_MAX, TILE_SIZE)
    tiles = arena.enum_tiles()
    mapper = {i: (tiles[i].centre().x, tiles[i].centre().y) for i in range(len(tiles))}

    for delegate in delegate_ids:

        # Ignore SQL syntax Warning
        query = "SELECT * FROM bettshowexcel2017.logs_beacons_nikos WHERE type = 'ble' AND measuredpower < 0" \
                " AND proximity = 'Near' AND uuidmm = ('%s')" % delegate

        # Create, analyse and plot an event map for each delegate
        event_map(path, delegate, query, arena, tiles, mapper)


if __name__ == '__main__':
    main()