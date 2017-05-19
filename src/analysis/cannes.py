import pandas as pd
from Code.config import get_path

''' Set PATH variable to data directory '''
PATH = get_path()


''' Grab Data '''
all = pd.DataFrame(pd.read_csv(PATH+'/Cannes/Data/AllDelegateTrakScanners.csv'))
red = pd.DataFrame(pd.read_csv(PATH+'/Cannes/Data/AllRedcarpetScanners.csv'))


