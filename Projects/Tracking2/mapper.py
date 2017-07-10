import pandas as pd
import objects as ob
from Code.config import get_path
from data_funcs import event_map

pd.set_option('display.width', 320)


def main():

    path = get_path()  # File path to data store
    delegate_ids = list(pd.read_csv('ids.csv').uuidmm)  # List of delegate IDs

    # Set arena size and tile size (granularity) manually
    print 'Constructing Arena...\n'
    tile_size = 25
    x_min, x_max = 0, 3000
    y_min, y_max = 0, 1000

    # Construct event arena with variables above
    arena = ob.EventArena(x_min, x_max, y_min, y_max, tile_size)
    tiles = arena.enum_tiles()
    # Map each square to a number from 0 to n
    mapper = {i: (tiles[i].centre().x, tiles[i].centre().y) for i in range(len(tiles))}

    for delegate in delegate_ids:

        # Ignore syntax warning
        query = "SELECT * FROM bettshowexcel2017.logs_beacons_nikos WHERE type = 'ble' AND measuredpower < 0" \
                " AND proximity = 'Near' AND uuidmm = ('%s')" % delegate

        # Create, analyse and plot an event map for each delegate
        event_map(path, delegate, query, arena, mapper)


if __name__ == '__main__':
    main()