"""Re-implementation of the core calendar library for both Persian and Gregorian styles"""

import enum
import datetime
from itertools import repeat


# Number of days in each month of a common Gregorian year and of a Jalali year.
# These drive the day-count conversion between the two calendars below:
_G_DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
_J_DAYS_IN_MONTH = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]


def _is_gregorian_leap(year):
    """Return whether the given Gregorian year is a leap year"""
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


def gregorian_to_persian(gy, gm, gd):
    """Convert a Gregorian date to a Persian (Jalali) date tuple (year, month, day).

    This is an independent implementation of the well-known FarsiWeb day-count
    algorithm, kept in-house to avoid the jdatetime/jalali-core dependency.
    """
    g_year = gy - 1600
    g_month = gm - 1

    days = (365 * g_year + (g_year + 3) // 4 - (g_year + 99) // 100
            + (g_year + 399) // 400 + gd - 1 - 79)
    for i in range(g_month):
        days += _G_DAYS_IN_MONTH[i]
    if g_month > 1 and _is_gregorian_leap(gy):
        days += 1

    j_np = days // 12053
    days %= 12053
    jy = 979 + 33 * j_np + 4 * (days // 1461)
    days %= 1461
    if days >= 366:
        days -= 1
        jy += days // 365
        days %= 365

    jm = 0
    while jm < 11 and days >= _J_DAYS_IN_MONTH[jm]:
        days -= _J_DAYS_IN_MONTH[jm]
        jm += 1
    return jy, jm + 1, days + 1


def persian_to_gregorian(jy, jm, jd):
    """Convert a Persian (Jalali) date to a Gregorian date tuple (year, month, day)."""
    j_year = jy - 979

    days = (365 * j_year + (j_year // 33) * 8 + (j_year % 33 + 3) // 4
            + jd - 1 + 79)
    for i in range(jm - 1):
        days += _J_DAYS_IN_MONTH[i]

    gy = 1600 + 400 * (days // 146097)
    days %= 146097

    leap = True
    if days >= 36525:
        days -= 1
        gy += 100 * (days // 36524)
        days %= 36524
        if days >= 365:
            days += 1
        else:
            leap = False

    gy += 4 * (days // 1461)
    days %= 1461
    if days >= 366:
        leap = False
        days -= 1
        gy += days // 365
        days %= 365

    gm = 0
    while True:
        month_len = _G_DAYS_IN_MONTH[gm] + (1 if (gm == 1 and leap) else 0)
        if days < month_len:
            break
        days -= month_len
        gm += 1
    return gy, gm + 1, days + 1


class PersianDate:
    """Minimal Persian (Jalali) date, mirroring the subset of jdatetime.date we use.

    Only the operations calcure relies on are implemented: construction, access to
    year/month/day, conversion to and from Gregorian, weekday (Saturday = 0, as in
    jdatetime), leap-year test, timedelta arithmetic, and equality.
    """

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def fromgregorian(cls, *, day, month, year):
        """Build a PersianDate from Gregorian year/month/day"""
        return cls(*gregorian_to_persian(year, month, day))

    @classmethod
    def today(cls):
        """Return today's date in the Persian calendar"""
        today = datetime.date.today()
        return cls.fromgregorian(day=today.day, month=today.month, year=today.year)

    def togregorian(self):
        """Return the equivalent Gregorian datetime.date"""
        return datetime.date(*persian_to_gregorian(self.year, self.month, self.day))

    def weekday(self):
        """Return the weekday with Saturday = 0, matching jdatetime's convention"""
        return (self.togregorian().weekday() + 2) % 7

    def isleap(self):
        """Return whether this date's Persian year is a leap year"""
        start = datetime.date(*persian_to_gregorian(self.year, 1, 1)).toordinal()
        next_start = datetime.date(*persian_to_gregorian(self.year + 1, 1, 1)).toordinal()
        return (next_start - start) == 366

    def __add__(self, other):
        if isinstance(other, datetime.timedelta):
            g = self.togregorian() + other
            return PersianDate.fromgregorian(day=g.day, month=g.month, year=g.year)
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, datetime.timedelta):
            g = self.togregorian() - other
            return PersianDate.fromgregorian(day=g.day, month=g.month, year=g.year)
        if isinstance(other, PersianDate):
            return self.togregorian() - other.togregorian()
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, PersianDate):
            return (self.year, self.month, self.day) == (other.year, other.month, other.day)
        return NotImplemented

    def __hash__(self):
        return hash((self.year, self.month, self.day))

    def __repr__(self):
        return f"PersianDate({self.year}, {self.month}, {self.day})"


def convert_to_persian_date(year, month, day):
    """Convert date from Gregorian to Persian calendar"""
    return gregorian_to_persian(year, month, day)


def convert_to_gregorian_date(year, month, day):
    """Convert date from Persian to Gregorian calendar"""
    return persian_to_gregorian(year, month, day)


class Calendar:
    """
    Calendar class, but in contrast to native calendar library, here
    the type of the calendar (Gregorian or Persian) is passed as argument
    and all methods change accordingly.
    """

    def __init__(self, firstweekday, use_persian_calendar):
        self.firstweekday = firstweekday
        self.use_persian_calendar = use_persian_calendar

    def last_day(self, year, month):
        """Return the number of the last day of the month"""
        if self.use_persian_calendar:
            isleap = PersianDate(year, 1, 1).isleap()
            mdays = [0, 31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
            ndays = mdays[month] + (month == 12 and isleap)
            return ndays
        else:
            isleap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
            mdays = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            ndays = mdays[month] + (month == 2 and isleap)
            return ndays

    def first_day(self, year, month):
        """Return weekday of the first day of the month"""
        if self.use_persian_calendar:
            return PersianDate(year, month, 1).weekday()
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

    def week_number(self, year, month, day):
        """Return the week number for a given date"""
        if self.use_persian_calendar:
            date = PersianDate(year, month, day)
            # For Persian calendar, calculate week number based on year start
            year_start = PersianDate(year, 1, 1)
            days_since_start = (date - year_start).days
            week_num = (days_since_start // 7) + 1
            return week_num
        else:
            date = datetime.date(year, month, day)
            # ISO week number (standard week numbering)
            return date.isocalendar()[1]

    def month_week_numbers(self, year, month):
        """Return list of week numbers for each week in the month"""
        weeks = self.monthdayscalendar(year, month)
        week_numbers = []
        for week in weeks:
            # Find the first non-zero day in the week to get the week number
            for day in week:
                if day != 0:
                    week_numbers.append(self.week_number(year, month, day))
                    break
            else:
                # If all days are 0 (shouldn't happen), use previous week + 1
                week_numbers.append(week_numbers[-1] + 1 if week_numbers else 1)
        return week_numbers
