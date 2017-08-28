import pandas as pd
import numpy as np
import psycopg2 as ps


def read_redshift(pwd, query):
    conn = ps.connect(
        host='redshift-clustor.cndr1rlsl2px.eu-west-1.redshift.amazonaws.com',
        user='root',
        port=5439,
        password=pwd,
        dbname='autumnfair')
    return pd.read_sql_query(query, conn).dropna()


def timestamped(df):
    start_time = pd.to_datetime('2017-01-24 10:56:51')
    df['timestamp'] = df.groupby('id')['datetime'].apply(lambda x: (x - start_time).dt.total_seconds() / 60).astype(int)
    return df


def time_to_next(df):
    df['timediff'] = df['datetime'].diff().dt.total_seconds().fillna(0)
    journeys, journ = [], 0
    for index, row in df.iterrows():
        if row.timediff > 600:
            journ += 1
        journeys.append(journ)
    df['journey'] = journeys
    df.loc[df['timediff'] > 600, 'timediff'] = 0
    return df


def compute_flows(id, df, sensors, sensor_map, start, end):
    """
    
    :param id: 
    :param df: 
    :param sensors: 
    :param sensor_map: 
    :param start: 
    :param end: 
    :return: 
    """

    print 'Extracting for delegate: %s' % id
    df = df[df['id'] == id]

    if df.empty:
        return np.zeros((len(sensors), len(sensors), (end-start+1)))
    else:
        # Ensure data in datetime format
        df['datetime'] = pd.to_datetime(df['datetime'])
        # Ensure data is time ordered
        df = df.sort_values('datetime').reset_index(drop=True)
        # Convert actual times to timestamps - (first minute is t0, etc, starting at 10am on Day 1)
        df = timestamped(df)
        # Extract data between 10am 25th Jan (t_1384) and 3pm 28th Jan (t_4620)
        df = df[(df['timestamp'] > start) & (df['timestamp'] < end)].reset_index(drop=True)
        if df.empty:
            return np.zeros((len(sensors), len(sensors), (end-start+1)))
        # Restart the timestmap clock at 0 (there are 1,383 timestamps until 10am on 25th Jan)
        df['timestamp'] = df['timestamp'] - start + 1
        # Compute time difference between each reading
        df = time_to_next(df)

        print 'Aggregating data...'
        df_agg = df.groupby(['id', 'sensor', 'timestamp', 'journey'])['timediff'].sum().reset_index().sort_values(
            'timestamp').reset_index()
        if df.empty:
            return np.zeros((len(sensors), len(sensors), (end - start + 1)))

        init_sensor = df_agg.ix[0].sensor
        flows = np.zeros((len(sensors), len(sensors), (end-start+1)))
        for idx, row in df_agg.iterrows():
            next_sensor = row.sensor
            # Get indices of each sensor (Name corresponds to a number from 0-33)
            i, j = sensor_map.get(init_sensor, np.nan), sensor_map.get(next_sensor, np.nan)
            # If we have the coordinates of that sensor, run, otherwise ignore
            if ~np.isnan(i) and ~np.isnan(j):
                if init_sensor == next_sensor:
                    flows[i, j, row.timestamp] += 1
                else:
                    flows[i, j, row.timestamp] += 1
            init_sensor = next_sensor
        return flows
