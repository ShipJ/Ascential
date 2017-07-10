import pandas as pd
import numpy as np
import sys

from Code.config import get_path
path = get_path()+'/Footfall/2017'

''' CL 2017 '''
CL17_dels = pd.DataFrame(pd.read_csv(path+'/CL17_Delegates.csv'))
CL17_scans = pd.DataFrame(pd.read_csv(path+'/CL17_Scans.csv'))
CL17_sessions = pd.DataFrame(pd.read_csv(path+'/CL17_SessionDescription.csv'))
CL17_hotel = pd.DataFrame(pd.read_csv(path+'/CL17_HotelAccess.csv'))

''' CL 2016 '''
CL16_dels = pd.DataFrame(pd.read_csv(path+'/CL16_Delegates.csv'))
CL16_scans = pd.DataFrame(pd.read_csv(path+'/CL16_Scans.csv'))
CL16_sessions = pd.DataFrame(pd.read_csv(path+'/CL16_SessionDescription.csv'))
CL16_sessions['SessionCode'] = CL16_sessions['SessionCode'].astype(str)

''' Merge and drop duplicates'''
CL_17 = CL17_scans.merge(CL17_dels, on='ID', how='inner').drop_duplicates(subset=['ScanTime', 'Name', 'Surname', 'Email'])
CL_17 = CL_17.merge(CL17_sessions, on='SessionCode')

CL_16 = CL16_scans.merge(CL16_dels, on='ID', how='inner').drop_duplicates(subset=['ScanTime', 'Name', 'Surname', 'Email'])
CL_16 = CL_16.merge(CL16_sessions, on='SessionCode')

CL_16_Paid = pd.DataFrame(CL_16[CL_16['PaymentStatus'].isin(['Paid', 'Pending Payment', 'Third Party'])].reset_index(drop=True))
CL_17_Paid = pd.DataFrame(CL_17[CL_17['PaymentStatus'].isin(['Paid', 'Pending Payment', 'Third Party'])].reset_index(drop=True))

# CL_16_Paid.to_csv(path+'/Final/CL16_Paid.csv', index=None)
# CL_17_Paid.to_csv(path+'/Final/CL17_Paid.csv', index=None)







''' ANALYSIS '''

''' Total number of Paying and Non-paying delegates '''
pnp_dels17 = len(pd.unique(CL17_dels['ID']))
print 'Number of paid & non-paid delegates 2017: ', pnp_dels17
print 'Number of paid & non-paid delegates 2016: ', 15872  # From Amy's work, non-paying not in DB
''' Unique Paying Delegates '''
p_dels17 = len(pd.unique(CL17_dels[CL17_dels['PaymentStatus'].isin(['Paid', 'Pending Payment', 'Third Party'])]['ID']))
p_dels16 = len(pd.unique(CL16_dels[CL16_dels['PaymentStatus'].isin(['Paid', 'Pending Payment', 'Third Party'])]['ID']))
print 'Number of paid delegates 2017: ', p_dels17
print 'Number of paid delegates 2016: ', p_dels16
''' Total Paying and Non-paying Delegates Scanned at least once'''
pnp_scanned17 = len(pd.unique(CL17_scans['ID']))
pnp_scanned16 = len(pd.unique(CL16_scans['ID']))
print 'Number of paid & non-paid delegates scanned at least once 2017: ', pnp_scanned17
print 'Number of paid & non-paid delegates scanned at least once 2016: ', pnp_scanned16
''' Total Paying Delegates Scanned more than once '''
p_scanned17 = len(pd.unique(CL_17_Paid['ID']))
p_scanned16 = len(pd.unique(CL_16_Paid['ID']))
print 'Number of paid delegates scanned at least once 2017: ', p_scanned17
print 'Number of paid delegates scanned at least once 2016: ', p_scanned16

''' Scans of Paying delegates '''
p_dels_scanned17 = len(CL_17_Paid)
p_dels_scanned16 = len(CL_16_Paid)
print 'Number of scans of paid delegates 2017: ', p_dels_scanned17
print 'Number of scans of paid delegates 2016: ', p_dels_scanned16

''' Paid but not scanned '''
print 'Number of delegates who paid but were not scanned 2017: ', p_dels17-p_scanned17
print 'Number of delegates who paid but were not scanned 2016: ', p_dels16-p_scanned16
# Further analysis here, attributes of these delegates

''' Mean scans per week/day '''
mean_pp_pw_17 =  np.mean(CL_17_Paid.groupby('ID').size().reset_index(name='scans')['scans'])
print 'Mean scans per person per week 2017: ', mean_pp_pw_17, mean_pp_pw_17/8.
mean_pp_pw_16 =  np.mean(CL_16_Paid.groupby('ID').size().reset_index(name='scans')['scans'])
print 'Mean scans per person per week 2016: ', mean_pp_pw_16, mean_pp_pw_16/8.

