import pandas as pd
from Code.config import get_path

PATH = get_path()


ble = pd.DataFrame(pd.read_csv(PATH+'/'))