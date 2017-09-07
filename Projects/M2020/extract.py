import sys
import numpy as np
import pandas as pd
from Code.config import get_path

pd.set_option('display.width', 320)


def main():


    revenue = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/final/revenue.csv'))
    delegates = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/final/delegates.csv'))


    print revenue.merge(delegates, on='Name', how='inner')

    a = revenue[revenue['Revenue'] > 0]
    print len(a)

    print a.merge(delegates, on='Name', how='inner')


    





    sys.exit()




if __name__ == '__main__':
    main()