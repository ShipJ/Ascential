import pandas as pd
import numpy as np
from clean import clean
import matplotlib.pyplot as plt
plt.rcParams['figure.facecolor']='white'
import sys
from Code.config import get_path

PATH = get_path()

a = np.zeros(10)

print a
sys.exit()



# # Run the code below to transform the original standLoc set to a cleaned version
# headers = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/Ascential/WRC/headers.csv'))
# standLoc = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/Ascential/WRC/SpringAutumn.txt',
#                                 sep='\t', names=headers, low_memory=False))
#
# clean(standLoc).to_csv('/Users/JackShipway/Desktop/Ascential/WRC/cleanedSpringAutumn.csv', index=None)


# data = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/Ascential/WRC/cleanedSpringAutumn.csv', low_memory=False))
# seasons = {'Spring13': 0, 'Autumn13': 1, 'Spring14': 2, 'Autumn14': 3, 'Spring15': 4, 'Autumn15': 5, 'Spring16': 6,
#            'Autumn16': 7, 'Spring17': 8, 'Autumn17': 9, 'Spring18': 10}
# data['Exhibition'].replace(seasons, inplace=True)
# seasonOrd = [idx for idx, val in sorted(seasons.items(), key=lambda x: x[1])]


# ''' Sales by stand size '''
# a = pd.DataFrame(data.groupby(['Company', 'Exhibition'])['NetArea'].first().reset_index())
# b = pd.DataFrame(data.groupby(['Company', 'Exhibition'])['ProductPrice'].sum().reset_index())
# a['Sales'] = b['ProductPrice']
#
# a = a[(a['Sales'] > 0) & (a['Sales'] < 1000000)]
# a = a[(a['NetArea'] > 0) & (a['NetArea'] < 1000)]
#
# identified_small = a[(a['NetArea'] < 100) & (a['Sales'] > 50000)]['Company']
# identified_big = a[((a['NetArea'] > 100) & (a['NetArea'] < 150))]
# identified_big = identified_big[(identified_big['Sales'] > 10000) & (identified_big['Sales'] < 15000)]['Company']


# Companies with small area but high spend
# smallBigSpend = data[data['Company'].isin(list(pd.unique(identified_small)))]
# z = pd.DataFrame(smallBigSpend.groupby(['Exhibition', 'ExhibitorType'])['Company'].count().reset_index())
# z.to_csv('/Users/JackShipway/Desktop/smallBigSpend.csv', index=None)

# bigSmallSpend = data[data['Company'].isin(list(pd.unique(identified_big)))]
# y = pd.DataFrame(smallBigSpend.groupby(['Exhibition', 'ExhibitorType'])['Company'].count().reset_index())
# y.to_csv('/Users/JackShipway/Desktop/bigSmallSpend.csv', index=None)


# highPerform = pd.DataFrame(data[data['Company'].isin(list(pd.unique(smallBigSpend['Company'])))])
# lowPerform = pd.DataFrame(data[data['Company'].isin(list(pd.unique(bigSmallSpend['Company'])))])

# print highPerform.groupby(['Exhibition', 'Company'])['CompanySectors'].first().reset_index()
# print lowPerform.groupby(['Exhibition', 'Company'])['CompanySectors'].first().reset_index()

# highPerformSectors = ['Contemporary', 'Accessories', 'Luggage', 'Home', 'Dining', 'Government' 'Independent', 'DIY']
# lowPerformSectors = ['Retail, Toys, Gadgets']






# highPerform = highPerform.groupby(['Exhibition'])['StandLocationType'].first().reset_index()
# lowPerform = lowPerform.groupby(['Exhibition'])['StandLocationType'].first().reset_index()





# for i in range(11):
#     j = a[a['Exhibition'] == i]
#     plt.scatter(j['NetArea'], j['Sales'])
#     plt.grid(), plt.xlabel('Net Area (m^2)'), plt.ylabel('Sales (GBP)')
#     plt.show()
#     print pearsonr(j['NetArea'], j['Sales'])



