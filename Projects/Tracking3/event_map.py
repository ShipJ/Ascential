import pandas as pd
import objects as ob
import data_funcs as df
import density as de
import time

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

    # For every separate journey made by the user
    for i in range(num_journeys):
        # Grab all data corresponding to journey i
        data_i = engineered_data[engineered_data['journey'] == i]

        # Need at least 3 points for reasonable journey, though we know they are onsite if there is a signal
        if len(data_i) < 3:
            print 'Not enough points for a journey, though we know they were on site\n'
        else:
            # Reset the dataframe index to start at 0
            data = data_i.reset_index(drop=True)

            ''' Initialise Coordinates, tiles and probabilities '''
            # initial positioning (guess, close to first contact sensor)

            x = sensor_coords[sensor_coords['id_location'] == data.ix[0].values[1]].values[0][2]
            y = sensor_coords[sensor_coords['id_location'] == data.ix[0].values[1]].values[0][3]
            coords = [ob.Point(x, y)]
            # Initialise possible tiles
            tiles = [de.points_to_tiles(coords, tile_size)[0]]
            # Initialise probabilities of each tile
            density_grid = [np.zeros((3000 / tile_size) * (1000 / tile_size))]
            density_grid[0][tiles] = 1

            # Read data line by line, and compute next possible tiles/coords
            count = 0
            for index, row in data.iterrows():
                r = row.metres * 100  # Circle radius(m)
                centre_x = sensor_coords[sensor_coords['sensor'] == [int(row.sensor)]].values[0][2]  # Circle centre x
                centre_y = sensor_coords[sensor_coords['sensor'] == [int(row.sensor)]].values[0][3]  # Circle centre y
                n = 50  # Number of points on the circumference to consider (tune to tile granularity)
                # Compute the possible points on circle radius, with attributes above
                points = de.circum_points(r, centre_x, centre_y, n)
                # Convert those points to tiles
                poss_tiles = list(pd.unique(de.points_to_tiles([ob.Point(i[0], i[1]) for i in points], tile_size)))

                # Check if any intersection of tiles with previous time
                triangulated = np.intersect1d(tiles[count], poss_tiles)

                if len(triangulated) == 0:
                    next_poss_coord = de.tiles_to_points([choice(poss_tiles)], tile_size)
                    next_coord_x = ((1 - (1. / len(poss_tiles))) * coords[count].x) + (
                    (1. / len(poss_tiles)) * next_poss_coord[0].x)
                    next_coord_y = ((1 - (1. / len(poss_tiles))) * coords[count].y) + (
                    (1. / len(poss_tiles)) * next_poss_coord[0].y)
                    # next_coord_x = (coords[count].x + next_poss_coord[0].x) / 2.
                    # next_coord_y = (coords[count].y + next_poss_coord[0].y) / 2.
                    next_coord = ob.Point(next_coord_x, next_coord_y)
                    coords.append(next_coord)
                else:
                    poss_tiles = triangulated
                    next_poss_coord = de.tiles_to_points([choice(poss_tiles)], tile_size)
                    next_coord_x = ((1 - (1. / len(poss_tiles))) * coords[count].x) + (
                    (1. / len(poss_tiles)) * next_poss_coord[0].x)
                    next_coord_y = ((1 - (1. / len(poss_tiles))) * coords[count].y) + (
                    (1. / len(poss_tiles)) * next_poss_coord[0].y)
                    # next_coord_x = (coords[count].x + next_poss_coord[0].x) / 2.
                    # next_coord_y = (coords[count].y + next_poss_coord[0].y) / 2.
                    next_coord = ob.Point(next_coord_x, next_coord_y)
                    coords.append(next_coord)

                tiles.append(poss_tiles)

                # Probability of each next 'possible' tile is equal, until we add intelligent layer
                prop = 1. / len(poss_tiles)

                # Update densities of new possible tiles
                density_new = density_grid[count]
                for j in range(len(poss_tiles)):
                    density_new[poss_tiles[j]] += prop
                density_new /= max(density_new)

                density_new[de.points_to_tiles([next_coord], tile_size)[0]] += 1
                density_new /= max(density_new)

                # plt.figure(figsize=(20, 10))
                # figure(1)
                # imshow(transpose(density_new.reshape((3000 / tile_size, 1000 / tile_size))), cmap='viridis',
                #        interpolation='gaussian', vmin=0, vmax=1, origin='lower')
                # plt.scatter(sensor_coords['x'] / tile_size, sensor_coords['y'] / tile_size, marker='x', c='w')
                #
                # plt.show()

                coords.append(next_coord)
                density_grid.append(density_new)
            x = [i.x for i in coords]
            y = [i.y for i in coords]

            noise = np.divide(np.random.normal(0, 1, len(x)), 10.)
            x += noise
            y += noise

            plt.plot(x, y), plt.xlim([0, 3000]), plt.ylim([0, 1000])
            plt.show()

