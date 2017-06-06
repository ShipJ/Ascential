import numpy as np
import pandas as pd
import pandas.io.sql as pdsql
from Code.config import get_path, get_pwd
from clean_functions import clean_ble
import psycopg2
import time
from filterpy.kalman import KalmanFilter
import sys
import matplotlib.pyplot as plt

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


positions = [[0, 0, 0, 0], [0.5, 1, 1, 1], [1, 2, 1, 1], [1.5, 3, 1, 1], [2, 4, 0, 0],
             [2.5, 5, 0, 0], [3, 5, 1, 1], [3.5, 5, 1, 1], [4, 6, 1, 1], [4.5, 6, 0, 0],
             [5, 4, 0, 0], [6, 4, 1, 1], [7, 5, 1, 1], [10, 4, 1, 1], [9, 4, 0, 0],
             [8, 4, 0, 0], [6, 4, 1, 1], [4, 4, 1, 1], [4, 4, 1, 1], [4, 4, 0, 0],]

R = np.diag([0.02, 0.02])
u = np.matrix([[0],
               [0],
               [0],
               [0]])
P = np.matrix(np.random.rand(4,4))
H = np.matrix([[1, 0, 0, 0],
               [0, 1, 0, 0]])
I = np.eye(4)

smoothed = []
for position in positions:
    dt = 1
    F = np.matrix([[1, 0, dt, 0],
                   [0, 1, 0, dt],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    x_uncertain = position[0] + (3000 * R[0, 0] * 2 * (np.random.rand() - 0.5))
    y_uncertain = position[1] + (1000 * R[1, 1] * 2 * (np.random.rand() - 0.5))
    Z = np.matrix([[x_uncertain],
                   [y_uncertain]])

    x = F * np.matrix(position).T + u

    P = F * P * F.T
    y = Z - (H * x)
    S = (H * P * H.T) + R
    K = P * H.T * np.linalg.inv(S)
    x = x + (K * y)
    P = I - (K * H * P)

    smoothed.append(np.array(x.T)[0])

a = np.array(smoothed)

x = a[:, 0]
y = a[:, 1]

w = np.array(positions)
x_actual = w[:, 0]
y_actual = w[:, 1]


plt.plot(x, y, c='r')
plt.plot(x_actual, y_actual, c='b')
plt.show()









sys.exit()

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