#
# c = pd.DataFrame(a.groupby('Exhibition')['NetArea'].mean().reset_index())
# c['Sales'] = pd.DataFrame(a.groupby('Exhibition')['Sales'].sum().reset_index())['Sales']
#
# c.to_csv('/Users/JackShipway/Desktop/salesStandArea.csv', index=None)




#
#
#
# a = pd.DataFrame(data.groupby(['Exhibition', 'Company'])['ProductPrice'].sum().reset_index())
# b = pd.DataFrame(a.groupby('Exhibition')['Company'].count().reset_index())
#
# b.to_csv('/Users/JackShipway/Desktop/uniqueCo.csv', index=None)
#
#
#
#
#
#

# sys.exit()


''' 4. SALES BY EXHIBITION '''
expo = pd.DataFrame(data.groupby(['Exhibition'])['ProductPrice'].sum().reset_index())
a = pd.DataFrame(data.groupby(['Exhibition', 'Company'])['ProductPrice'].sum().reset_index())
b = a.groupby(['Exhibition'])['ProductPrice'].mean().reset_index()
a = pd.DataFrame(a.groupby('Exhibition')['Company'].count().reset_index())
a['AverageSpend'] = b['ProductPrice']

a.to_csv('/Users/JackShipway/Desktop/avgSpendNumCos.csv', index=None)



# expo['Expo'] = seasonOrd
#
# print expo



#
# expo.to_csv('/Users/JackShipway/Desktop/salesByExpo.csv', index=None)
#
# plt.plot(range(0, 11, 2),
#          np.divide(expo[expo['Exhibition'] % 2 == 0]['ProductPrice'], 1000000), '-x',
#          label='Spring') #spring
# plt.plot(range(1, 10, 2),
#          np.divide(expo[expo['Exhibition'] % 2 != 0]['ProductPrice'], 1000000), '-x', c='red',
#          label='Autumn') #autumn
# plt.grid(), plt.legend(), plt.xlim([-0.5,10.5])
# plt.xlabel('Exhibition', fontsize=18), plt.ylabel('Total Spent (m)', fontsize=18)
# plt.xticks(range(len(expo)), seasonOrd, rotation='horizontal')
# plt.show()
# sys.exit()


''' SALES BY COUNTRY/CONTINENT '''
# salesByCountry = data[~data['BillingCountry'].isnull()]
# sbc = salesByCountry['BillingCountry'].str.lower()
# salesByCountry = salesByCountry.assign(Country=sbc.values)
# cityMap = {'cape town': 'south africa', 'county durham': 'united kingdom', 'dubai': 'united arab emirates',
#            'telford': 'united kingdom', 'uk': 'united kingdom', 'england': 'united kingdom', 'united kindgom':
#            'united kingdom', 'u.s.a.': 'united states', 'viet nam': 'vietnam', 'jersey': 'united kingdom',
#            'russian federation': 'russia', 'north yorkshire': 'united kingdom', 'holland': 'the netherlands',
#            'paris': 'france', 'usa': 'united states'}
# salesByCountry['Country'].replace(cityMap, inplace=True)
# salesByCountry = salesByCountry.drop('BillingCountry', axis=1)
# spendByCountry = pd.DataFrame(salesByCountry.groupby('Country')['ProductPrice'].sum().reset_index())
# spendByCountry.to_csv('/Users/JackShipway/Desktop/Ascential/WRC/spendByCountry.csv', index=None)
# plt.scatter(range(len(spendByCountry)), spendByCountry['ProductPrice']), plt.grid()
# plt.xlim([0, 100])
# plt.xlabel('Country', fontsize=18), plt.ylabel('Total Spent', fontsize=18)
# plt.xticks(range(len(spendByCountry)), spendByCountry['Country'], rotation='vertical')
# plt.show()
# sys.exit()

