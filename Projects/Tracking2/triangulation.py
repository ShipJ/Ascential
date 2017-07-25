import numpy as np
import pandas as pd
import math
from collections import Iterable, Counter
from random import choice
import objects as ob
import sys
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
    points = [((math.cos(2*math.pi/n*i)*r+x), (math.sin(2*math.pi/n*i)*r)+y) for i in xrange(0, n+1)]
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
        tiles.append(int((float(1000)/size)*math.floor(point.x/float(size)) + math.floor(point.y/float(size))))
    return tiles


def sensor_to_area(df, tile_size, sensor_coords):
    df = df.groupby(['sensor', 'timestamp']).agg({'metres': np.mean, 'time_diff': sum}).reset_index().sort_values('timestamp').reset_index(drop=True)
    poss_tiles = []
    for index, row in df.iterrows():
        r = row.metres*100
        y = sensor_coords[sensor_coords['sensor'] == [int(row.sensor)]].values[0][2]
        z = sensor_coords[sensor_coords['sensor'] == [int(row.sensor)]].values[0][2]
        n = 50
        points = circum_points(r, y, z, n)
        poss_tiles.append(list(pd.unique(points_to_tiles([ob.Point(i[0], i[1]) for i in points], tile_size))))
    df['poss_tiles'] = poss_tiles
    return df


def flatten(a):
    for item in a:
        if isinstance(item, Iterable):
            for x in flatten(item):
                yield x
        else:
            yield item


def g(x):
    print list(x.values)
    poss_tiles = flatten(list(x.values))
    print poss_tiles
    sys.exit()
    counts = Counter(poss_tiles)
    print counts
    if len(counts.values()) == 0:
        return None
    else:
        count_max = max(counts.values())
        return choice([key for key, value in counts.iteritems() if value == count_max])


def intersect(df):
    print df
    t = df['poss_tiles'].apply(lambda x: pd.Series(1, index=x))
    t = t.fillna(0)  # Filled by 0

    t['timestamp'] = df['timestamp']
    t['journey'] = df['journey']

    print t

    sys.exit()

    print Counter(t.ix[0])

    # sum observations across days and transpose
    # print t.groupby(['timestamp', 'journey']).sum().T


    df = df.groupby(['timestamp', 'journey'])['poss_tiles'].apply(g).reset_index()
    sys.exit()
    if len(df) > 2:
        return df
    else:
        return pd.DataFrame()


class Triangulate:
    def __init__(self, data, tile_size, sensor_coords):
        self.data = data
        self.tile_size = tile_size
        self.sensor_coords = sensor_coords
        
    def triangulate(self):
        tile_path = sensor_to_area(self.data, self.tile_size, self.sensor_coords)
        print tile_path

        a = intersect(tile_path).dropna()
        return a



    # journey_paths = journeys.triangulate()
    # print journey_paths

    # if journey_paths.empty:
    #     print 'Not possible to construct user journeys from engineered data\n'
    #     return None


    # print 'Plotting Journeys...\n'
    # num_journeys = len(pd.unique(journey_paths.journey))
    # vs.vis_plot(journey_paths, num_journeys, enum_tiles, sensor_coords, arena.tile_size)