''' 8-day average num scans: (of those scanned) '''
p_8day17 = CL_17_Paid[CL_17_Paid['PassGroup'].isin(['Complete', 'Classic', 'Networking', 'Academy', 'Yacht'])]
mean_8day17 = np.mean(p_8day17.groupby('ID')['ScanTime'].count().reset_index()['ScanTime'])
print 'Mean scans per 8-day pass per week, per day 2017: ', mean_8day17, mean_8day17/8.
p_8day16 = CL_16_Paid[CL_16_Paid['PassGroup'].isin(['Complete', 'Classic', 'Networking', 'Academy', 'Yacht'])]
mean_8day16 = np.mean(p_8day16.groupby('ID')['ScanTime'].count().reset_index()['ScanTime'])
print 'Mean scans per 8-day pass per week, per day 2016: ', mean_8day16, mean_8day16/8.

''' frequency plot of 8-day pass holders '''
pscans_8day17 = p_8day17.groupby('ID').size().reset_index(name='scans')
pscans_8day16 = p_8day16.groupby('ID').size().reset_index(name='scans')
print 'Number of 8-day pass holders scanned at least once 2017: ', len(pscans_8day17)
print 'Number of 8-day pass holders scanned at least once 2016: ', len(pscans_8day16)
print 'Number of 8-day pass holders scanned only once 2017: ', len(pd.unique(pscans_8day17[pscans_8day17['scans'] == 1]['ID']))
print 'Number of 8-day pass holders scanned only once 2016: ', len(pd.unique(pscans_8day17[pscans_8day17['scans'] == 1]['ID']))

''' Young vs. Clsasic/Complete '''
young17 = CL_17_Paid[CL_17_Paid['PassGroup'].isin(['Standalone Student', 'Young', 'Academy'])]
print 'Mean scans per person per day student 2017: ', np.mean(young17.groupby('ID')['ScanTime'].count().reset_index()['ScanTime'])/8.
complete17 = CL_17_Paid[CL_17_Paid['PassGroup'].isin(['Classic', 'Complete'])]
print 'Mean scans per person per day classic/complete 2017: ', np.mean(complete17.groupby('ID')['ScanTime'].count().reset_index()['ScanTime'])/8.
young16 = CL_16_Paid[CL_16_Paid['PassGroup'].isin(['Standalone Student', 'Young', 'Academy'])]
print np.mean(young16.groupby('ID')['ScanTime'].count().reset_index()['ScanTime'])/8.
complete16 = CL_16_Paid[CL_16_Paid['PassGroup'].isin(['Classic', 'Complete'])]
print 'Mean scans per person per day classic/complete 2017: ', np.mean(complete16.groupby('ID')['ScanTime'].count().reset_index()['ScanTime'])/8.

''' Grouping paid delegates by seniority '''
seniority_17 = CL_17_Paid.groupby('Seniority').size().reset_index(name='scans')
vip_17 = CL_17_Paid[CL_17_Paid['Seniority'] == 6]
vip_17_scans = vip_17.groupby('ID').size().reset_index(name='scans')

print 'Total number of paying VIPs onsite: ',
print 'Number of VIPs scanned at least once: ', len(pd.unique(CL_17_Paid[CL_17_Paid['Seniority'] == 6]['ID']))
print 'Number of VIPs scanned only once: ', len(vip_17_scans[vip_17_scans['scans'] == 1])

''' Classics attended which festival '''
classic17 = CL_17[CL_17['PassGroup'] == 'Classic']
num_classics17 = len(pd.unique(classic17['ID']))
print 'Number of classics: ', num_classics17

lions_health17 = len(pd.unique(classic17[classic17['Host'] == 'Lh Delegates Entrance']['ID']))
print 'Number of classics attending a Lions health event 2017: ', lions_health17/float(num_classics17)
lions_entertainment17 = len(pd.unique(classic17[classic17['Host'] == 'Le Delegates Entrance']['ID']))
print 'Number of classics attending a Lions entertainment event 2017: ', lions_entertainment17/float(num_classics17)
lions_innovation17 = len(pd.unique(classic17[classic17['Host'] == 'Li Delegates Entrance']['ID']))
print 'Number of classics attending a Lions innovation event 2017: ', lions_innovation17/float(num_classics17)

classic16 = CL_16[CL_16['PassGroup'] == 'Classic']
num_classics16 = len(pd.unique(classic16['ID']))
print 'Number of classics: ', num_classics16

lions_health16 = len(pd.unique(classic16[classic16['Host'] == 'Lh Delegates Entrance']['ID']))
print 'Number of classics attending a Lions health event 2016: ', lions_health16/float(num_classics16)
lions_entertainment16 = len(pd.unique(classic16[classic16['Host'] == 'Le Delegates Entrance']['ID']))
print 'Number of classics attending a Lions entertainment event 2016: ', lions_entertainment16/float(num_classics16)
lions_innovation16 = len(pd.unique(classic16[classic16['Host'] == 'Li Delegates Entrance']['ID']))
print 'Number of classics attending a Lions innovation event 2016: ', lions_innovation16/float(num_classics16)

