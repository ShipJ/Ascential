import numpy as np
import pandas as pd
from Code.config import get_path

pd.set_option('display.width', 320)


def clean_attendee_list(df):
    df = df.drop(['Phone', 'External Link', 'Client Reference', 'Registration Reference', 'Date Created'], axis=1)
    group_map = {'Wristband to collect': 1}
    df['Group'] = df['Group'].replace(group_map)
    df.columns = ['First Name', 'Last Name', 'Company', 'Type', 'Wristband', 'Country',
                  'Email Address', 'First Seen', 'Job Function']
    return df

def clean_attendance(df):
    df.columns=['regRef', 'Enter Time', 'Exit Time', 'First Name', 'Last Name', 'Company', 'Talk Title',
                'Start Time', 'End Time', 'Type', 'Location', 'Group', 'Client Reference', 'Date', 'Email Address',
                'Country', 'regRef2', 'Job Title']
    df = df.drop(['regRef', 'Enter Time', 'Exit Time', 'Company', 'Type', 'Group',
                  'Client Reference', 'Date', 'Country', 'regRef2', 'Job Title'], axis=1)
    return df


def main():

    path = get_path()  # File path to data store

    attendee_list = clean_attendee_list(pd.DataFrame(pd.read_csv(path+'/Raw/AttendeeList.csv')))

    session_attendance = clean_attendance(pd.read_csv(path+'/Raw/SessionAttendance.csv'))

    data = pd.DataFrame(session_attendance.merge(attendee_list, how='inner', on=['First Name', 'Last Name', 'Email Address']))

    data.to_csv(path+'/Cleaned/sessions.csv', index=None)



if __name__ == '__main__':
    main()