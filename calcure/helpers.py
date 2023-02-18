"""Module that provides few converter functions"""

import curses
import jdatetime

from calcure.data import Color


def convert_to_persian_date(year, month, day):
    """Convert date from Gregorian to Persian calendar"""
    persian_date =  jdatetime.date.fromgregorian(day=day, month=month, year=year)
    day = persian_date.day
    month = persian_date.month
    year = persian_date.year
    return year, month, day


def convert_to_gregorian_date(year, month, day):
    """Convert date from Persian to Gregorian calendar"""
    gregorian_date = jdatetime.date(year, month, day).togregorian()
    day = gregorian_date.day
    month = gregorian_date.month
    year = gregorian_date.year
    return year, month, day


def initialize_colors(cf):
    """Define all the color pairs"""
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(Color.DAY_NAMES.value, cf.COLOR_DAY_NAMES, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.WEEKENDS.value, cf.COLOR_WEEKENDS, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.HINTS.value, cf.COLOR_HINTS, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.TODAY.value, cf.COLOR_TODAY, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.DAYS.value, cf.COLOR_DAYS, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.WEEKEND_NAMES.value, cf.COLOR_WEEKEND_NAMES, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.BIRTHDAYS.value, cf.COLOR_BIRTHDAYS, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.PROMPTS.value, cf.COLOR_PROMPTS, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.CONFIRMATIONS.value, cf.COLOR_CONFIRMATIONS, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.TITLE.value, cf.COLOR_TITLE, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.TODO.value, cf.COLOR_TODO, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.DONE.value, cf.COLOR_DONE, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.IMPORTANT.value, cf.COLOR_IMPORTANT, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.TIMER.value, cf.COLOR_TIMER, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.TIMER_PAUSED.value, cf.COLOR_TIMER_PAUSED, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.HOLIDAYS.value, cf.COLOR_HOLIDAYS, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.EVENTS.value, cf.COLOR_EVENTS, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.TIME.value, cf.COLOR_TIME, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.WEATHER.value, cf.COLOR_WEATHER, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.UNIMPORTANT.value, cf.COLOR_UNIMPORTANT, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.CALENDAR_HEADER.value, cf.COLOR_CALENDAR_HEADER, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.ACTIVE_PANE.value, cf.COLOR_ACTIVE_PANE, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.SEPARATOR.value, cf.COLOR_SEPARATOR, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.EMPTY.value, cf.COLOR_BACKGROUND, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.CALENDAR_BOARDER.value, cf.COLOR_CALENDAR_BOARDER, cf.COLOR_BACKGROUND)
    curses.init_pair(Color.DEADLINES.value, cf.COLOR_DEADLINES, cf.COLOR_BACKGROUND)

    if not cf.MINIMAL_WEEKEND_INDICATOR:
        curses.init_pair(Color.WEEKENDS.value, curses.COLOR_BLACK, cf.COLOR_WEEKENDS)
    if not cf.MINIMAL_TODAY_INDICATOR:
        curses.init_pair(Color.TODAY.value, curses.COLOR_BLACK, cf.COLOR_TODAY)
    if not cf.MINIMAL_DAYS_INDICATOR:
        curses.init_pair(Color.DAYS.value, curses.COLOR_BLACK, cf.COLOR_DAYS)

