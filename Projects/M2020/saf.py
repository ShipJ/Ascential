import pandas as pd
import numpy as np
import os

sales = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/sales.csv'))
scans15 = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/scans_15.csv'))
scans16 = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/scans_16_2.csv'))

x = sales[sales['IsWon'] == True]

a1 = x[x['Exhibition'] == 'Autumn Fair International 2015']
a2 = x[x['Exhibition'] == 'Spring Fair International 2016']

co1 = pd.unique(a1['Company'])
co2 = pd.unique(a2['Company'])

c = pd.DataFrame(np.intersect1d(co1,co2))
c.columns=['Company']
c.to_csv('/Users/JackShipway/Desktop/companies.csv', index=None)

sys.exit()




sys.exit()




b = scans15[scans15['Type'] == 'lead']
c = scans16[scans16['Type'] == 'lead']

d = b[b['Action'] == 'scan']
e = c[c['Action'] == 'scan']

d = d[['Scan Time', 'Full Name Visitor', 'Partner', 'Exhibition', 'Visitor Code']]
e = e[['Scan Time', 'Full Name Visitor', 'Partner', 'Exhibition', 'Visitor Code']]

f = pd.DataFrame(pd.concat([d, e])).reset_index(drop=True)

z = y[['Exhibition', 'Company', 'CompanySector', 'OpportunityId', 'ShowSector', 'ProductPrice', 'MainCustomerObjectives',
       'Hall', 'StandLocationType', 'StandType', 'Width', 'Length']].reset_index(drop=True)

data = pd.DataFrame(f.merge(z, left_on=['Partner', 'Exhibition'], right_on=['Company', 'Exhibition'], how='inner'))

data.to_csv('/Users/JackShipway/Desktop/data2.csv', index=None)






















