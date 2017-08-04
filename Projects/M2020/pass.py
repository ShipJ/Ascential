import sys

import pandas as pd
import numpy as np
from Code.config import get_path
from collections import Counter

pd.set_option('display.width', 500)


def main():
    path = get_path()  # File path to data store

    sessions = pd.DataFrame(pd.read_csv(path+'/PassGroup/sessions.csv'))
    names = pd.DataFrame(pd.read_csv(path+'/PassGroup/names.csv'))
    combined = sessions.merge(names, on='SessionCode', how='left')


    dels = pd.DataFrame(pd.read_csv(path + '/PassGroup/dels.csv'))

    # dels = dels.dropna(subset=['ID']).reset_index(drop=True)

    print dels
    a = Counter(dels['ID'])
    b = [i for i in a.keys() if a[i] > 1]

    c = dels[dels['ID'].isin(b)]
    d = c[c['PaymentStatus'] == 'Paid'].reset_index(drop=True)
    rev = d.groupby('ID')['Revenue'].sum().reset_index()

    dels = dels.drop_duplicates(subset=['ID'], keep='first')
    print dels
    for i in range(len(rev)):
        dels[dels['ID'] == rev['ID'].ix[i]]['Revenue'] = rev['Revenue'].ix[i]

    all = combined.merge(dels, on='ID', how='left')


    # all.to_csv(path+'/PassGroup/pass_sessions.csv', index=None, encoding='utf-8-sig')







if __name__ == '__main__':
    main()