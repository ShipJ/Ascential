import pandas as pd
pd.set_option('display.width', 380)
import numpy as np
import sys

from Code.config import get_path

path = get_path()

delegates16 = pd.DataFrame(pd.read_csv(path+'/ScanSessions16/2016Delegates.csv',
                                       usecols=['Delegate_ID', 'FestivalGenericName', 'ProductName', 'ProductGroup',
                                                'Registered - CompanyName', 'Registered - Country',
                                                'Registered - City', 'banding', 'sub_banding']))
delegates16.columns=['ID', 'Fest', 'ProductName', 'ProductGroup', 'Company', 'Country', 'City', 'Band', 'SubBand']
delegates16 = delegates16[delegates16['ID'] != 'None']
delegates16['ID'] = delegates16['ID'].astype(int)

scan_sessions16 = pd.DataFrame(pd.read_csv(path+'/ScanSessions16/2016ScanSessions.csv', low_memory=False,
                                           usecols=['DelegateId', 'SessionCode', 'Scanned']))
scan_sessions16.columns=['ID', 'Session', 'Time']
weird = ['GD', 'JP']
scan_sessions16 = scan_sessions16[~scan_sessions16['Session'].isin(weird)].reset_index(drop=True)
scan_sessions16['Session'] = scan_sessions16['Session'].astype(int)

session_desc = pd.DataFrame(pd.read_csv(path+'/ScanSessions16/2016SessionDescr.csv',
                                        usecols=['SessionCode', 'SessionHost', 'SessionDescription']))
session_desc.columns=names=['Session', 'Host', 'Description']


''' Session Description per Scan '''
scan_desc = scan_sessions16.merge(session_desc, on='Session', how='inner')

''' Delegate info per scan '''
joined = scan_desc.merge(delegates16, on='ID', how='left')

data = pd.DataFrame(joined.drop_duplicates(subset=['ID', 'Time']))



print len(data)









