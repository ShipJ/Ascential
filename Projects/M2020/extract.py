import sys
import numpy as np
import pandas as pd
from Code.config import get_path

pd.set_option('display.width', 320)


def main():


    # revenue = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/revenue.csv'))
    # attendance = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/attendance.csv'))
    # attendees = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/attendees.csv'))
    # seminars = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/seminars.csv'))
    # country_banding = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/country_banding.csv'))
    # job_banding = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/job_banding.csv'))
    #
    # a = attendance.merge(attendees, on='Reg Ref', how='inner')
    # b = a.merge(seminars, on='Seminar', how='inner')
    # c = b.merge(country_banding, on='Country', how='left').merge(job_banding, on='Job', how='left')
    #
    # print c
    #
    #
    #
    # sys.exit()





if __name__ == '__main__':
    main()