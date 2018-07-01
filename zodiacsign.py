from datetime import datetime
from datetime import timedelta

class ZodiacSign:

    sign_dates = (
        ((21, 3), (19, 4)),  # Aries
        ((20, 4), (20, 5)),
        ((21, 5), (20, 6)),
        ((21, 6), (22, 7)),
        ((23, 7), (22, 8)),
        ((23, 8), (22, 9)),
        ((23, 9), (22, 10)),
        ((23, 10), (21, 11)),
        ((22, 11), (21, 12)),
        ((22, 12), (19, 1)),
        ((20, 1), (18, 2)),
        ((19, 2), (20, 3)),  # Pisces
    )

    en_dict = (
        (0, "Aries"),
        (1, "Taurus"),
        (2, "Gemini"),
        (3, "Cancer"),
        (4, "Leo"),
        (5, "Virgo"),
        (6, "Libra"),
        (7, "Scorpio"),
        (8, "Sagittarius"),
        (9, "Capricorn"),
        (10, "Aquarius"),
        (11, "Pisces"),
    )

    def __init__(self, name, birth_date: datetime):
        self.name = name
        self.birth_date = birth_date

    @staticmethod
    def get_zodiac_sign(d, month=None):
        # params
        if month is None:
            month = int(d.month)
            day = int(d.day)
        else:
            day = int(d)
            month = int(month)
        # calculate
        for index, sign in enumerate(ZodiacSign.sign_dates):
            if (month == sign[0][1] and day >= sign[0][0]) or (month == sign[1][1] and day <= sign[1][0]):
                return index
        return ''

    @staticmethod
    def sign_from_fecundation(fecundation: datetime):
        birth_date = fecundation + timedelta(days=266)  # 266 days avg 38 weeks birth date
        signIndex = ZodiacSign.get_zodiac_sign(birth_date)
        return ZodiacSign(name= ZodiacSign.en_dict[signIndex][1], birth_date= birth_date)
