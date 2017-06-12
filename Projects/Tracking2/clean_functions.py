import pandas as pd
import numpy as np


def clean(PATH, df):

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
    # # Map Sensors to enumerated
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
    df['metres'] = pd.to_numeric(df['metres'])
    df = pd.DataFrame(df.drop(['ratio', 'power', 'accuracy', 'proximity', 'rssi'], axis=1))
    return df