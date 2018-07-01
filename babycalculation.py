
"""
1. datainput we receive the nearest menstruation day and then the fertile window, city name
2. dayfiltering filter days from 1 to 16 day after menstruation taking into account fertile window and favorable week days Monday, Wednesday, Thursday and Friday and 1-16 days table, not include 1-4 7 11 and 13 from menstruation day
3. DataBydate with the resulting days we need to call the scrapper to check each of the dates in prokerala.com panchangam for that city and month obtaining tithis and naksatras for each of them
4. tithiValidation thn with that information we validate each date tithis
5. naksatra validation
6.timing of the day validation
7. results
"""

from datescrapper import DateScrapper
from datetime import timedelta
from datetime import datetime
from dateinfo import DateInfo
from zodiacsign import ZodiacSign

class BabyCalculation:
    good_naksatras = ['Rohini', 'Uttara Phalguni', 'Hasta', 'Swati', 'Anuradha', 'Shravana', 'Shatabhisha',
                      'Uttara Bhadrapada', 'Revati']

    good_tithis = ['Panchami', 'Dwitiya', 'Tritiya', 'Saptami', 'Dashami', 'Dwadashi', 'Trayodashi']

    def compute_on(self, menstruation_date: str):
        # TODO: add fertile window
        m_date = datetime.strptime(menstruation_date, '%d-%m-%Y')
        filtered_dates: [datetime] = []
        for index in range(1, 17):
            d = m_date + timedelta(days=index)
            # auspicious days filter from 1-16 from m_day don't include 1-4 7 11 and 13
            # week day filter Monday, Wednesday, Thursday and Friday
            if index not in [1, 2, 3, 4, 7, 11, 13] and d.isoweekday() in [1, 3, 4, 5]:
                # fertile window points ? or filter
                filtered_dates.append(d)

        date_scrapper = DateScrapper(filtered_dates)
        results = date_scrapper.scrape()
        filtered_results = self.filter_by_naksatras(self.filter_by_tithis(results))
        self.print_results(m_date, filtered_results)

    def print_results(self, m_date: datetime, results: [DateInfo]):
        for res in results:
            print('-----------------------------------------------')
            days_diff = (res.date - m_date).days

            print('DATE: ' + res.date.strftime('%B-%d %A').lower() + ' day #' + str(days_diff) + ' and its prediction: ' + self.day_description(days_diff))

            sign = ZodiacSign.sign_from_fecundation(res.date)
            print('Sign: ' + sign.name + ' Birthdate: ' + sign.birth_date.strftime('%B-%d %A').lower())
            print()
            print('NAKSATRAS:')
            for nak in res.naksatras:
                print(nak.name + ': ' + nak.daterange)
            print('TITHIS:')
            for tithi in res.tithis:
                print(tithi.name + ': ' + tithi.daterange)
            print('-----------------------------------------------')

    def day_description(self, day: int):
        days = {5: 'girl',
                6: 'expanding family boy',
                8: 'common boy',
                9: 'beautiful girl',
                10: 'lead boy',
                12: 'fortunate boy',
                14: 'virtuoso',
                15: 'fortunate girl',
                16: 'wise boy'}
        return days[day]

    def filter_by_naksatras(self, dates: [DateInfo]):
        filtered_results = []
        # filtering by naksatras
        for date_info in dates:
            naks = []
            for nak in date_info.naksatras:
                if nak.name in self.good_naksatras and date_info not in filtered_results:
                    filtered_results.append(date_info)
                    naks.append(nak)
            date_info.naksatras = naks

        return filtered_results

    def filter_by_tithis(self, dates: [DateInfo]):
        filtered_results = []

        # filtering by tithis
        for date_info in dates:
            tithis = []
            for tithi in date_info.tithis:
                if tithi.name in self.good_tithis and date_info not in filtered_results:
                    filtered_results.append(date_info)
                    tithis.append(tithi)
            date_info.tithis = tithis

        return filtered_results


baby_calculation = BabyCalculation()
baby_calculation.compute_on('16-06-2018') # aries
# baby_calculation.compute_on('10-07-2018') # aries
# baby_calculation.compute_on('03-08-2018') # taurus
# baby_calculation.compute_on('27-08-2018') # taurus to  geminis
# baby_calculation.compute_on('20-09-2018') # gemisnis to cancer
# baby_calculation.compute_on('14-10-2018') # still cancer , small likehood of leo
# baby_calculation.compute_on('07-11-2018') # leo
