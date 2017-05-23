import pandas as pd
import numpy as np
from Code.config import get_path
from clean_functions import clean_ble, rssi_to_metres


PATH = get_path()

# Clean data
ble = clean_ble(PATH, pd.DataFrame(pd.read_csv(PATH+'/Processed/ble_39184.txt', sep='\t')))
# Compute distances (in metres) from sensor to beacon
ble = pd.DataFrame(rssi_to_metres(ble))

print ble



# print ble.groupby(['datetime', 'sensor'])['id', 'power', 'rssi', 'accuracy',
#                                           'id_sensor', 'id_location', 'metres'].first().reset_index()


