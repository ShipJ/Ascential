import pandas as pd
pd.set_option('display.width', 380)
import numpy as np

from collections import Counter
from Code.config import get_path




''' Grab data '''
path = get_path()+'/Raw/HotelAccess'

# hotel_access = pd.DataFrame(pd.read_csv(path+'/HotelAccess.csv'))
# delegates_16 = pd.DataFrame(pd.read_csv(path+'/delegates16.csv').drop('PaymentMethod', axis=1))
# delegates_17 = pd.DataFrame(pd.read_csv(path+'/delegates17.csv').drop('Delegate_ID', axis=1))
#
# # Multiple people under same email address
# counts = Counter(hotel_access['Email Address'])
# a = [(key, value) for key, value in counts.iteritems() if value > 1]

# # People in 16 not in 17
# print len(np.setdiff1d(pd.unique(delegates_16['Registered - CompanyName']), pd.unique(delegates_17['Registered - CompanyName'])))
# # People in 17 not in 16
# print len(np.setdiff1d(pd.unique(delegates_17['Registered - CompanyName']), pd.unique(delegates_16['Registered - CompanyName'])))
#
#
# df = delegates_17.dropna(subset=['ProductGroup', 'Registered - PersonEmail'])
#
# dg = hotel_access.dropna(subset=['Email Address'])
#
# dh = df.merge(dg, left_on='Registered - PersonEmail', right_on='Email Address', how='inner')
#
#
# a = Counter(dh['Registered - PersonEmail'])
#
# print [(key, value) for key, value in a.iteritems() if value > 2]


# print hotel_access.groupby('Country')['Email Address'].count().reset_index().sort_values('Email Address', ascending=True)

# print delegates_17[delegates_17['Registered - CompanyName'] == 'Google']['Registered - PersonEmail']


# People with hotel access with multiple emails, who also have a pass
# for i in a[1:]:
#     print delegates_17[delegates_17['Registered - PersonEmail'] == i[0]]



# rev = pd.DataFrame(pd.read_csv(path+'/revenue.csv'))
#
#
#
# a = rev.groupby('ProductName')['Revenue'].sum().sort_values(ascending=False).head(10).reset_index()
# a.to_csv(path+'/Tableau/revByProduct.csv', index=None)

# a = a[~a['JobBanding'].isin(['Editors', 'Owners', 'Photographer', 'Product Developer',
#                              'Production', 'Recruitment', 'Research'])]
#
# a.to_csv(path+'/Tableau/bandingRevenue.csv', index=None)








combined = pd.DataFrame(pd.read_csv(path+'/combined.csv'))

no_pass = combined[combined['Banding'] == 'No Pass']
has_pass = combined[combined['Banding'] != 'No Pass']










#
# print has_pass.groupby('Job')
#
# sys.exit()
#
# top10 = pd.DataFrame(no_pass.groupby('Company')['EmailAddress'].count().sort_values(ascending=False).head(10).reset_index())
# no_pass_top10 = pd.DataFrame(no_pass[no_pass['Company'].isin(top10['Company'])])
#
#
# a = has_pass[has_pass['JobBanding'] == 'C-Level']
# b = no_pass[no_pass['JobBanding'] == 'C-Level']
#
# c = a.groupby('ProductName')['EmailAddress'].count().sort_values(ascending=False).head(6).reset_index()
#
#
# c.to_csv(path+'/Tableau/productsPass.csv', index=None)
#
#
#
#
#





# c = no_pass.groupby('JobBanding')['EmailAddress'].count().reset_index()
# c['EmailAddress'] = c['EmailAddress']/sum(c['EmailAddress'])
#
#
# b = has_pass.groupby('JobBanding')['EmailAddress'].count().reset_index()
# b['EmailAddress'] = b['EmailAddress']/sum(b['EmailAddress'])
# d = pd.DataFrame(b.merge(c, on='JobBanding'))
#
#
# d.to_csv(path+'/Tableau/jobbandsall.csv', index=None)