''' SALES BY COMPANY SECTOR '''

''' SALES BY PRODUCT FAMILY '''
# salesProductFamily = data[~data['ProductFamily'].isnull()]
# prodFam = pd.DataFrame(salesProductFamily.groupby(['Exhibition', 'ProductFamily'])['ProductPrice'].sum().reset_index())
# prodFam.to_csv('/Users/JackShipway/Desktop/prodFam.csv', index=None)


''' 6. How have cancellation charges changed through time? '''
# cancel = data[data['ProductFamily'] == 'Cancellation Charge'].reset_index(drop=True)
# a = pd.DataFrame(cancel.groupby('Exhibition')['Company'].count().reset_index())
# a.to_csv('/Users/JackShipway/Desktop/cancelNumber.csv', index=None)


# cancelTime = cancel.groupby('Exhibition')['ProductPrice'].sum().reset_index()
# print cancelTime

# data = data[~data['ExhibitorType'].isnull()]
# exhibitorType = pd.DataFrame(data.groupby(['Exhibition', 'ExhibitorType'])['ProductPrice'].sum().reset_index())
# exhibitorType.to_csv('/Users/JackShipway/Desktop/exhibitorType.csv', index=None)
# sys.exit()

# plt.plot(range(0, 11, 2),
#          np.divide(cancelTime[cancelTime['Exhibition'] % 2 == 0]['ProductPrice'], 1000000), '-x',
#          label='Spring') #spring
# plt.plot(range(1, 10, 2),
#          np.divide(cancelTime[cancelTime['Exhibition'] % 2 != 0]['ProductPrice'], 1000000), '-x', c='red',
#          label='Autumn') #autumn
# plt.grid(), plt.legend(), plt.xlim([-0.5,10.5])
# plt.xlabel('Exhibition', fontsize=18), plt.ylabel('Total Cancellation Charges (m)', fontsize=18)
# plt.xticks(range(len(cancelTime)), seasonOrd, rotation='horizontal')
# plt.show()


''' 7: Open close difference days - is there a reduction in time as the event matures? '''
# openClose = data[~data['CreateCloseDateDiff'].isnull()]
# openClose = openClose[openClose['StageName'] == 4]
# openCloseExpo = pd.DataFrame(openClose.groupby('Exhibition')['CreateCloseDateDiff'].mean().reset_index())
# openCloseExpo.to_csv('/Users/JackShipway/Desktop/openClose.csv', index=None)
# sys.exit()

# plt.plot(range(0, 11, 2), openCloseExpo[openCloseExpo['Exhibition'] % 2 == 0]['CreateCloseDateDiff'], '-x',
#          label='Spring') #spring
# plt.plot(range(1, 10, 2), openCloseExpo[openCloseExpo['Exhibition'] % 2 != 0]['CreateCloseDateDiff'], '-x', c='red',
#          label='Autumn') #autumn
# plt.grid(), plt.legend(), plt.xlim([-0.5,10.5])
# plt.xlabel('Exhibition', fontsize=18), plt.ylabel('Mean days to closure', fontsize=18)
# plt.xticks(range(len(openCloseExpo)), seasonOrd, rotation='horizontal')
# plt.show()

''' 8.1: Sales by Stand location type '''
# standLoc = data.groupby(['Exhibition', 'Company'])['StandLocationType'].first().reset_index()
# standSales = data.groupby(['Exhibition', 'Company'])['ProductPrice'].sum().reset_index()
# standLoc['Sales'] = standSales['ProductPrice']
# standLoc = standLoc.dropna()
# salesStandLoc = pd.DataFrame(standLoc.groupby(['Exhibition', 'StandLocationType'])['Sales'].sum().reset_index())
# salesStandLoc.to_csv('/Users/JackShipway/Desktop/salesStandLoc.csv', index=None)
#
# sys.exit()
# salesByType = data.groupby(['Exhibition', 'StandLocationType'])['Sales'].sum().reset_index()
#
# print salesByType
# plt.plot(range(0, 11, 2), salesByType[salesByType['Exhibition'] % 2 == 0]['Sales'], '-x',
#          label='Spring') #spring
# plt.plot(range(1, 10, 2), salesByType[salesByType['Exhibition'] % 2 != 0]['Sales'], '-x', c='red',
#          label='Autumn') #autumn
# plt.grid(), plt.legend(), plt.xlim([-0.5,10.5])
# plt.xlabel('Exhibition', fontsize=18), plt.ylabel('Mean days to closure', fontsize=18)
# plt.xticks(range(len(salesByType)), seasonOrd, rotation='horizontal')
# plt.show()


