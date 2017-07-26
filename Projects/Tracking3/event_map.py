import pandas as pd
import objects as ob
import data_funcs as df
import density as de

from pylab import *
from random import choice
from Code.config import get_pwd

pd.set_option('display.width', 320)


def density_map(path, delegate, query, tile_size):
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

    # Coordinates of all sensors
    sensor_coords = df.get_sensor_coords(path, engineered_data)
    # Number of separate journeys (10 minute time-gap)
    num_journeys = max(engineered_data['journey'])

    for i in range(num_journeys):
        data_i = engineered_data[engineered_data['journey'] == i]

        # Need at least 3 points for reasonable journey, though we know they are onsite if there is a signal
        if len(data_i) < 3:
            print 'Not enough points for a journey, though we know they were on site\n'
        else:

            data = data_i.reset_index(drop=True)

            # initial positioning (guess, close to first contact sensor)
            x = sensor_coords[sensor_coords['id_location'] == data.ix[0].values[1]].values[0][2]
            y = sensor_coords[sensor_coords['id_location'] == data.ix[0].values[1]].values[0][3]

            init_coord = ob.Point(x, y)
            init_tiles = de.points_to_tiles([init_coord], tile_size)[0]
            init_density_grid = np.zeros(3000 / tile_size * 1000 / tile_size)

            init_density_grid[init_tiles] = 1

            for index, row in data.iterrows():
                r = row.metres * 100  # Circle radius(m)
                centre_x = sensor_coords[sensor_coords['sensor'] == [int(row.sensor)]].values[0][2]  # Circle centre x
                centre_y = sensor_coords[sensor_coords['sensor'] == [int(row.sensor)]].values[0][3]  # Circle centre y
                n = 100  # Number of points on the circumference to consider (tune to tile granularity)

                # Compute the possible points on circle radius, with attributes above
                points = de.circum_points(r, centre_x, centre_y, n)
                # Convert those points to tiles
                next_tiles = list(pd.unique(de.points_to_tiles([ob.Point(i[0], i[1]) for i in points], tile_size)))


                triangulated = np.intersect1d(init_tiles, next_tiles)

                if len(triangulated) == 0:
                    poss_tiles = next_tiles
                    current_coord = ob.Point(1000, 1000)  # Avg. of all possible tiles
                else:
                    poss_tiles = triangulated
                    current_tile = choice(poss_tiles)
                    # x_intersect =
                    # y_intersect =

                    # current_coord = ob.Point(x_intersect, y_intersect)

                # Probability of each next 'possible' tile is equal, until we add intelligent layer
                prop = 1./len(poss_tiles)

                # Update densities of new possible tiles
                for j in range(len(poss_tiles)):
                    init_density_grid[poss_tiles[j]] = prop
                init_density_grid /= 2.

                next_coord = ob.Point((init_coord.x + current_coord.x)/2.,
                                      (init_coord.y + current_coord.y)/2.)
                next_tile = de.points_to_tiles([next_coord], tile_size)[0]

                init_density_grid[next_tile] = 1
                init_density_grid /= 2.

                figure(1)
                imshow(transpose(init_density_grid.reshape((3000/tile_size,
                                                            1000/tile_size))),
                       cmap='viridis', interpolation='gaussian', vmin=0, vmax=1, origin='lower')
                plt.show()


                init_coord = next_coord
                init_tiles = next_tiles
