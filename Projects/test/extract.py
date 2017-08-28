import sys
import pandas as pd
import numpy as np
import networkx as nx

from data_funcs import read_redshift, compute_flows
from Code.config import get_pwd

pd.set_option('display.width', 320)


def main():

    # print 'Reading Test Data...'
    # test = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/measures.csv'))
    # test.columns = ['id', 'datetime', 'sensor']
    # print 'Test data loaded successfully'


    locs = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/Ascential/Projects/Tracking/Location/stand_locations.txt', sep='\t'))
    coords = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/Ascential/Projects/Tracking/Location/sensor_coords.txt', sep='\t'))

    print list(pd.unique(locs.merge(coords, left_on='id', right_on='id_points', how='inner')['name']))


    sys.exit()





    #
    print 'Reading sensor data...'
    sensors = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/sensor_loc.csv'))
    sensor_map = {sensor: j for j, sensor in enumerate(set(sensors['sensor']))}
    sensors['id'] = sensors['sensor'].map(sensor_map)
    num_sensors = len(sensors)
    print 'Loaded sensor data'
    sensors.to_csv('/Users/JackShipway/Desktop/sensors.csv', index=None)
    sys.exit()
    #
    # # Only read data for sensors that we have coordinates for
    # data = test[test['sensor'].isin(sensors['sensor'])]
    #
    # # Timestamps corresponding to event start/end
    # start, end = 1384, 4620
    #
    # cnt = 0
    # delegate_ids = pd.unique(data['id'])
    # all_flows = np.empty([len(delegate_ids), num_sensors, num_sensors, (end-start+1)])
    # for id in delegate_ids:
    #     print 'Computing flows for Delegate: %s\n______________________________' % cnt
    #     # Extract data per delegate
    #     data_i = data[data['id'] == id]
    #     # Compute flows per delegate
    #     flows = compute_flows(id, data_i, sensors, sensor_map, start, end)
    #     all_flows[cnt, :, :, :]=flows
    #     cnt+=1
    #
    # np.save('/Users/JackShipway/Desktop/flows.csv', all_flows)

    all_flows = np.load('/Users/JackShipway/Desktop/flows.csv.npy')

    # Run some temporal analysis (i.e. select particular times, particular delegates etc)
    ''' '''

    print '\n\nComputing Sum'
    a = np.sum(all_flows, axis=0)
    b = np.sum(a, axis=2)
    print 'Computing Graph'
    G = nx.DiGraph(b)
    print 'Computing Edge list'
    edge_list = pd.DataFrame(nx.to_edgelist(G))
    edge_list.columns=('Source', 'Target', 'Weight')
    edge_list['Weight'] = edge_list['Weight'].astype(str).str.extract('(\d+)').astype(int)

    node_list = pd.DataFrame()
    node_list['Id'] = range(num_sensors)

    edge_list.to_csv('/Users/JackShipway/Desktop/edge_list_all.csv', index=None)
    node_list.to_csv('/Users/JackShipway/Desktop/node_list_all.csv', index=None)



if __name__ == '__main__':
    main()