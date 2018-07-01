import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
from dateinfo import DateInfo
from dateinfo import Naksatra
from dateinfo import Tithi


class DateScrapper:

    def __init__(self, dates: datetime):
        self.dates = dates

    def scrape(self):
        # https://www.prokerala.com/astrology/panchang/2018-june-17.html
        #urls = []
        scrapedResults: [DateInfo] = []
        for dat in self.dates:
            #build url with year-month-day.html
            dateforUrl = dat.strftime('%Y-%B-%d').lower()  # format date in this format 2018-june-18
            hardcoded_locationid = '3688689'  # from http://www.geonames.org/
            url_to_scrape = 'https://www.prokerala.com/astrology/panchang/' + dateforUrl + '.html?loc=' + hardcoded_locationid
            print(url_to_scrape)
            # https://www.prokerala.com/astrology/panchang/2018-june-19.html?loc=3688689

            page = requests.get(url_to_scrape)
            soup = BeautifulSoup(page.text, 'html.parser')

            section_headers = soup.find_all('i', class_='icon-info-circle')
            tithis: List[Tithi] = []
            naksatras: List[Naksatra] = []

            for header in section_headers:
                if header.has_attr('data-id') and header['data-id'] in ['tithi', 'nakshatra']:
                    section_parent = header.parent.parent
                    li_items = section_parent.find_all('li')

                    #iterate li items found in that section usually are the li's containing the needed information
                    for item in li_items:
                        title_item = item.find_all('span', class_='row-title')[0]
                        titlee = next(title_item.stripped_strings) if header['data-id'] == 'tithi' else title_item.string
                        value = item.find_all('span', class_='row-value')[0].string
                        if header['data-id'] == 'tithi':
                            tithis.append(Tithi(titlee.split(' ')[2], value))
                        if header['data-id'] == 'nakshatra':
                            naksatras.append(Naksatra(titlee.strip(), value))

            # find chogadiyas
            scrapedResults.append(DateInfo(dat, tithis, naksatras))
        return scrapedResults
