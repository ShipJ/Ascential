import pandas as pd
import numpy as np
import sys


def clean(df):
    """
    Takes a dataframe of salesforce data and maps values to a more usable format, returning a clean data set.
    
    :param df: pandas DataFrame containing raw data
    :return: df: cleaned data set - i.e. mapped to correct values
    """

    # Replace empty and NaN's with None
    empty_nan_map = {np.nan: None, '': None}
    df.replace(empty_nan_map, inplace=True)

    # Drop unwanted headers
    df = pd.DataFrame(df.drop(['RegisteredCompany', 'OpportunityId', 'CreditStatus', 'CompanyTelephone', 'ShowSector',
                               'BillingPostalCode', 'BillingState', 'VATNumber', 'VATNumberValidationStatus', 'Website',
                               'CurrencyIsoCode', 'IsWon', 'InvoiceFrequency', 'LeadChannel', 'LeadSource',
                               'ProductDescription', 'ReasonLost', 'OtherReasonsLost', 'OtherCustomerObjectives',
                               'Probability', 'GrossArea', 'NetChargeableArea', 'ProductCategory'], axis=1))

    # Exhibitions: map 'Spring Fair International 2017' -> Spring17
    fairs = []
    years = []
    for i in range(len(df)):
        fairs.append(df['Exhibition'][i].split(' ', 1)[0])
        years.append(df['Exhibition'][i].split(' ')[3][2:])
    df['Exhibition'] = fairs
    df['Year'] = years

    # Company Sectors: strip redundant values, repeat entries, mistake entries, combine 3 cols to 1 col
    words, results = [], []
    stopwords = ['and', '&', 'the']
    for i in range(len(df)):
        query1, query2, query3 = df['CompanySector'][i], df['CompanySector2'][i], df['CompanySector3'][i]
        queries = list()
        if query1 != None:
            queries += list(query1.split())
            if query2 != None:
                queries += list(query2.split())
                if query3!= None:
                    queries += list(query3.split())
        else:
            queries = None
        if queries == None:
            result = None
        else:
            result = list([word for word in queries if word.lower() not in stopwords])
            mapping = [("Children\xe2\x80\x99s", 'Children\'s Gifts'), ('Gifts,', ''), ('Children?s', 'Children\'s Gifts'),
                       ('Fashion,', 'Fashion'), ('Jewellery,', 'Jewellery'), ('Volume,', 'Volume'), ('Kitchen,', 'Kitchen'),
                       ('Multiple, /', ''), ('Department', 'Department Store'), ('Stores', ''), ('retailer', 'Retail'),
                       ('/', ''), ('Multiple', ''), (' ', '')]
            for k, v in mapping:
                result = [i.replace(k, v) for i in result]
            if '' in result: result.remove('')
            result = pd.unique(result)

        results.append(result)
    df = pd.DataFrame(df.drop(['CompanySector', 'CompanySector2', 'CompanySector3'], axis=1))
    df['CompanySectors'] = results


    # Replace unknown with None
    exhibitorTypeMap = {'Unknown': None}
    df['ExhibitorType'].replace(exhibitorTypeMap, inplace=True)

    # Replace the multitude of Hall labels with the following map
    hallMap = {'': None, '1': 1, '1.1': 1, '10,11,12': [10, 11, 12], '10-Dec': None, '11': 11, '19-20': [19, 20],
               '2': 2, '20': 20, '3': 3, '4': 4, '5': 5, '6': 6, '9': 9, 'Autumn Fair Intl 2014 Hall 3': 3,
               'Autumn Fair Intl 2015 Hall 1': 1, 'Autumn Fair Intl 2015 Hall 4': 4,
               'Autumn Fair Intl 2015 Hall 5': 5, 'Ground Level': 'n/a', 'Hall 01': 1, 'Hall 02': 2,
               'Hall 03': 3, 'Hall 04': 4, 'Hall 05': 5, 'Hall 1': 1, 'Hall 1 (H1)': 1,
               'Hall 10,Hall 11,Hall 12': [10, 11, 12], 'Hall 10,Hall 11,Hall 12 (H10-12)': [10, 11, 12],
               'Hall 10-12': [10, 11, 12], 'Hall 17,Hall 18 (H17-18)': [17, 18], 'Hall 17-19': [17, 18, 19],
               'Hall 19,Hall 20': [19, 20], 'Hall 19,Hall 20 (H19-20)': [19, 20], 'Hall 19-20': [19, 20], 'Hall 2': 2,
               'Hall 2 (H2)': 2, 'Hall 3': 3, 'Hall 3 (H3)': 3, 'Hall 3 3A': 3, 'Hall 3-3A': 3, 'Hall 4': 4,
               'Hall 4 (H4)': 4, 'Hall 5': 5, 'Hall 5 (H5)': 5, 'Hall 6 & 7': [6, 7], 'Hall 6, Hall 7 (H6-7)': [6, 7],
               'Hall 6,Hall7': [6, 7], 'Hall 6-7': [6, 7], 'Hall 8': 8, 'Hall 8 (H8)': 8, 'Hall 9': 9,
               'Hall 9 (H9)': 9, 'Hall 9-10': [9, 10], 'Hall N1-19': range(1, 20), 'Halls 10-12': [10, 11, 12],
               'Halls 6 & 7': [6, 7], 'Spring Fair International 2016 - Hall 1': 1,
               'Spring Fair International 2016 - Hall 19&20': [19, 20], 'Spring Fair International 2016 - Hall 3': 3,
               'Spring Fair International 2016 - Hall 4': 4, 'Spring Fair International 2016 - Hall 5': 5,
               'Spring Fair International 2016 - Halls 19&20': [19, 20],
               'Spring Fair International 2016 - Halls 6&7': [6, 7], 'Spring Fair International 2016 Halls 6 & 7': [6, 7]}
    df['Hall'].replace(hallMap, inplace=True)

    cityMap = {'.': '', 'X': '', 'Tbc': '', 'Oxon': 'Oxford', 'Girona 17469': 'Girona', 'Ny': 'New York'}
    df['BillingCity'].replace(cityMap, inplace=True)

    # Some stage names map to the same value
    StageNameMap = {'': None, 'Adv. Commercial Negotiation': 'Commercial Negotiation', 'Close Lost': 'Closed Lost'}
    df['StageName'].replace(StageNameMap, inplace=True)

    # Some dates incorrectly labelled, must be greater than 0
    df = df[df['CreateCloseDateDiff'] >= 0]
    return df
