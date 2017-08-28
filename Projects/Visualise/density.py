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


def agg_data(df, sensors, start, end):
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values('datetime').reset_index(drop=True)
    df = timestamped(df)
    df = df[(df['timestamp'] > start) & (df['timestamp'] < end)].reset_index(drop=True)
    if df.empty:
        return df
    df['timestamp'] = df['timestamp'] - start + 1
    df = time_to_next(df)
    agg = df.groupby(['id', 'sensor', 'timestamp', 'journey'])['timediff'].sum().reset_index()
    agg = agg[agg['sensor'].isin(sensors['Label'])].sort_values('timestamp').reset_index(drop=True)
    return agg


def compute_density(id, query, sensors, x_max, y_max, tile_size, sensor_map):
    # Read raw redshift data per delegate
    raw = read_redshift(get_pwd(), query)

    start, end = 1384, 4620
    agg = agg_data(raw, sensors, start, end)

    if len(agg) == 0:
        return None

    # Set axis to arena size
    ax = [0, x_max, 0, y_max]
    plt.axis(ax)
    plt.ion()

    # Initial arena density is 0 per tile

    init_sensor = agg['sensor'].iloc[0]
    init_density = np.zeros((int(x_max / tile_size), int(y_max / tile_size)))

    # Initial position is first closest sensor
    init_x = int(sensors[sensors['Label'] == init_sensor].x / tile_size)
    init_y = int(sensors[sensors['Label'] == init_sensor].y / tile_size)

    # Initial time-stamp
    init_timestamp = agg['timestamp'].iloc[0]
    last_timestamp = agg['timestamp'].iloc[-1]

    first_seen = pd.to_datetime('2017-01-25 10:00:00') + pd.Timedelta(minutes=init_timestamp)
    last_seen = pd.to_datetime('2017-01-25 10:00:00') + pd.Timedelta(minutes=last_timestamp)

    print '\nDelegate %s\n' \
          '_________________________________________________________________\n\n' \
          'First scanned: Day %s at %s, around Sensor %s' % (
          id[-10:], first_seen.day - 24, first_seen, sensor_map[init_sensor])

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
            next_x = int((init_x + sensors[sensors['Label'] == row.sensor].x / tile_size) / 2.)
            next_y = int((init_y + sensors[sensors['Label'] == row.sensor].y / tile_size) / 2.)

            # Update density grid - dampen previous signal, enhance new signals
            next_density = init_density / 1.5
            next_density[next_x][next_y] = 1

            plt.scatter(sensors['x'], sensors['y'], c='w', marker='x')
            plt.imshow(np.transpose(next_density), cmap='viridis', interpolation='gaussian', vmin=0, vmax=1,
                       origin='lower', extent=ax, aspect='auto')
            plt.title('Day %s, Journey %s' % (first_seen.day - 24, journey))
            plt.pause(0.5)

            first_seen = next_seen
            init_density = next_density

        init_timestamp = row.timestamp
        init_sensor = row.sensor
    print 'Last scanned at %s on Day %s\n' \
          '___________________________________________\n\n' % (last_seen, last_seen.day - 24)


def main():
    path = get_path()
    # List of delegate IDs
    delegate_ids = list(pd.read_csv('ids.csv').uuidmm)
    # Sensor names and coordinates
    sensors = pd.DataFrame(pd.read_csv(path + '/sensors.csv'))
    sensor_map = {sensor: j for j, sensor in enumerate(set(sensors['Label']))}

    x_max, y_max = 3000., 1000.
    tile_size = 50.  # Set as granular as you wish

    for id in delegate_ids[247:]:
        query = "SELECT uuidmm AS id, timestamp AS datetime, sensor FROM bettshowexcel2017.logs_beacons_nikos WHERE type = 'ble' AND measuredpower < 0 AND proximity = 'Near' AND uuidmm = ('%s')" % id
        compute_density(id, query, sensors, x_max, y_max, tile_size, sensor_map)


if __name__ == '__main__':
    main()