''' 8.2: Sales by Hall '''
# hall = data.groupby(['Exhibition', 'Company'])['Hall'].first().reset_index()
# hallSales = data.groupby(['Exhibition', 'Company'])['ProductPrice'].sum().reset_index()
# hall['Sales'] = hallSales['ProductPrice']
# hall = hall.dropna()
# hallSalesByType = hall.groupby(['Exhibition', 'Hall'])['Sales'].sum().reset_index()
# hallSalesByType = hallSalesByType[hallSalesByType['Hall'] != '10-Dec']
#
#
# expoSalesByHall = pd.DataFrame(hallSalesByType.groupby(['Exhibition', 'Hall'])['Sales'].sum().reset_index())
# totalSalesByHall = pd.DataFrame(hallSalesByType.groupby('Hall')['Sales'].sum().reset_index())
#
# expoSalesByHall.to_csv('/Users/JackShipway/Desktop/expoSalesByHall.csv', index=None)
# totalSalesByHall.to_csv('/Users/JackShipway/Desktop/totalSalesByHall.csv', index=None)


# plt.bar(range(len(totalSalesByHall)), totalSalesByHall['Sales'])
# plt.show()

# plt.plot(range(0, 11, 2), hallSalesByType[hallSalesByType['Exhibition'] % 2 == 0]['Sales'], '-x',
#          label='Spring') #spring
# plt.plot(range(1, 10, 2), hallSalesByType[hallSalesByType['Exhibition'] % 2 != 0]['Sales'], '-x', c='red',
#          label='Autumn') #autumn
# plt.grid(), plt.legend(), plt.xlim([-0.5,10.5])
# plt.xlabel('Exhibition', fontsize=18), plt.ylabel('Mean days to closure', fontsize=18)
# plt.xticks(range(len(hallSalesByType)), seasonOrd, rotation='horizontal')
# plt.show()



''' 8.3: Sales by exhibitor type '''
# exType = data.groupby(['Exhibition', 'Company'])['StandType'].first().reset_index()
# exTypeSales = data.groupby(['Exhibition', 'Company'])['ProductPrice'].sum().reset_index()
# exType['Sales'] = exTypeSales['ProductPrice']
# exType = exType.dropna()
# SalesByExType = pd.DataFrame(exType.groupby(['Exhibition', 'StandType'])['Sales'].sum().reset_index())
# SalesByExType.to_csv('/Users/JackShipway/Desktop/salesByExhibitorType.csv', index=None)



''' 9. Firm objectives: groupings/trend analysis? '''
# firmObjectives = data[~data['MainCustomerObjectives'].isnull()]
# salesByFirmObjective = pd.DataFrame(firmObjectives.groupby('MainCustomerObjectives')['ProductPrice'].sum().reset_index())
# salesByFirmObjective.to_csv('/Users/JackShipway/Desktop/salesByFirmObjective.csv', index=None)


#
# plt.bar(range(11), np.divide(salesByFirmObjective['ProductPrice'], 1000000))
# plt.xticks(range(11), salesByFirmObjective['MainCustomerObjectives'] , rotation='vertical')
# plt.grid(), plt.xlabel('Customer Objective'), plt.ylabel('Total Spend (m)')
# plt.show()



































