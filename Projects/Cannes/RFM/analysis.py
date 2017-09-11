import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from Code.config import get_path


def get_raw(path):
    raw = pd.DataFrame(pd.read_csv(path + '/Data/Raw/GoogleWGSN.csv'))
    return raw


def prop_null(df):
    null_dict = {}
    total = float(len(df))
    for col in df.columns:
        nulls = len(df[df[col].isnull()])
        null_dict[col] = (nulls / total) * 100
    return null_dict


def prop_unique(df):
    unique_dict = {}
    total = float(len(df))
    for col in df.columns:
        uniques = len(pd.unique(df[col]))
        unique_dict[col] = (uniques / total) * 100
    return unique_dict


def analysis(df):
    nulls = prop_null(df)
    uniques = prop_unique(df)

    for key, value in sorted(nulls.iteritems(), key=lambda (k, v): (v, k)):
        print "%s: %s" % (key, value)
    for key, value in sorted(uniques.iteritems(), key=lambda (k, v): (v, k)):
        print "%s: %s" % (key, value)

    cmap = sns.diverging_palette(5, 250, as_cmap=True)
    corr = df.corr()

    sns.heatmap(corr, cmap=cmap)
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.show()

    s = corr.abs().unstack()
    so = s.sort_values(kind="quicksort", ascending=False)
    print so


def recency(df):
    df['diff'] = df['visitstarttime'] - min(df['visitstarttime'])
    diff = max(df['visitstarttime']) - min(df['visitstarttime'])
    band = diff / 5
    df['recency'] = df['diff'] / band
    df['recency'] = df['recency'].round()
    return df


def frequency(df):

    return df

def main():
    path = get_path()
    data = get_raw(path)
    recent = recency(data)
    analysis(recent)



if __name__ == '__main__':
    main()
