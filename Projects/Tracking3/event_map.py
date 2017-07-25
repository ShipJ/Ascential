import pandas as pd
import numpy as np
import objects as ob
import data_funcs as df
pd.set_option('display.width', 320)

from pylab import *
from random import choice
from Code.config import get_pwd


def density_map(path, delegate, query, tile_size, arena, enum_tiles):
    print '____________________________\n'

    print 'Reading data for Delegate: %s...\n' % delegate
    raw = df.read_redshift(get_pwd(), query)
    if raw.empty:
        print 'No beacon data exists for Delegate: %s\n' % delegate
        return None

    print 'Cleaning data...\n'
    clean = df.cleaned(path, raw)
    if clean.empty:
        print 'When cleaned, data for Delegate: %s did not produce adequate results\n' % delegate
        return None

    print 'Engineering Data...'
    engineered_data = df.engineered(clean)
    if engineered_data.empty:
        print 'Not possible to engineer data usefully\n'
        return None


    print 'Mapping User Journey...\n'

    a = engineered_data
    sensor_coords = df.get_sensor_coords(path, engineered_data)
    print sensor_coords

    for i in range(len(a)):
        b = a[a['journey'] == i]
        if len(b) < 3:
            print 'Journey %s too short...\n' % i
        else:
            print 'Constructing Pathway for Journey: %s\n' % i

            poss_tiles = []
            for index, row in b.iterrows():
                r = row.metres * 100
                y = sensor_coords[sensor_coords['sensor'] == [int(row.sensor)]].values[0][2]
                z = sensor_coords[sensor_coords['sensor'] == [int(row.sensor)]].values[0][3]
                n = 100
                points = de.circum_points(r, y, z, n)
                poss_tiles.append(list(pd.unique(tr.points_to_tiles([ob.Point(i[0], i[1]) for i in points], tile_size))))

            d = np.array(np.zeros((3000000/(tile_size ** 2))).reshape((3000/tile_size, 1000/tile_size)))
            position = 266
            for i in range(len(poss_tiles)):



                sys.exit()
                b = poss_tiles[i]
                prop = 1/len(poss_tiles)

                f = np.intersect1d(b, d)
                if len(f) > 0:
                    position = position + choice(f)
                else:
                    position = int((position + np.mean(b))/2)

                c = np.zeros(3000000/(tile_size**2))
                for j in range(len(b)):
                    c[b[j-1]] = prop
                    c[position] = 1

                c = np.array(c.reshape((3000/tile_size, 1000/tile_size)))


                e = c + d
                d = c

                figure(1)
                imshow(transpose(e), cmap='viridis', interpolation='hamming', vmin=0, vmax=1, origin='lower')
                plt.show()
            sys.exit()

