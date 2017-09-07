import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
plt.rcParams['figure.facecolor']='white'
from Code.config import get_path
from clean import clean


def sales_by_stand_size(df):
    """
    
    :param df: 
    :return: 
    """

    ''' Sales by stand size: Could use net/gross/chargeable area (noticeable difference?) '''
    area_by_co = pd.DataFrame(df.groupby(['Company', 'Exhibition'])['NetArea'].first().reset_index())
    sales_by_co = pd.DataFrame(df.groupby(['Company', 'Exhibition'])['ProductPrice'].sum().reset_index())
    area_by_co['Sales'] = sales_by_co['ProductPrice']

    area_by_co = area_by_co[(area_by_co['Sales'] > 0) & (area_by_co['Sales'] < 1000000)]
    area_by_co = area_by_co[(area_by_co['NetArea'] > 0) & (area_by_co['NetArea'] < 1000)]

    identified_small = a[(a['NetArea'] < 100) & (a['Sales'] > 50000)]['Company']
    identified_big = a[((a['NetArea'] > 100) & (a['NetArea'] < 150))]
    identified_big = identified_big[(identified_big['Sales'] > 10000) & (identified_big['Sales'] < 15000)]['Company']

    # Companies with small area but high spend
    smallBigSpend = df[df['Company'].isin(list(pd.unique(identified_small)))]
    z = pd.DataFrame(smallBigSpend.groupby(['Exhibition', 'ExhibitorType'])['Company'].count().reset_index())
    z.to_csv('/Users/JackShipway/Desktop/smallBigSpend.csv', index=None)

    bigSmallSpend = data[data['Company'].isin(list(pd.unique(identified_big)))]
    y = pd.DataFrame(smallBigSpend.groupby(['Exhibition', 'ExhibitorType'])['Company'].count().reset_index())
    y.to_csv('/Users/JackShipway/Desktop/bigSmallSpend.csv', index=None)


    highPerform = pd.DataFrame(data[data['Company'].isin(list(pd.unique(smallBigSpend['Company'])))])
    lowPerform = pd.DataFrame(data[data['Company'].isin(list(pd.unique(bigSmallSpend['Company'])))])

    highPerform = pd.DataFrame(highPerform.groupby(['Exhibition'])['StandLocationType'].first().reset_index())
    lowPerform = pd.DataFrame(lowPerform.groupby(['Exhibition'])['StandLocationType'].first().reset_index())

    return highPerform, lowPerform


def sales_by_exhibition(df):
    exhibition = pd.DataFrame(df.groupby(['Exhibition', 'Company'])['ProductPrice'].sum().reset_index())
    mean_spend = exhibition.groupby(['Exhibition'])['ProductPrice'].mean().reset_index()
    exhibition = pd.DataFrame(exhibition.groupby('Exhibition')['Company'].count().reset_index())
    exhibition['MeanSpend'] = mean_spend['ProductPrice']
    return exhibition

def sales_by_exhibitor_type(df):
    ex_type = df.groupby(['Exhibition', 'Company'])['StandType'].first().reset_index()
    ex_type_sales = df.groupby(['Exhibition', 'Company'])['ProductPrice'].sum().reset_index()
    ex_type['Sales'] = ex_type_sales['ProductPrice']
    ex_type = ex_type.dropna()
    return pd.DataFrame(ex_type.groupby(['Exhibition', 'StandType'])['Sales'].sum().reset_index())

def sales_by_firm_objective(df):
    firm_objectives = df[~df['MainCustomerObjectives'].isnull()]
    return pd.DataFrame(firm_objectives.groupby('MainCustomerObjectives')['ProductPrice'].sum().reset_index())

def sales_by_hall(df):
    hall = df.groupby(['Exhibition', 'Company'])['Hall'].first().reset_index()
    hall_sales = df.groupby(['Exhibition', 'Company'])['ProductPrice'].sum().reset_index()
    hall['Sales'] = hall_sales['ProductPrice']
    hall = hall.dropna()
    sales_by_type = hall.groupby(['Exhibition', 'Hall'])['Sales'].sum().reset_index()
    sales_by_hall_by_exhibition = pd.DataFrame(sales_by_type.groupby(['Exhibition', 'Hall'])['Sales'].sum().reset_index())
    total_sales_by_hall = pd.DataFrame(sales_by_type.groupby('Hall')['Sales'].sum().reset_index())
    return sales_by_hall_by_exhibition, total_sales_by_hall


def unique_co(df):
    unique = pd.DataFrame(df.groupby(['Exhibition', 'Company'])['ProductPrice'].sum().reset_index())
    unique_by_exhibition = pd.DataFrame(unique.groupby('Exhibition')['Company'].count().reset_index())
    return unique_by_exhibition


if __name__ == '__main__':

    # Get path to data
    PATH = get_path()

    # Grab raw data
    headers = pd.DataFrame(pd.read_csv(PATH+'/Footfall/Data/Raw/headers.csv'))
    data = pd.DataFrame(pd.read_csv(PATH+'/Footfall/Data/Raw/Spring_Autumn.txt', sep='\t', names=headers, low_memory=False))
    # Clean data and store in csv
    print clean(data)

    clean(data).to_csv('/Users/JackShipway/Desktop/SAFair.csv', index=None)





    sys.exit()

    # Grab processed data
    data = pd.DataFrame(pd.read_csv(PATH+'/Processed/cleanedSpringAutumn.csv', low_memory=False))


    ''' Individual Analyses '''

    # Number of unique co's by exhibition
    unique_co(data).to_csv('/Processed/uniqueCo.csv', index=None)

    # Sales by exhibition
    sales_by_exhibition(data).to_csv(PATH+'/Processed/sales_by_exhibition.csv', index=None)

    # Sales by stand size
    sales_by_stand_size(data)[0].to_csv(PATH+'/Processed/high_perform.csv', index=None)
    sales_by_stand_size(data)[1].to_csv(PATH+'/Processed/low_perform.csv', index=None)
    
    # Sales by exhibitor type
    sales_by_exhibitor_type(data).to_csv(PATH+'/Processed/sales_by_ex_type.csv', index=None)
    
    # Sales by firm objectives
    sales_by_firm_objective(data).to_csv(PATH+'/Processed/salesByFirmObjective.csv', index=None)
    
    # Sales by Hall
    sales_by_hall(data)[0].to_csv(PATH+'/Processed/exhibition_sales_by_hall.csv', index=None)
    sales_by_hall(data)[1].to_csv(PATH+'/Processed/total_sales_by_hall.csv', index=None)



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
















































