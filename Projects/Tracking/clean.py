import pandas as pd
from Code.config import get_path


def clean_ble(df):

    PATH = get_path()

    # Remove unwanted columns
    df = df.drop(['clientmac', 'proximity', 'type', 'probetime_gmt', 'probetime'], axis=1)
    # Rename column headers
    df.columns=['id', 'datetime', 'sensor', 'power', 'rssi', 'accuracy']
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
    # Map datetime strings to datetime
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df
