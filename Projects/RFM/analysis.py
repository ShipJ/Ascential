import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from Code.config import get_path


def get_raw(path):
    raw = pd.DataFrame(pd.read_csv(path + '/Data/Raw/GoogleWGSN2.csv'))
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
    a = df.groupby(['fullVisitorId']).agg({'visitstarttime': max, 'visitId': len}).reset_index()

    most_recent = max(df['visitstarttime'])
    least_recent = min(df['visitstarttime'])
    recent_diff = (most_recent-least_recent)/5
    a['visitstarttime'] = ((a['visitstarttime']-least_recent)/recent_diff)
    a['visitstarttime'] = a['visitstarttime'].round().astype(int)

    most_frequent = max(a['visitId'])
    least_frequent = min(a['visitId'])

    frequent_diff = (most_frequent - least_frequent) / 5
    a['visitId'] = ((a['visitId']-least_frequent)/frequent_diff)
    a['visitId'] = a['visitId'].round().astype(int)
    a.columns=['Visitor ID', 'Frequency', 'Recency']
    return a

def frequency(df):

    return df

def main():
    path = get_path()
    data = get_raw(path)
    recent = recency(data)
    print recent
    sys.exit()
    analysis(recent)



if __name__ == '__main__':
    main()
