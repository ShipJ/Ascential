import pandas as pd
import numpy as np
from Code.config import get_path
import matplotlib.pyplot as plt

''' Set PATH variable to data directory '''
PATH = get_path()


''' Grab raw data '''
data = pd.DataFrame(pd.read_csv(PATH+'/Raw/AllDelegateTrakScanners.csv',
                                usecols=['delegateid', 'package_description', 'delegate_JobRole', 'Bucket',
                                         'Country', 'SessionHost', 'Sessiondescription', 'Scanned']))

def clean(df):
    country_map = {'104': None, '105': None, '106': None, '108': None, '110': None, '111': None, '112': None,
                   '114': None, '117': None, '121': None, '122': None, '127': None, '128': None, '131': None,
                   '138': None, '151': None, '161': None, '211': None, '118': None, 'Tokyo': 'JAPAN',
                   'shanghai': 'China', '157': None, 'Paris': None}
    df['Country'].replace(country_map, inplace=True)

    session_map = {'103': None, '110': None, '112': None, '121': None, 'BELGIUM': None, 'BRAZIL': None,
                   'CANADA': None, 'FRANCE': None, 'GERMANY': None, 'INDIA': None, 'IRELAND': None,
                   'SOUTH AFRICA': None, 'SPAIN': None, 'UNITED KINGDOM': None, 'USA': None, 'MEXICO': None,
                   'LITHUANIA': None, 'DENMARK': None, 'TURKEY': None}
    df['SessionHost'].replace(session_map, inplace=True)
    session_desc_map = {'AUSTRIA': None, 'FRANCE': None, 'JAPAN': None, 'UNITED KINGDOM': None, 'USA': None,
                        'CHINA': None}
    df['Sessiondescription'].replace(session_desc_map, inplace=True)

    bucket_map = {'ADVERTISER_/_CLIENT': 'ADVERTISER', 'ADVERTISING AGENCY': 'ADVERTISER', 'MEDIA AGENCY': 'MEDIA',
                  'MEDIA_OWNER': 'MEDIA', 'NOT_FOR_PROFIT_/_EDU': 'EDUCATION', 'PRODUCTION COMPANY': 'PRODUCTION'}
    df['Bucket'].replace(bucket_map, inplace=True)

    package_map = {'Festival Representative': 'Festival Official', 'Jury - Film Craft': 'Jury',
                   'Jury - Titanium & Integrated': 'Jury', 'Speaker (Cannes Lions)': 'Speaker Lions',
                   'Jury - Cyber': 'Jury', 'Jury - Promo & Activation': 'Jury', 'Jury - Outdoor': 'Jury',
                   'Jury - Direct': 'Jury', 'Speaker (Lions Health)': 'Speaker Health',
                   '2 Day Sawa Monday/Tuesday': '2-day', 'Jury-Design': 'Jury',
                   'Lions Health - Early Bird': 'Lions Health', 'Speaker (Lions Innovation)': 'Speaker Innovation',
                   'Lions Innovation - Early Bird': 'Lions Innovation', 'Jury - Print & Publishing': 'Jury',
                   'Jury - Film': 'Jury', 'Speaker (Lions Entertainment)': 'Speaker Entertainment',
                   'Jury - Radio': 'Jury', 'Jury - Creative Data': 'Jury',
                   '2 Day (Cannes Lions, part of Health Mini)': '2-day',
                   'Lions Entertainment - Super Early Bird': 'Lions Entertainment', '1 Day (Cannes Lions)': '1-day',
                   'Jury - Creative Effectiveness': 'Jury', 'Jury Media': 'Jury', 'Jury - Health & Wellness': 'Jury',
                   'Jury - PR': 'Jury', 'Jury - Entertainment Lions for Music': 'Jury',
                   'Jury - Glass': 'Jury', 'Jury - Entertainment': 'Jury', 'Jury Companion': 'Jury',
                   'Jury - Mobile': 'Jury', 'Palais Access (Cannes Lions)': 'Palais', 'Jury - Pharma': 'Jury',
                   '2 Day (Cannes Lions) for Innovation shortlist': '2-day',
                   'Speaker Mini (Cannes Lions)': 'Speaker Lions', 'Jury - Digital Craft': 'Jury',
                   '2 Day Sawa Sunday/Monday': '2-day', 'Jury - Innovation': 'Jury', 'Unilever Foundry': 'Unilever',
                   'Unilever Foundry Guest': 'Unilever', 'Jury - Product Design': 'Jury',
                   'Lions Entertainment - Early Bird': 'Lions Entertainment', 'Jackson': None,
                   'Speaker Mini (Lions Health)': 'Speaker Health', '1 Day (Lions Innovation)': '1-day',
                   'Palais Access (Lions Innovation)': 'Palais', '1 Day (Lions Entertainment)': '1-day',
                   '1 Day (Lions Health)': '1-day', 'Complete Student Special Offer': 'Complete Student',
                   'Palmer': None, 'Moore': None, 'Rousseau': None, 'Ceponone': None, 'Kahhat': None}
    df['package_description'].replace(package_map, inplace=True)

    return pd.DataFrame(df)

data = clean(data)


