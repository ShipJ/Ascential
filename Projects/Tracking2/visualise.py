import numpy as np
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt


def dwell(path):
    new_path = []
    start = path[0]
    journey = 0
    for i in range(len(path)):
        if path[i] != start:
            journey += 1
        new_path.append(journey)
    df = pd.DataFrame({'A': path, 'B': new_path})
    path = pd.DataFrame(df.groupby('A')['B'].count().reset_index())
    return new_path, path


def meannext(i):
    return [np.mean(i[:, 0]), np.mean(i[:, 1])] if len(i) > 2 else i

def visplot(data, num_journeys, mapper, sensor_coords, tile_size):


    fig, ax = plt.subplots(1, 1)
    plt.xlim([0, 3000]), plt.ylim([0, 1000])

    c = ['b', 'g', 'c', 'y', 'm', 'k', 'b', 'g', 'c', 'y', 'm', 'k']
    count = 0
    for i in range(num_journeys):

        path = np.array(data[data['journey'] == i].poss_tiles)

        [new_path, path] = dwell(path)

        if len(path) > 3:
            count+=1
            b = [mapper[j] for j in path['A']]
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
            ax.plot(xi, yi, '-b', c=c[count], label='Journey %s' % i)

            plt.scatter(x, y, s=z*3, c='r', label=None)

            plt.scatter(sensor_coords.x, sensor_coords.y, marker='x', c='k', label=None)
            for loc, i, j in zip(sensor_coords['id_location'], sensor_coords['x'], sensor_coords['y']):
                ax.annotate('%s' % loc, xy=(i, j), xytext=(5, 5), textcoords='offset points')


    major_ticks = np.arange(0, 3001, tile_size*5)
    minor_ticks = np.arange(0, 1001, tile_size*5)
    ax.set_xticks(major_ticks)
    ax.set_yticks(minor_ticks)
    plt.grid(which='both')
    plt.legend()
    plt.show()
