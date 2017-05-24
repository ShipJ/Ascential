import pandas as pd
import numpy as np
from Code.config import get_path
import clean_functions as cf

PATH = get_path()

# Clean data
ble = cf.clean_ble(PATH, pd.DataFrame(pd.read_csv(PATH+'/Processed/ble_39283.txt', sep='\t'))).dropna()

# Compute distances (in metres) from sensor to beacon
ble = pd.DataFrame(cf.rssi_to_metres(ble)).sort_values('datetime')


print ble


















