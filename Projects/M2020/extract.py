import pandas as pd
from Code.config import get_path

pd.set_option('display.width', 320)


def main():

    path = get_path()  # File path to data store
    print path


if __name__ == '__main__':
    main()