class Tithi:

    def __init__(self, name, daterange):
        self.name = name
        self.daterange = daterange

class Naksatra:

    def __init__(self, name, daterange):
        self.name = name
        self.daterange = daterange

class DateInfo:

    def __init__(self, date, tithis: [Tithi], naksatras: [Naksatra]):
        self.tithis = tithis
        self.naksatras = naksatras
        self.date = date
