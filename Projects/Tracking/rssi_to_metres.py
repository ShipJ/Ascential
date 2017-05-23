

def compute_dist(df):
    df['metres'] = 10 ** ((df['power'] - df['rssi']) / 20.0)
    return df
