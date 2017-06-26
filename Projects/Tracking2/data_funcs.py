import psycopg2 as ps
import pandas as pd
import numpy as np
import triangulation as tr
import visualise as vs

from Code.config import get_pwd


def read_redshift(pwd, query):
    conn = ps.connect(
        host='redshift-clustor.cndr1rlsl2px.eu-west-1.redshift.amazonaws.com',
        user='root',
        port=5439,
        password=pwd,
        dbname='autumnfair')
    return pd.read_sql_query(query, conn).dropna()


def cleaned(path, df):
    # Remove unwanted columns
    df = df.drop(['clientmac', 'type', 'probetime_gmt', 'probetime'], axis=1)
    # Rename column headers
    df.columns=['id', 'datetime', 'sensor', 'proximity', 'power', 'rssi', 'accuracy']
    # Merge with stand locations
    sensor_stand_loc = pd.merge(

        pd.DataFrame(pd.read_csv(path.replace('BLE', 'Location', 1) + '/stand_locations.txt',
                                 sep='\t')),
        pd.DataFrame(pd.read_csv(path.replace('BLE', 'Location', 1) + '/sensor_locations.txt',
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
    df['ratio'] = np.where(df['rssi'] >= 0, None, df.rssi*(np.divide(1.0, df.power))) # Ignore runtime warnings
    df['metres'] = np.where(df['ratio'] < 1, np.power(df['ratio'], 10), np.multiply(0.89976, np.power(df['ratio'], 7.7095) + 0.111))
    df['metres'] = pd.to_numeric(df['metres'])
    df = pd.DataFrame(df.drop(['ratio', 'power', 'accuracy', 'proximity', 'rssi'], axis=1))
    return df


def near_only(df):
    return df[df['metres'] < 5]


def timestamped(df):
    df = df.sort_values('datetime').reset_index(drop=True)
    start_time = min(df.datetime)
    df['timestamp'] = df.groupby('id')['datetime'].apply(lambda x: (x - start_time).dt.total_seconds() / 60).astype(int)
    return df


def time_to_next(df):
    df = df.sort_values(['id', 'datetime']).reset_index(drop=True)
    df['time_diff'] = df['datetime'].diff().dt.total_seconds().fillna(0)
    journeys, journ = [], 0
    for index, row in df.iterrows():
        if row.time_diff > 600:
            journ += 1
        journeys.append(journ)
    df['journey'] = journeys
    df.loc[df['time_diff'] > 600, 'time_diff'] = 0
    return df


def get_sensor_coords(PATH, data):
    sensor_coords = pd.DataFrame(pd.read_csv(PATH.replace('BLE', 'Location/', 1) + '/sensor_coords.txt',
                                             sep='\t',
                                             usecols=['id_location', 'x', 'y']))
    name_loc = data[['sensor', 'id_location']].drop_duplicates().sort_values('sensor').reset_index(drop=True)
    return name_loc.merge(sensor_coords, on='id_location', how='inner')


def engineered(data):
    print '1. Converting RSSI to metres'
    rssi = rssi_to_metres(data)
    print '2. Removing distant signals'
    near = near_only(rssi)
    print '3. Filling missing minutes'
    timestamp = timestamped(near)
    print '4. Computing time difference\n'
    time_diff = time_to_next(timestamp)
    return time_diff


def event_map(path, delegate, query, arena, tiles, mapper):
    print '____________________________'
    print '\nReading Data for Delegate: %s' % delegate
    raw = read_redshift(get_pwd(), query)

    if raw.empty:
        print 'No beacon data exists for Delegate: %s' % delegate
        return None
    else:
        print 'Cleaning Data...'
        clean_data = cleaned(path, raw)

        if clean_data.empty:
            print 'Data for Delegate: %s could not be cleaned' % delegate
            return None
        else:
            print 'Engineering Data...'
            engineered_data = engineered(clean_data)

    # Get coordinates of all beacons receiving delegate signal
    sensor_coords = get_sensor_coords(path, engineered_data)

    print 'Mapping User Journey...\n'
    print engineered_data
    journey = tr.Triangulate(engineered_data, arena.tile_size, sensor_coords)
    journey_data = journey.triangulate()

    if not journey_data.empty:
        print 'Plotting Journeys...\n'
        num_journeys = len(pd.unique(journey_data.journey))
        tile_size = arena.tile_size
        vs.visplot(journey_data, num_journeys, mapper, sensor_coords, tile_size)


