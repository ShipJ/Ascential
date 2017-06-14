import pandas as pd
import numpy as np

from Code.config import get_path

path = get_path()+'/Raw/HotelAccess'

hotel_access = pd.DataFrame(pd.read_csv(path+'/HotelAccess.csv'))
delegates_16 = pd.DataFrame(pd.read_csv(path+'/delegates16.csv'))
delegates_17 = pd.DataFrame(pd.read_csv(path+'/delegates17.csv'))


# Number of companies in '16 NOT IN '17
print delegates_17.columns
print np.setdiff1d(delegates_16['Company'], delegates_17['Company'])




