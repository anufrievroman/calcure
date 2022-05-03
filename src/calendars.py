"""Re-implementation of the core calendar library for both Persian and Gregorian styles"""

import enum
import datetime
from itertools import repeat

import jdatetime


class CalType(enum.Enum):
    """Possible types of the calendar"""
    GREGORIAN = 1
    PERSIAN = 2


class Calendar:
    """Base calendar class. In contrast with core calendar library, here
    the type of the calendar is passed as argument"""

    def __init__(self, firstweekday, calendar_type):
        self.firstweekday = firstweekday
        self.calendar_type = calendar_type

    def last_day(self, year, month):
        """Return the last day of the month"""
        if self.calendar_type == CalType.GREGORIAN:
            return Calendar.monthrange_gregorian(year, month)[1]
        else:
            return Calendar.monthrange_persian(year, month)[1]

    @staticmethod
    def monthrange_persian(year, month):
        """Return weekday and number of days (28-31) if Persian calendar"""
        isleap = jdatetime.date(year, 1, 1).isleap()
        day1 = jdatetime.date(year, month, 1).weekday()
        mdays = [0, 31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
        ndays = mdays[month] + (month == 2 and isleap)
        return day1, ndays

    @staticmethod
    def monthrange_gregorian(year, month):
        """Return weekday and number of days (28-31) if Gregorian calendar"""
        isleap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
        day1 = datetime.date(year, month, 1).weekday()
        mdays = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        ndays = mdays[month] + (month == 2 and isleap)
        return day1, ndays

    def itermonthdays(self, year, month):
        """Iterate through the days of the month"""
        if self.calendar_type == CalType.GREGORIAN:
            day1, ndays = Calendar.monthrange_gregorian(year, month)
        else:
            day1, ndays = Calendar.monthrange_persian(year, month)
        days_before = (day1 - self.firstweekday) % 7
        yield from repeat(0, days_before)
        yield from range(1, ndays + 1)
        days_after = (self.firstweekday - day1 - ndays) % 7
        yield from repeat(0, days_after)

    def monthdayscalendar(self, year, month):
        """Return a matrix representing a month's calendar"""
        days = list(self.itermonthdays(year, month))
        return [days[i:i + 7] for i in range(0, len(days), 7)]
