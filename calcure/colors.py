"""Module that provides few converter functions"""

import curses
import jdatetime
from enum import Enum, auto


class Color(Enum):
    """Colors read from user config"""
    DAY_NAMES = auto()
    WEEKENDS = auto()
    HINTS = auto()
    TODAY = auto()
    DAYS = auto()
    WEEKEND_NAMES = auto()
    BIRTHDAYS = auto()
    PROMPTS = auto()
    CONFIRMATIONS = auto()
    TITLE = auto()
    TODO = auto()
    DONE = auto()
    IMPORTANT = auto()
    TIMER = auto()
    TIMER_PAUSED = auto()
    HOLIDAYS = auto()
    EVENTS = auto()
    TIME = auto()
    WEATHER = auto()
    UNIMPORTANT = auto()
    CALENDAR_HEADER = auto()
    ACTIVE_PANE = auto()
    SEPARATOR = auto()
    EMPTY = auto()
    CALENDAR_BOARDER = auto()
    DEADLINES = auto()
    ICS_CALENDARS0 = auto()
    ICS_CALENDARS1 = auto()
    ICS_CALENDARS2 = auto()
    ICS_CALENDARS3 = auto()
    ICS_CALENDARS4 = auto()
    ICS_CALENDARS5 = auto()
    ICS_CALENDARS6 = auto()
    ICS_CALENDARS7 = auto()
    ICS_CALENDARS8 = auto()
    ICS_CALENDARS9 = auto()


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

    # Assign color pair for each ics resourse:
    if cf.ICS_EVENT_FILES is None:
        return

    for index in range(len(cf.ICS_EVENT_FILES)):
        if index < len(cf.COLOR_ICS_CALENDARS):
            color = cf.COLOR_ICS_CALENDARS[index] # Take colors from config
        else:
            color = cf.COLOR_ICS_CALENDARS[-1] # Remaining resourses assume the last assigned color
        curses.init_pair(Color.ICS_CALENDARS0.value + index, color, cf.COLOR_BACKGROUND)
