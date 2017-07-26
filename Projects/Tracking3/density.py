import numpy as np
import pandas as pd
import math
import objects as ob

pd.set_option('display.width', 320)


def circum_points(r, x, y, n):
    """
    # Return coords on the circumference of a circle with given centre-coords and radius
    :param r: float - radius of the circle in metres
    :param x: 
    :param y: 
    :param n: number of points to return
    :return: 
    """
    points = [((math.cos(2 * math.pi / n * i) * r + x), (math.sin(2 * math.pi / n * i) * r) + y) for i in
              xrange(0, n + 1)]
    points = [i for i in points if 0. < i[0] < 3000 and 0. < i[1] < 1000]
    return points


def points_to_tiles(points, size):
    """
    Return all possible tiles in which one could be, given points on the circle's circumference
    :param points: List of Point data structures
    :param size: Tile size
    :return: 
    """
    tiles = []
    for point in points:
        tiles.append(int((float(1000) / size) * math.floor(point.x / float(size)) + math.floor(point.y / float(size))))
    return tiles


def sensor_to_area(df, tile_size, sensor_coords):
    df = df.groupby(['sensor', 'timestamp']).agg({'metres': np.mean, 'time_diff': sum}).reset_index().sort_values(
        'timestamp').reset_index(drop=True)
    poss_tiles = []
    for index, row in df.iterrows():
        r = row.metres * 100
        y = sensor_coords[sensor_coords['sensor'] == [int(row.sensor)]].values[0][2]
        z = sensor_coords[sensor_coords['sensor'] == [int(row.sensor)]].values[0][2]
        n = 50
        points = circum_points(r, y, z, n)
        poss_tiles.append(list(pd.unique(points_to_tiles([ob.Point(i[0], i[1]) for i in points], tile_size))))
    df['poss_tiles'] = poss_tiles
    return df