total_delegates = float(len(pd.unique(data['delegateid'])))

# Fake data for time being - need to make sure real data structured like this
scanned = np.random.choice(pd.unique(data['delegateid']), 9350, replace=False)
paying = np.random.choice(pd.unique(data['delegateid']), 8790, replace=False)
data['scanned'] = [1 if i in scanned else 0 for i in data['delegateid']]
data['paying'] = [1 if i in paying else 0 for i in data['delegateid']]

# Scanned vs. Paying
print '\033[4m\033[1mScanned vs. Paid\033[0m\033[0m'
print 'Scanned: %.1f%%' % ((len(pd.unique(data[data['scanned'] == 1]['delegateid']))/total_delegates)*100.)
print 'Not Scanned: %.1f%%' % ((len(pd.unique(data[data['scanned'] == 0]['delegateid']))/total_delegates)*100.)
print 'Paying: %.1f%%' % ((len(pd.unique(data[data['paying'] == 1]['delegateid']))/total_delegates)*100.)
print 'Not Paying: %.1f%%\n' % ((len(pd.unique(data[data['paying'] == 0]['delegateid']))/total_delegates)*100.)

# Scanned vs. Paying
scan_pay = data[(data['scanned'] == 1) & (data['paying'] == 1)]
scan_no_pay = data[(data['scanned'] == 1) & (data['paying'] == 0)]
no_scan_pay = data[(data['scanned'] == 0) & (data['paying'] == 1)]
no_scan_no_pay = data[(data['scanned'] == 0) & (data['paying'] == 0)]

# Proportion of paying by scan and vice versa
print '\033[4m\033[1mProportion of Scanned who Paid and vice versa\033[0m\033[0m'
print 'Scanned, Paid : %.1f%%' % ((len(pd.unique(scan_pay['delegateid']))/total_delegates)*100)
print 'Scanned, Not Paid : %.1f%%' % ((len(pd.unique(scan_no_pay['delegateid']))/total_delegates)*100)
print 'Not Scanned, Paid : %.1f%%' % ((len(pd.unique(no_scan_pay['delegateid']))/total_delegates)*100)
print 'Not Scanned, Not Paid : %.1f%%\n' % ((len(pd.unique(no_scan_no_pay['delegateid']))/total_delegates)*100)


# Various groupings of scanned v. paid
 # for i in data.columns:
#     print i, len(pd.unique(data[i]))
#     print pd.unique(data[i])



# for i in np.setdiff1d(data.columns, ['delegateid', 'paying', 'scanned', 'Scanned']):
#     a = pd.DataFrame(scan_pay.groupby(i)['delegateid'].nunique().reset_index())
#     plt.bar(range(len(a)), a['delegateid'])
#     plt.xticks(range(len(a)), a[i], rotation='vertical')
#     plt.show()
#     a = pd.DataFrame(scan_no_pay.groupby(i)['delegateid'].nunique().reset_index())
#     plt.bar(range(len(a)), a['delegateid'])
#     plt.xticks(range(len(a)), a[i], rotation='vertical')
#     plt.show()
#     a = pd.DataFrame(no_scan_pay.groupby(i)['delegateid'].nunique().reset_index())
#     plt.bar(range(len(a)), a['delegateid'])
#     plt.xticks(range(len(a)), a[i], rotation='vertical')
#     plt.show()
#     a = pd.DataFrame(no_scan_no_pay.groupby(i)['delegateid'].nunique().reset_index())
#     plt.bar(range(len(a)), a['delegateid'])
#     plt.xticks(range(len(a)), a[i], rotation='vertical')
#     plt.show()

# 8 Day pass holders
print '\033[4m\033[1m8-Day pass holders\033[0m\033[0m'
eight_day = ['Classic', 'Complete', 'Classic Gold', 'Classic + Companion', 'Classic Gold + Companion',
             'Classic Platinum', 'Classic Young Lion', 'Networking', 'Classic Educator', 'Creative Academy',
             'Young Lion Competitor', 'Classic Platinum Upgrade from Gold', 'Account Leadership Academy',
             'Classic Student', 'Roget Hatchuel Academy', 'Complete Young Lion', 'Creative Social Media Academy',
             'Classic Young Lion + Companion', 'Media Academy', 'Complete Student']
eight = data[data['package_description'].isin(eight_day)]
eight_group = eight.groupby('delegateid')['scanned'].sum().reset_index()

# Mean scans of 8-day holders
print np.mean(eight_group['scanned'])/8.
# % of 8-day holders scanned only once
print len(eight_group[eight_group['scanned'] == 1])/float(len(eight_group))*100


# 2 day pass holders
two_day = data[data['package_description'] == '2-day']
print np.mean(two_day.groupby('delegateid')['scanned'].sum().reset_index()['scanned'])/2.


# VIPs
vips = ['Chief Executive Officer', 'Managing Partner']
vip = data[data['delegate_JobRole'].isin(vips)]
print np.mean(vip.groupby('delegateid')['scanned'].sum().reset_index()['scanned'])/2.

# New delegates vs. Returning by Grouping

# Description of low attendance, average attendance, high attendance: which groups of people had which? Why?

#






