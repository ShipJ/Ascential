import pandas as pd
import numpy as np
import sys


def clean_ble(PATH, df):

    # Remove unwanted columns
    df = df.drop(['clientmac', 'type', 'probetime_gmt', 'probetime'], axis=1)
    # Rename column headers
    df.columns=['id', 'datetime', 'sensor', 'proximity', 'power', 'rssi', 'accuracy']
    # Merge with stand locations
    sensor_stand_loc = pd.merge(
        pd.DataFrame(pd.read_csv(PATH.replace('BLE/Data', 'Location/', 1) + '/stand_locations.txt',
                                 sep='\t')),
        pd.DataFrame(pd.read_csv(PATH.replace('BLE/Data', 'Location/', 1) + '/sensor_locations.txt',
                                 sep='\t')),
        left_on='id',
        right_on='id_location').drop('id', axis=1)
    # Merge with location data
    df = pd.DataFrame(pd.merge(df,
                               sensor_stand_loc,
                               left_on='sensor',
                               right_on='name',
                               how='outer').drop(['name', 'type'], axis=1))
    # Map IDs to enumerated
    map_id = {id: i for i, id in enumerate(set(df['id']))}
    df['id'] = df['id'].map(map_id)
    # Map Sensors to enumerated
    map_sensors = {sensor: i for i, sensor in enumerate(set(df['sensor']))}
    df['sensor'] = df['sensor'].map(map_sensors)
    # Map datetime strings to datetime # map(lambda x: x.replace(second=0))
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.dropna()
    # Convert floats to ints
    df['id_location'] = df['id_location'].astype(int)
    return df


def rssi_to_metres(df):
    # Original, simple function
    # df['metres1'] = 10 ** ((df['power'] - df['rssi']) / 20.0)

    # More complex, non-linear function
    df['ratio'] = np.where(df['rssi'] >= 0, None, df.rssi*(1.0/df.power)) # Ignore runtime warnings
    df['metres'] = np.where(df['ratio'] < 1, np.power(df['ratio'], 10), (0.89976)*np.power(df['ratio'], 7.7095) + 0.111)
    df = df.drop('ratio', axis=1)
    return df


def identify_pairs(df):
    pairs = []
    start_time, start_sensor = df['datetime'][0], df['sensor'][0]
    for i in range(len(df)-1):
        next_time, next_sensor = df['datetime'][i+1], df['sensor'][i+1]
        if (next_time-start_time).seconds < 30:
            if next_sensor != start_sensor:
                pairs.append(np.array(df.loc[i]))
                pairs.append(np.array(df.loc[i+1]))
        start_time, start_sensor = next_time, next_sensor
    return np.array(pairs)


def identify_triples(pairs):
    triples = []
    for i in range(len(pairs)-3):
        triple = pairs[i:i+4, :]
        if (triple[3, 1] - triple[0, 1]).seconds < 30:
            if len(pd.unique(triple[:, 2])) == 3:
                triples.append(triple)
    return np.array(triples)
