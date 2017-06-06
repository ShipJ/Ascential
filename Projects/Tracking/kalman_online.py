import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


x = [0, 1, 2, 3, 4, 5]
y = [0, 1, 4, 9, 16, 25]


x_cycle, x_trend = sm.tsa.filters.hpfilter(x)
y_cycle, y_trend = sm.tsa.filters.hpfilter(y)


# first_journey = journeys_rand[2]
# print first_journey
#
# actual_coords = first_journey[['x', 'y', 'x_v', 'y_v']].as_matrix()
#
# positions = actual_coords
# decay = 0.5 #start = 0.03
# R = np.diag([0.005, 0.005]) # start = 0.02
# P = np.matrix(np.random.rand(4,4))
# H = np.matrix([[1, 0, 0, 0],
#                [0, 1, 0, 0]])
# I = np.eye(4)
#
# smoothed = []
# start_t = 0
# i = 0
# for position in positions[1:]:
#     dt = first_journey.iloc[i]['secs']
#     F = np.matrix([[1, 0, dt, 0],
#                    [0, 1, 0, dt],
#                    [0, 0, 1, 0],
#                    [0, 0, 0, 1]])
#     P = np.multiply(P, (1 + (decay * dt)))
#     x_uncertain = position[0] + (300 * R[0, 0] * 2 * (np.random.rand() - 0.5))
#     y_uncertain = position[1] + (100 * R[1, 1] * 2 * (np.random.rand() - 0.5))
#     Z = np.matrix([[x_uncertain],
#                    [y_uncertain]])
#
#     x = F * np.matrix(position).T
#
#     P = F * P * F.T
#     y = Z - (H * x)
#     S = (H * P * H.T) + R
#     K = P * H.T * np.linalg.inv(S)
#     x = x + (K * y)
#     P = I - (K * H * P)
#
#     smoothed.append(np.array(x.T)[0])
#     i+=1
#
# a = np.array(smoothed)
# print smoothed
#
# x = a[:, 0]
# y = a[:, 1]
#
# w = np.array(positions)
# x_actual = w[:, 0]
# y_actual = w[:, 1]
#
#
#
# plt.plot(x, y, c='r')
# # plt.plot(x_actual, y_actual, c='b')
# plt.show()
#
#
# # kalman filter
