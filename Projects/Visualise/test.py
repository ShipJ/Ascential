import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2 as ps

from Code.config import get_pwd, get_path

pd.set_option('display.width', 320)


def read_redshift(pwd, query):
    conn = ps.connect(
        host='redshift-clustor.cndr1rlsl2px.eu-west-1.redshift.amazonaws.com',
        user='root',
        port=5439,
        password=pwd,
        dbname='autumnfair')
    return pd.read_sql_query(query, conn).dropna()


def rssi_to_metres(df):
    """
    This non-linear function takes an RSSI (relative signal strength) reading, and converts it to a distance (in metres)
    :param df: 
    :return: 
    """
    df['ratio'] = np.where(df['rssi'] >= 0, None, df.rssi * (np.divide(1.0, df.measuredpower)))
    df['metres'] = pd.to_numeric(np.where(df['ratio'] < 1,
                                          np.power(df['ratio'], 10),
                                          np.multiply(0.89976, np.power(df['ratio'], 7.7095) + 0.111)))
    df=df[df['metres'] < 4]
    df = pd.DataFrame(df.drop(['ratio', 'measuredpower', 'proximity', 'type', 'metres', 'rssi'], axis=1)).reset_index(drop=True)
    return df


def timestamped(df):
    start_time = pd.to_datetime('2017-08-15 14:00:00')
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


def agg_data(df, sensors):
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values('datetime').reset_index(drop=True)
    df = timestamped(df)
    if df.empty:
        return df
    df = time_to_next(df)
    agg = df.groupby(['id', 'sensor', 'timestamp', 'journey'])['timediff'].sum().reset_index()
    agg = agg[agg['sensor'].isin(sensors['Label'])].sort_values('timestamp').reset_index(drop=True)
    return agg


def compute_density(id, query, sensors, x_max, y_max, tile_size, sensor_map):
    # Read raw redshift data per delegate
    raw = read_redshift(get_pwd(), query)
    rssi = rssi_to_metres(raw)
    agg = agg_data(rssi, sensors)

    # # Set axis to arena size
    # ax = [0, x_max, 0, y_max]
    # plt.axis(ax)
    # plt.ion()

    init_sensor = agg['sensor'].iloc[0]
    init_density = np.zeros((int(x_max / tile_size), int(y_max / tile_size)))

    init_x = int(sensors[sensors['Label'] == init_sensor].x / tile_size)
    init_y = int(sensors[sensors['Label'] == init_sensor].y / tile_size)

    # Initial time-stamp
    init_timestamp = agg['timestamp'].iloc[0]
    last_timestamp = agg['timestamp'].iloc[-1]

    first_seen = pd.to_datetime('2017-08-15 14:00:00') + pd.Timedelta(minutes=init_timestamp)
    last_seen = pd.to_datetime('2017-08-15 19:00:00') + pd.Timedelta(minutes=last_timestamp)

    print '\nDelegate %s\n' \
          '_________________________________________________________________\n\n' \
          'First scanned: Day %s at %s, around Sensor %s' % (
          id, first_seen.day - 24, first_seen, sensor_map[init_sensor])

    # Update initial density with first known location (nearest sensor)
    init_density[init_x][init_y] = 1

    # Journeys are defined as any continual activity without more than 10 minutes between scans
    journey = agg['journey'].iloc[0]
    # Dwell is where the nearest sensor does not change over time
    dwell = 0

    # Read each sensor scan in turn
    for idx, row in agg.iterrows():

        if init_sensor == row.sensor:
            dwell += 1

        else:
            next_seen = first_seen + pd.Timedelta(minutes=dwell)
            print 'Dwelled for: %s minutes around Sensor %s' % (dwell, sensor_map[init_sensor])
            print '... then moved to Sensor %s at %s' % (sensor_map[row.sensor], next_seen)
            # Moved to new station, so dwell time resets`
            dwell = 0

            # Next nearest sensor
            next_x = int((0.4*(init_x) + 0.6*(sensors[sensors['Label'] == row.sensor].x / tile_size)))
            next_y = int((init_y + sensors[sensors['Label'] == row.sensor].y / tile_size) / 2.)

            # Update density grid - dampen previous signal, enhance new signals
            next_density = init_density / 1.5
            next_density[next_x][next_y] = 1

            # plt.scatter(sensors['x'], sensors['y'], c='w', marker='x')
            # plt.imshow(np.transpose(next_density), cmap='viridis', interpolation='gaussian', vmin=0, vmax=1,
            #            origin='lower', extent=ax, aspect='auto')
            # plt.title('Day %s, Journey %s' % (first_seen.day - 24, journey))
            # plt.pause(0.5)

            first_seen = next_seen
            init_density = next_density

        init_timestamp = row.timestamp
        init_sensor = row.sensor
    print 'Last scanned at %s on Day %s\n' \
          '___________________________________________\n\n' % (last_seen, last_seen.day - 24)


def main():

    # Sensor names and coordinates
    data = [['98:7B:F3:1C:CA:92', 1, 350, 900],
            ['98:7B:F3:D3:4A:A7', 2, 200, 600],
            ['98:7B:F3:1D:1D:E3', 3, 250, 100]]

    sensors = pd.DataFrame(data, columns=['Label', 'Id', 'x', 'y'])
    sensor_map = {sensor: j for j, sensor in enumerate(set(sensors['Label']))}

    x_max, y_max = 500., 1000.
    tile_size = 20.  # Set as granular as you wish

    id_1 = 37802
    query = "SELECT uuidmm as id, timestamp as datetime, sensor, proximity, type, measuredpower, rssi FROM cannes2017.logs WHERE (uuidmm LIKE '%39019%' OR uuidmm LIKE '%39019%')" \
            " AND timestamp BETWEEN '2017-08-15 14:00:00' AND '2017-08-15 19:00:00' AND type = 'ble' AND measuredpower < 0 AND proximity IN ('Near', 'Immediate')"
    compute_density(id_1, query, sensors, x_max, y_max, tile_size, sensor_map)


if __name__ == '__main__':
    main()