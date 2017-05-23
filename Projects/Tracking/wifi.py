import pandas as pd
from Code.config import get_path

PATH = get_path()

''' Get WiFi data '''
wifi = pd.DataFrame(pd.read_csv(PATH+'/Raw/wifi.txt', sep='\t'))


print wifi