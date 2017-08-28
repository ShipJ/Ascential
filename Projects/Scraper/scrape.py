import re
import urllib2
import pandas as pd
import sys
from bs4 import BeautifulSoup

pd.set_option('display.width', 320)

website = 'https://europe.money2020.com/session/'

themes = ['Entrepreneurship and Investing', 'POS & Open Platforms', 'Next Gen Retail & Commerce', 'New Market Research & Commercial Models',
          'Bank (R)evolution', 'Perspectives From Fintech"s Leaders', 'Data & Algorithm-Based Innovation', 'UX', 'Legal & Regulatory',
          'Mobile Payments & Wallets', 'X-Border Disruption', 'Shared Ledgers', 'Alternative Lending & Finance', 'ID', 'Risk, Security & Fraud',
          'Keynote']

seminar_content = pd.DataFrame()

for line in file('pages', 'r'):
    page = urllib2.urlopen(website + line)
    soup = BeautifulSoup(page, 'html.parser')
    a = soup.text


    b = a.split("Add to calendar", 1)[-1].split('speakers')

    title = re.split("[0-9][0-9]:[0-9][0-9] - [0-9][0-9]:[0-9][0-9]", b[0].split('|')[0])[0].strip()
    content = b[0].split('|')[3].split('Speakers')[0].strip()

    c = b[0].split('Speakers')[1].split('SOCIAL MEDIA')[0].split('CDATA')[0].split(title)

    num_speakers = len(c)-1

    names = []
    job_titles = []
    companies = []
    for k in range(num_speakers):
        d = c[k].strip().split(',')
        name = d[0].strip()
        job_title = d[1].strip()
        company = c[k].strip().split(',')[2].split('\n\n\n\n')[0].strip()
        names.append(name)
        job_titles.append(job_title)
        companies.append(company)

    names = [i.encode('utf-8') for i in names]
    job_titles = [j.encode('utf-8') for j in job_titles]
    companies = [k.encode('utf-8') for k in companies]

    theme = 'Unknown'
    for j in themes:
        if j in content:
            theme = j
            content = content.split(theme)[1].split('<')[0].rstrip()

    row = {'Seminar': title, 'Theme': theme, 'Content': content, 'NumSpeakers': num_speakers, 'SpeakerNames': names, 'SpeakerJobTitles': job_titles, 'SpeakerCompanies': companies}

    seminar_content = seminar_content.append(row, ignore_index=True)



    print 'Title: %s' % title
    print 'Theme: %s' % theme
    print 'Content: %s' % content
    print 'Number of Speakers: %d' % num_speakers
    print 'Speaker Names: %s' % names
    print 'Job Title: %s' % job_titles
    print 'Companies: %s' % companies
    print '\n'

# seminar_content.to_csv('/Users/JackShipway/Desktop/seminar_scrape.csv', encoding='utf-8-sig', index=None)



