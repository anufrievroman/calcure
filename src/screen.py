import datetime
import enum
import curses

from data import Events, State
from config import cf


class Screen():
    '''Main state of the program that describes what is displayed and how'''
    def __init__(self, stdscr, privacy, state, split):
        self.stdscr = stdscr
        self.day = datetime.date.today().day
        self.month = datetime.date.today().month
        self.year = datetime.date.today().year
        self.privacy = privacy
        self.state = state
        self.split = cf.SPLIT_SCREEN
        self.active_pane = False
        self.selection_mode = False
        self.refresh_now = False
        self.key = None
        self.y_max, _ = self.stdscr.getmaxyx()

    @property
    def journal_pane_width(self):
        _, x_max = self.stdscr.getmaxyx()
        if 0 < cf.RIGHT_PANE_PERCENTAGE < 99:
            return int(x_max//(100/cf.RIGHT_PANE_PERCENTAGE))
        else:
            return x_max//4

    @property
    def x_max(self):
        _, x_max = self.stdscr.getmaxyx()
        if x_max < 40:
            self.split = False
        if self.split and self.state != State.JOURNAL:
            return x_max - self.journal_pane_width
        else:
            return x_max

    @property
    def x_min(self):
        _, x_max = self.stdscr.getmaxyx()
        if x_max < self.journal_pane_width:
            self.split = False
        if self.split and self.state == State.JOURNAL:
            return x_max - self.journal_pane_width + 2
        else:
            return 0

    @property
    def date(self) -> datetime:
        '''Return displayed date in datetime format'''
        return datetime.date(self.year, self.month, self.day)

    def next_month(self):
        '''Switches to the next month'''
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year += 1

    def previous_month(self):
        '''Switches to the previous month'''
        if self.month > 1:
            self.month -= 1
        else:
            self.month = 12
            self.year -= 1

    def next_day(self):
        '''Switch to the next day'''
        days_in_this_month = Events.monthrange_gregorian(self.year, self.month)
        if self.day < days_in_this_month:
            self.day += 1
        else:
            self.day = 1
            if self.month < 12:
                self.month += 1
            else:
                self.month = 1
                self.year += 1

    def previous_day(self):
        '''Switch to the previous day'''
        if self.day > 1:
            self.day -= 1
        else:
            if self.month > 1:
                self.month -= 1
            else:
                self.month = 12
                self.year -= 1
            self.day = Events.monthrange_gregorian(self.year, self.month)

    def reset_to_today(self):
        '''Reset the day, month, and year to the current date'''
        today = datetime.date.today()
        self.month = today.month
        self.year  = today.year
        self.day   = int(today.day)

    def is_valid_day(self, number) -> bool:
        '''Check if input corresponds to a date this month'''
        if number is None:
            return False
        return True if (0 < number <= Events.monthrange_gregorian(self.year, self.month)) else False


############## COLORS ################


def initialize_colors(stdscr):
    '''Define all the color pairs'''
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, cf.COLOR_DAY_NAMES, cf.COLOR_BACKGROUND)
    curses.init_pair(2, cf.COLOR_WEEKENDS, cf.COLOR_BACKGROUND)
    curses.init_pair(3, cf.COLOR_HINTS, cf.COLOR_BACKGROUND)
    curses.init_pair(4, cf.COLOR_TODAY, cf.COLOR_BACKGROUND)
    curses.init_pair(5, cf.COLOR_DAYS, cf.COLOR_BACKGROUND)
    curses.init_pair(6, cf.COLOR_WEEKEND_NAMES, cf.COLOR_BACKGROUND)
    curses.init_pair(7, cf.COLOR_BIRTHDAYS, cf.COLOR_BACKGROUND)
    curses.init_pair(8, cf.COLOR_PROMPTS, cf.COLOR_BACKGROUND)
    curses.init_pair(9, cf.COLOR_CONFIRMATIONS, cf.COLOR_BACKGROUND)
    curses.init_pair(10, cf.COLOR_TITLE, cf.COLOR_BACKGROUND)
    curses.init_pair(11, cf.COLOR_TODO, cf.COLOR_BACKGROUND)
    curses.init_pair(12, cf.COLOR_DONE, cf.COLOR_BACKGROUND)
    curses.init_pair(13, cf.COLOR_IMPORTANT, cf.COLOR_BACKGROUND)
    curses.init_pair(14, cf.COLOR_TIMER, cf.COLOR_BACKGROUND)
    curses.init_pair(15, cf.COLOR_TIMER_PAUSED, cf.COLOR_BACKGROUND)
    curses.init_pair(16, cf.COLOR_HOLIDAYS, cf.COLOR_BACKGROUND)
    curses.init_pair(17, cf.COLOR_EVENTS, cf.COLOR_BACKGROUND)
    curses.init_pair(18, cf.COLOR_TIME, cf.COLOR_BACKGROUND)
    curses.init_pair(19, cf.COLOR_WEATHER, cf.COLOR_BACKGROUND)
    curses.init_pair(20, cf.COLOR_UNIMPORTANT, cf.COLOR_BACKGROUND)
    curses.init_pair(21, cf.COLOR_CALENDAR_HEADER, cf.COLOR_BACKGROUND)
    curses.init_pair(22, cf.COLOR_ACTIVE_PANE, cf.COLOR_BACKGROUND)
    curses.init_pair(23, cf.COLOR_SEPARATOR, cf.COLOR_BACKGROUND)

    if not cf.MINIMAL_WEEKEND_INDICATOR:
        curses.init_pair(2, curses.COLOR_BLACK, cf.COLOR_WEEKENDS)
    if not cf.MINIMAL_TODAY_INDICATOR:
        curses.init_pair(4, curses.COLOR_BLACK, cf.COLOR_TODAY)
    if not cf.MINIMAL_DAYS_INDICATOR:
        curses.init_pair(5, curses.COLOR_BLACK, cf.COLOR_DAYS)
