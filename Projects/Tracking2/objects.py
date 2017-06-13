import math


class Tile:
    def __init__(self, tl, br, tile_size):
        self.tl = tl
        self.br = br
        self.tile_size = tile_size
    def centre(self):
        return Point(self.tl[0]+self.tile_size/2., self.tl[1]-self.tile_size/2.)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class EventArena:
    def __init__(self, x_min, x_max, y_min, y_max, tile_size):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.tile_size = tile_size
    def enum_tiles(self):
        ts = self.tile_size
        tiles = []
        for i in range(self.x_min, self.x_max, ts):
            for j in range(self.y_min, self.y_max, ts):
                tiles.append(Tile((i, j+ts), (i+ts, j), ts))
        return tiles
    def num_tiles(self):
        return (self.x_max/self.tile_size) * (self.y_max / self.tile_size)
    def point_in_tile(self, point):
        return int(((self.y_max/self.tile_size)*math.floor(point.x/self.tile_size))+math.floor(point.y/self.tile_size))