''' New vs Returning '''
new_17 = len(pd.unique(CL_17_Paid[CL_17_Paid['BusinessType'] == 'New']['ID']))
return_17 = len(pd.unique(CL_17_Paid[CL_17_Paid['BusinessType'] == 'Returning']['ID']))
win_17 = len(pd.unique(CL_17_Paid[CL_17_Paid['BusinessType'] == 'Win Back']['ID']))
reg_17 = len(pd.unique(CL_17_Paid[CL_17_Paid['BusinessType'] == 'Regular']['ID']))
print 'Number of new, returning, win back and regs delegates 2017: ', new_17, return_17, win_17, reg_17, ' Out of', 7927

new_16 = len(pd.unique(CL_16_Paid[CL_16_Paid['BusinessType'] == 'New']['ID']))
return_16 = len(pd.unique(CL_16_Paid[CL_16_Paid['BusinessType'] == 'Returning']['ID']))
win_16 = len(pd.unique(CL_16_Paid[CL_16_Paid['BusinessType'] == 'Win Back']['ID']))
reg_16 = len(pd.unique(CL_16_Paid[CL_16_Paid['BusinessType'] == 'Regular']['ID']))
print 'Number of new, returning, win back and reg delegates 2016: ', new_16, return_16, win_16, reg_16, ' Out of', 7792

''' Mean scans of new vs. returning '''
new_17_id = CL_17_Paid[CL_17_Paid['BusinessType'] == 'New']
print 'Mean scans per person per day of new dels 2017: ', np.mean(new_17_id.groupby('ID').size().reset_index(name='scans')['scans'])/8.
return_17_id = CL_17_Paid[CL_17_Paid['BusinessType'] == 'Returning']
print 'Mean scans per person per day of returning dels 2017: ', np.mean(return_17_id.groupby('ID').size().reset_index(name='scans')['scans'])/8.

new_16_id = CL_16_Paid[CL_16_Paid['BusinessType'] == 'New']
print 'Mean scans per person per day of new dels 2016: ', np.mean(new_16_id.groupby('ID').size().reset_index(name='scans')['scans'])/8.
return_16_id = CL_16_Paid[CL_16_Paid['BusinessType'] == 'Returning']
print 'Mean scans per person per day of returning dels 2016: ', np.mean(return_16_id.groupby('ID').size().reset_index(name='scans')['scans'])/8.


''' Hotel Access: 2017 only '''

''' 2017 paying dels accessing hotels '''
print 'Number of paying and nonpaying delegates accessing hotels: ', len(pd.unique(CL_17[CL_17['Description'] == 'Hotel Access']['ID']))
print 'Number of paying delegates accessing hotels: ', len(pd.unique(CL_17_Paid[CL_17_Paid['Description'] == 'Hotel Access']['ID']))
print 'Number of scans into the Carlton (currently the only hotel) over Cannes: ', len(CL17_scans[CL17_scans['SessionCode'] == 'Carlton'])

print len(CL17_hotel), ' Many people signed up for hotel access'
unique_hotel = CL17_hotel.drop_duplicates(subset=['First Name', 'Last Name', 'EmailAddress'])
print len(unique_hotel), ' Many unique people are in the hotel access data'




names = CL17_hotel[['First Name', 'Last Name', 'EmailAddress']].drop_duplicates()

print names.merge(CL17_dels, left_on=['First Name', 'Last Name', 'EmailAddress'], right_on=['Name', 'Surname', 'Email'],
                  how='inner').drop_duplicates(subset=['First Name', 'Last Name', 'EmailAddress'])




sys.exit()


names = CL17_hotel[['First Name', 'Last Name', 'EmailAddress']].drop_duplicates()
dels_HA = len(pd.unique(names.merge(CL17_dels, left_on=['First Name', 'Last Name', 'EmailAddress'], right_on=['Name', 'Surname', 'Email'], how='inner')['ID']))
print 'Number of paying and non paying dels with hotel access: ', dels_HA
print 'Number of people signed up for HA without a pass = ', len(names) - dels_HA

dels_pay_scanned_HA = len(pd.unique(names.merge(CL_17_Paid, left_on=['First Name', 'Last Name', 'EmailAddress'], right_on=['Name', 'Surname', 'Email'], how='inner')['ID']))
print 'Number of paying, scanned dels with hotel access: ', dels_pay_scanned_HA


''' Fringe Analysis '''
print CL_17_Paid.groupby('Host').size().reset_index(name='scans')
c = CL_17[CL_17['Description'] == 'Lions Fringe']
d = CL_16[CL_16['Description'] == 'Lions Fringe']

e = CL_17.groupby('PassGroup').size().reset_index(name='scans')
f = c.groupby('PassGroup').size().reset_index(name='scans')
g = CL_16.groupby('PassGroup').size().reset_index(name='scans')
h = d.groupby('PassGroup').size().reset_index(name='scans')
e['scanspp'] = e['scans']/f['scans']
print e
g['scans'] = g['scans']/h['scans']
print g
print c
print c.groupby('BusinessType').size().reset_index(name='scans')
print d.groupby('BusinessType').size().reset_index(name='scans')




