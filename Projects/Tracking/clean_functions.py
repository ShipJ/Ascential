import pandas as pd
import numpy as np


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
    # Map datetime strings to datetime - chop off seconds: eg. 12:00:15 => 12:00:00
    df['datetime'] = pd.to_datetime(df['datetime']) #.map(lambda x: x.replace(second=0))
    return df


def rssi_to_metres(df):
    df['metres'] = 10 ** ((df['power'] - df['rssi']) / 20.0)
    return df


def identify_pairs(df):
    pairs = []
    start_time, start_sensor = df['datetime'][0], df['sensor'][0]
    for i in range(len(df)-1):
        next_time, next_sensor = df['datetime'][i+1], df['sensor'][i+1]
        if (next_time-start_time).seconds < 30:
            if next_sensor != start_sensor:
                pairs.append([0, start_time, start_sensor, df['proximity'][i], df['metres'][i]])
                pairs.append([0, next_time, next_sensor, df['proximity'][i+1], df['metres'][i+1]])
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
