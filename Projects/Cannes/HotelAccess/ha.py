import pandas as pd
pd.set_option('display.width', 320)


dels = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/cannesdels.csv')).drop_duplicates().drop_duplicates(subset='Delegate_ID').dropna()
sesh = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/hotelsessions.csv'))
reg = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/hotelreg.csv')).drop_duplicates()



a = reg[~reg['Name'].isin(dels['Name'])]

map = {'United Kingdom Of Great Britain And Northern Ireland': 'UK', 'United Kingdom of Great Britain and Northern Ireland': 'UK',
       'United States Of America': 'USA', 'United States of America': 'USA', 'united states of America': 'USA'}
a['Country'] = a['Country'].replace(map)



print a.groupby('Country')['Name'].count().reset_index().sort_values('Name', ascending=False)