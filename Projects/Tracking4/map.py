import pandas as pd
import numpy as np
np.set_printoptions(threshold=np.inf)
from random import choice
import matplotlib.pyplot as plt
import Code.Projects.Tracking3.objects as ob
from pylab import *

from Code.Projects.Tracking3 import density as de
from Code.config import get_path, get_pwd
from Code.Projects.Tracking3.data_funcs import read_redshift, cleaned2, engineered2, timestamped
import Code.Projects.Tracking3.objects

rcParams['figure.figsize'] = 12, 8
pd.set_option('display.width', 320)


def main():
    path = get_path()  # File path to data store
    delegate_ids = list(pd.read_csv('ids.csv').uuidmm)  # List of delegate IDs

    # Set arena size and tile size (granularity) manually
    print 'Constructing Arena...\n'
    tile_size = 100
    x_max, y_max = 3000, 1000

    for dels in range(2):  # delegate in delegate_ids[11:]:

        # Ignore syntax warning
        query = "SELECT * FROM bettshowexcel2017.logs_beacons_nikos WHERE type = 'ble' AND measuredpower < 0" \
                  " AND proximity = 'Near' AND uuidmm = ('%s')" % (delegate_ids[12])

        query2 = "SELECT * FROM bettshowexcel2017.logs_beacons_nikos WHERE type = 'ble' AND measuredpower < 0" \
                  " AND proximity = 'Near' AND uuidmm = ('%s')" % (delegate_ids[13])

        raw = read_redshift(get_pwd(), query)
        clean = cleaned2(path, raw)
        data = engineered2(clean)

        raw2 = read_redshift(get_pwd(), query2)
        clean2 = cleaned2(path, raw2)
        data2 = engineered2(clean2)



        a = pd.DataFrame(pd.concat([data, data2])).sort_values('datetime')

        b = timestamped(a)

        c = b.groupby(['id', 'id_location', 'timestamp', 'journey']).agg({'metres': np.mean, 'time_diff': sum}).reset_index().sort_values('timestamp').reset_index(drop=True)

        d = c[c['id'] == '699EBC80E1F311E39A0F0CF3EE3BC012:4/41690']
        e = c[c['id'] == '699EBC80E1F311E39A0F0CF3EE3BC012:4/41675']

        arr = np.zeros((35, 35, max(d['timestamp'])+1))
        init_sense = d.ix[0].id_location

        for idx, row in d.iterrows():
            next_sense = row.id_location


            if init_sense == next_sense:
                count1+=1

                arr[0, 0, row.timestamp] += 1
            else:
                count2+=1
                arr[0, 1, row.timestamp] += 1

            init_sense = next_sense

        print arr.sum(axis=2)
        print count1, count2







        sys.exit()


        for journey in range(max(data['journey']) + 1):
            print 'Mapping Journey: %s\n' % journey
            data_i = data[data['journey'] == journey].reset_index(drop=True)

            print data_i

            init_coords = [ob.Point(data_i.ix[0].x, data_i.ix[0].y)]
            init_tiles = [de.points_to_tiles(init_coords, tile_size)[0]]

            density_grid = [np.zeros((x_max / tile_size) * (y_max / tile_size))]
            density_grid[0][init_tiles] = 1

            init_sensor = 2572

            count = 0
            coords = [init_coords[0]]
            total_time_diff = 0
            for index, row in data_i.iterrows():
                print '%s seconds later...' % row.time_diff
                total_time_diff += row.time_diff
                next_x, next_y = row.x, row.y
                r = row.metres * 100  # Circle radius(m)
                centre_x, centre_y = next_x, next_y
                n = 50

                points = de.circum_points(r, centre_x, centre_y, n)
                poss_tiles = list(pd.unique(de.points_to_tiles([ob.Point(i[0], i[1]) for i in points], tile_size)))

                triangulated = np.intersect1d(init_tiles, poss_tiles)

                if len(triangulated) == 0:
                    next_poss_coord = de.tiles_to_points([choice(poss_tiles)], tile_size)
                    next_coord_x = ((1 - (1. / len(poss_tiles))) * init_coords[0].x) + (
                        (1. / len(poss_tiles)) * next_poss_coord[0].x)
                    next_coord_y = ((1 - (1. / len(poss_tiles))) * init_coords[0].y) + (
                        (1. / len(poss_tiles)) * next_poss_coord[0].y)
                    next_coord = ob.Point(next_coord_x, next_coord_y)
                else:
                    poss_tiles = triangulated
                    next_poss_coord = de.tiles_to_points([choice(poss_tiles)], tile_size)
                    next_coord_x = ((1 - (1. / len(poss_tiles))) * init_coords[0].x) + (
                        (1. / len(poss_tiles)) * next_poss_coord[0].x)
                    next_coord_y = ((1 - (1. / len(poss_tiles))) * init_coords[0].y) + (
                        (1. / len(poss_tiles)) * next_poss_coord[0].y)
                    next_coord = ob.Point(next_coord_x, next_coord_y)

                # Nearest sensor
                next_sensor = row.id_location

                if init_sensor == next_sensor:
                    print 'Been dwelling for %s seconds\n' % total_time_diff

                prop = 1. / len(poss_tiles)

                # Update densities of new possible tiles
                density_new = density_grid[count]
                for j in range(len(poss_tiles)):
                    density_new[poss_tiles[j]] += prop
                density_new /= max(density_new)

                density_new[de.points_to_tiles([next_coord], tile_size)[0]] += 1
                density_new /= max(density_new)

                plt.imshow(transpose(density_new.reshape((x_max / tile_size, y_max / tile_size))),
                           cmap='viridis', interpolation='gaussian', vmin=0, vmax=1, origin='lower',
                           extent=[0, x_max, 0, y_max], aspect='auto')

                plt.grid(c='k')
                plt.scatter(data['x'], data['y'], marker='x', c='w')

                count += 1
                init_sensor = next_sensor
                density_grid.append(density_new)
                coords.append(next_coord)

            plt.plot([i.x for i in coords], [i.y for i in coords])
            # plt.xlim([0, x_max]), plt.ylim([0, y_max])
            plt.show()


if __name__ == '__main__':
    main()
