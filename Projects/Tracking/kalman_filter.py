import numpy as np
import pandas as pd
import pandas.io.sql as pdsql
from Code.config import get_path, get_pwd
from clean_functions import clean_ble
import psycopg2
import time
from filterpy.kalman import KalmanFilter
import sys

# PATH = get_path()
#
# conn = psycopg2.connect(
#     host='redshift-clustor.cndr1rlsl2px.eu-west-1.redshift.amazonaws.com',
#     user='root',
#     port=5439,
#     password=get_pwd(),
#     dbname='autumnfair')
#
# cur = conn.cursor()
#
# df = clean_ble(PATH, pd.read_sql_query("SELECT * FROM bettshowexcel2017.logs WHERE type = 'ble' LIMIT 1000000", conn))


vals = np.matrix([[0.1, 5, 0], [0.4, 8, 1], [0.5, 10, 2], [1, 15, 3], [1, 19, 4], [1, 23, 5],
                  [1, 20, 6], [1.1, 22, 7], [1.3, 24, 8], [1.2, 18, 9], [1, 19, 10], [1, 20, 11]])

R = np.diag([0.02, 0.02])
x = np.matrix([[0], [0], [0], [0]])
u = np.matrix([[0], [0], [0], [0]])
P = np.random.randint(10, size=(4,4))
H = np.matrix([[1, 0, 0, 0], [0, 1, 0, 0]])
I = np.eye(4)

for i in range(len(vals)):
    dt = 1

    F = np.matrix([[1, 0, dt, 0],
                   [0, 1, 0, dt],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])

    x = (F * x) + u
    P = (F * P) * F.T

    Z = np.matrix([vals[i, 0] * R[0, 0] * (np.random.rand()),
                   vals[i, 1] * R[1, 1] * (np.random.rand())])

    y = Z.T - (H * x)

    S = ((H * P) * H.T) + R

    K = (P * H.T) * np.linalg.inv(S)
    x = x + (K * y)
    P = (I - (K*H)) * P

    print x[0, 0], x[1, 0]
