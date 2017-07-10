import numpy as np
import pandas as pd
import math
from collections import Iterable, Counter
from random import choice
import objects as ob


def circum_points(r, x, y, n):
    """
    # Return coords on the circumference of a circle with given centre-coords and radius
    :param r: float - radius of the circle in metres
    :param x: 
    :param y: 
    :param n: number of points to return
    :return: 
    """
    points = [((math.cos(2*math.pi/n*i)*r+x), (math.sin(2*math.pi/n*i)*r)+y) for i in xrange(0, n+1)]
    points = [i for i in points if 0. < i[0] < 3000 and 0. < i[1] < 1000]
    return points


def points_to_tiles(points, tile_size):
    """
    Return all possible tiles in which a person could be based on the points given on the circle circumference
    :param points: List of Point data structures
    :param size: Set tile size
    :return: 
    """
    tiles = []
    for point in points:
        tiles.append(int((float(1000)/tile_size)*math.floor(point.x/float(tile_size)) + math.floor(point.y/float(tile_size))))
    return tiles


def sensor_to_area(df, tile_size, sensor_coords):
    df = df.groupby(['sensor', 'timestamp', 'journey']).agg({'metres': np.mean, 'time_diff': sum}).reset_index().sort_values('timestamp').reset_index(drop=True)
    poss_tiles = []
    for index, row in df.iterrows():
        r = row.metres
        y = sensor_coords[sensor_coords['sensor'] == [int(row.sensor)]].values[0][2]
        z = sensor_coords[sensor_coords['sensor'] == [int(row.sensor)]].values[0][2]
        n = 50
        points = circum_points(r, y, z, n)
        poss_tiles.append(list(pd.unique(points_to_tiles([ob.Point(i[0], i[1]) for i in points], tile_size))))
    df['poss_tiles'] = poss_tiles
    return df


def flatten(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, basestring):
            for x in flatten(item):
                yield x
        else:
            yield item


def g(x):
    poss_tiles = flatten(list(x.values))
    counts = Counter(poss_tiles)
    if len(counts.values()) == 0:
        return None
    else:
        count_max = max(counts.values())
        return choice([key for key, value in counts.iteritems() if value == count_max])


def intersect(df):
    df = df.groupby(['timestamp', 'journey'])['poss_tiles'].apply(g).reset_index()
    if len(df) > 2:
        return df
    else:
        print 'It is not possible to construct a pathway for this delegate.'
        return pd.DataFrame()


class Triangulate:
    def __init__(self, data, tile_size, sensor_coords):
        self.data = data
        self.tile_size = tile_size
        self.sensor_coords = sensor_coords

    def triangulate(self):
        tile_path = sensor_to_area(self.data, self.tile_size, self.sensor_coords)
        return intersect(tile_path)