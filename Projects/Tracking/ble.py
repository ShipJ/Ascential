import pandas as pd
from Code.config import get_path
from clean import clean_ble


PATH = get_path()
ble = clean_ble(PATH, pd.DataFrame(pd.read_csv(PATH+'/Processed/ble_39184.txt', sep='\t')))


print ble