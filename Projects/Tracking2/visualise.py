import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate
from random import choice


def dwell(path):
    if len(path) > 0:
        new_path, start, journey_id = [], path[0], 0
        for i in range(len(path)):
            if path[i] != start:
                journey_id += 1
            new_path.append(journey_id)
        df = pd.DataFrame({'A': path, 'B': new_path})
        path = pd.DataFrame(df.groupby('A')['B'].count().reset_index())
    else:
        print 'Non'
        path = pd.DataFrame()
    return path


def meannext(i):
    return [np.mean(i[:, 0]), np.mean(i[:, 1])] if len(i) > 2 else i


def vis_plot(data, num_journeys, enum_tiles, sensor_coords, tile_size):

    fig, ax = plt.subplots(1, 1)

    colour = ['b', 'g', 'c', 'y', 'm', 'k']

    for i in range(num_journeys):

        plt.scatter(sensor_coords.x, sensor_coords.y, marker='x', c='k', label=None)
        for loc, j, k in zip(sensor_coords['id_location'], sensor_coords['x'], sensor_coords['y']):
            ax.annotate('%s' % loc, xy=(j, k), xytext=(5, 5), textcoords='offset points')

        path = dwell(np.array(data[data['journey'] == i].poss_tiles))

        if len(path) > 3:
            b = [enum_tiles[j] for j in path['A']]
            diff = [1 for k in range(len(path))]

            mean_next = []
            for l in range(len(path)):
                mean_next.append(meannext(b[l]))


            w_avg = [mean_next[0]]
            for m in range(len(b) - 1):
                conf = (1. / (1 + diff[m]))
                w_avg.append(np.multiply(conf, mean_next[m]) + np.multiply(1 - conf, mean_next[m+1]))

            x = np.array([n[0] for n in w_avg])
            y = np.array([o[1] for o in w_avg])

            noise = np.divide(np.random.normal(0, 1, len(x)), 10.)
            x += noise
            y += noise

            tck, u = interpolate.splprep([x, y], k=3, s=0)

            xi, yi = interpolate.splev(np.linspace(0, 1, 1000), tck)

            z = np.array(path['B'])
            ax.plot(xi, yi, '-b', c=choice(colour), label='Journey %s' % i)

            plt.scatter(x, y, s=z*3, c='r', label=None)


    major_ticks, minor_ticks = np.arange(0, 3001, tile_size*5), np.arange(0, 1001, tile_size*5)
    ax.set_xticks(major_ticks), ax.set_yticks(minor_ticks)
    plt.xlim([0, 3000]), plt.ylim([0, 1000]), plt.grid(which='both'), plt.legend()
    plt.show()