# a = has_pass[has_pass['Company'].isin(top10['Company'])]
#
# b = a.groupby('JobBanding')['EmailAddress'].count().reset_index()
# b['EmailAddress'] = b['EmailAddress']/sum(b['EmailAddress'])
#
# c = no_pass_top10.groupby('JobBanding')['EmailAddress'].count().reset_index()
# c = c[c['JobBanding'].isin(b['JobBanding'])]
# c['EmailAddress'] = c['EmailAddress']/sum(c['EmailAddress'])
# d = pd.DataFrame(b.merge(c, on='JobBanding'))
#
# d.to_csv(path+'/Tableau/jobBandingspassvsnopass.csv', index=None)










# a = no_pass.dropna(subset=['EmailAddress', 'First Name', 'Last Name'])
# a = a.drop(['EmailAddress.1', 'Email Address_local', 'Email Address_domain', 'Barcode', 'Referral Code',
#             'Created At', 'Date', 'Time', 'ProductGroup', 'ProductName', 'Registered - ValueSegment',
#             'RegistrationDateTime', 'banding', 'Registered - JobRole', 'NewToCannes', 'NewToLions',
#             'Registered - Company ValueSegment', 'Job Title', 'Registered - HoldCo', 'RegistrationType',
#             'NewToFestival', 'Registered - SeniorityLevel', 'Banding'], axis=1)
#
# b = pd.DataFrame(a.groupby('JobBanding')['EmailAddress'].count().reset_index())
# b.to_csv(path+'/Tableau/jobBanding.csv', index=None)


# a = no_pass_top10.dropna(subset=['EmailAddress', 'First Name', 'Last Name'])
# a = a.drop(['EmailAddress.1', 'Email Address_local', 'Email Address_domain', 'Barcode', 'Referral Code',
#             'Created At', 'Date', 'Time', 'ProductGroup', 'ProductName', 'Registered - ValueSegment',
#             'RegistrationDateTime', 'banding', 'Registered - JobRole', 'NewToCannes', 'NewToLions',
#             'Registered - Company ValueSegment', 'Job Title', 'Registered - HoldCo', 'RegistrationType',
#             'NewToFestival', 'Registered - SeniorityLevel', 'Banding'], axis=1)
#
# b = pd.DataFrame(a.groupby('JobBanding')['EmailAddress'].count().reset_index())
# b.to_csv(path+'/Tableau/jobBanding_top10.csv', index=None)












#
# a = has_pass[has_pass['Company'].isin(big_dogs['Company'])]
#
# b = pd.DataFrame(a.groupby('Registered - SeniorityLevel')['EmailAddress.1'].count().reset_index())
# c = pd.DataFrame(a.groupby('ProductName')['EmailAddress.1'].count().reset_index())








# for i in big_dogs:
#     a = has_pass[has_pass['Company'] == i]
#     b = no_pass[no_pass['Company'] == i]
#     print i
#     print a.groupby('Registered - SeniorityLevel')['EmailAddress.1'].count().reset_index()
#     print a.groupby('JobBanding')['EmailAddress.1'].count().reset_index()
#     print a.groupby('Country')['EmailAddress.1'].count().reset_index()
#     print b.groupby('Registered - SeniorityLevel')['EmailAddress.1'].count().reset_index()
#     print b.groupby('JobBanding')['EmailAddress.1'].count().reset_index()
#     print b.groupby('Country')['EmailAddress.1'].count().reset_index()
#     print '\n'


#
# for i in big_dogs:
#     a = has_pass[has_pass['Company'] == i]
#     print a[a['NewToCannes'] == 1]
#     print a[a['NewToFestival'] == 1]
#     print a[a['NewToLions'] == 1]
#     print '\n'


# for i in big_dogs:
#     a = has_pass[has_pass['Company'] == i]
#     print i
#     print a.groupby('ProductName')['EmailAddress.1'].count().reset_index()
#     print a.groupby('Country')['EmailAddress.1'].count().reset_index()
#     print a.groupby('Registered - SeniorityLevel')['EmailAddress.1'].count().reset_index()
#     print '\n\n'










