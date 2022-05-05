"""Re-implementation of the core calendar library for both Persian and Gregorian styles"""

import enum
import datetime
from itertools import repeat

import jdatetime


class Calendar:
    """
    Calendar class, but in contrast to calendar library, here
    the type of the calendar (Gregorian or Persian) is passed as argument
    and all menthods depend on it
    """

    def __init__(self, firstweekday, use_persian_calendar):
        self.firstweekday = firstweekday
        self.use_persian_calendar = use_persian_calendar

    def last_day(self, year, month):
        """Return the number of the last day of the month"""
        if self.use_persian_calendar:
            isleap = jdatetime.date(year, 1, 1).isleap()
            mdays = [0, 31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
            ndays = mdays[month] + (month == 2 and isleap)
            return ndays
        else:
            isleap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
            mdays = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            ndays = mdays[month] + (month == 2 and isleap)
            return ndays

    def first_day(self, year, month):
        """Return weekday of the first day of the month"""
        if self.use_persian_calendar:
            return jdatetime.date(year, month, 1).weekday()
        return datetime.date(year, month, 1).weekday()

    def itermonthdays(self, year, month):
        """Iterate through the days of the month"""
        first_day = self.first_day(year, month)
        days_before = (first_day - self.firstweekday) % 7
        yield from repeat(0, days_before)
        yield from range(1, self.last_day(year, month) + 1)
        days_after = (self.firstweekday - first_day - self.last_day(year, month)) % 7
        yield from repeat(0, days_after)

    def monthdayscalendar(self, year, month):
        """Return a matrix representing a month's calendar"""
        days = list(self.itermonthdays(year, month))
        return [days[i:i + 7] for i in range(0, len(days), 7)]
