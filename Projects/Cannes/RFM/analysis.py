import pandas as pd
import numpy as np

from Code.config import get_path


def get_raw(path):
    raw = pd.DataFrame(pd.read_csv(path+'/Data/Raw/GoogleWGSN.csv'))
    return raw


def analysis(data):
    print data
    return None


def main():
    path = get_path()
    data = get_raw(path)
    print analysis(data)


if __name__ == '__main__':
    main()
