import sys

import pandas as pd
import numpy as np
from Code.config import get_path
from collections import Counter

pd.set_option('display.width', 500)


def main():

    attendee_list = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/AttendeeList.csv').drop(['Phone',
                                                                                                   'External Link',
                                                                                                   'Date Created',
                                                                                                   'Registration Reference'],
                                                                                                  axis=1))
    group_map = {'Wristband to collect': 1, None: 0}
    attendee_list['Group'] = attendee_list['Group'].replace(group_map)
    attendee_list.columns = ['First Name', 'Last Name', 'Company', 'DelegateType', 'Wristband', 'Country', 'Email Address', 'ClientRef', 'FirstSeen', 'Job']
    attendee_list['ID'] = attendee_list['First Name'] + ' ' + attendee_list['Last Name'] + ' ' + attendee_list['Email Address']
    for col in ['Company', 'DelegateType', 'Country', 'Job']:
        attendee_list[col] = attendee_list[col].str.title()
    a = attendee_list[~attendee_list['ClientRef'].isin(['New pass - Sophie W', 'OPP555928'])]
    a = a.dropna(subset=['ClientRef'])

    preprints = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/preprints.csv').dropna(subset=['clientReference']).drop(['datecreated', 'firstname',
                                                                                           'lastname', 'company', 'categoryName', 'Unnamed: 6'], axis=1))
    preprints['preprint'] = np.ones((len(preprints)))
    preprints.columns=['ClientRef', 'PrePrint']
    b = preprints

    arrivals = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/arrivals.csv').drop(['idAttendee', 'firstname',
                                                                                         'lastname', 'company',
                                                                                         'categoryname'], axis=1).drop_duplicates())

    sessions = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/sessions.csv').drop(
        ['dateCreated', 'registrationReference.1', 'company', 'categoryName',
         'groupName', 'country', 'jobTitle', 'registrationReference', 'firstName', 'lastName', 'email'], axis=1))
    sessions.columns = ['ScanIn', 'ScanOut', 'Seminar', 'Start', 'Finish', 'Location', 'ClientRef']
    for col in ['Seminar', 'Location']:
        sessions[col] = sessions[col].str.title()
    sessions = sessions.drop_duplicates().reset_index()

    sessions = sessions.dropna(subset=['ClientRef'])

    revenue = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/revenue.csv').drop(['Event Member ID', 'Asset Record Type',
                                                                                       'Product Line Item', 'Event: TRG Event Name',
                                                                                       'Contact Job Title', 'Order Value Currency'], axis=1)).reset_index(drop=True)
    revenue['ID'] = revenue['Contact: Full Name']+ ' ' +revenue['Contact Email']
    revenue = pd.DataFrame(revenue.drop(['Contact: Full Name', 'Contact Email'], axis=1))


    # Keep all revenue (with and without client refs)
    d = attendee_list.merge(sessions, on='ClientRef', how='inner')
    e = pd.DataFrame(revenue.merge(d, on='ID', how='left').drop(['First Name', 'Last Name', 'Email Address', 'index'], axis=1)).reset_index(drop=True)
    e.columns=['Revenue', 'ID', 'Company', 'Delegate Type', 'Wristband', 'Country', 'Client Ref', 'First Seen', 'Job Title', 'ScanIn', 'ScanOut', 'Seminar', 'Start', 'Finish', 'Location']

    e.to_csv('/Users/JackShipway/Desktop/data.csv', index=None, encoding='utf-8-sig')









if __name__ == '__main__':
    main()