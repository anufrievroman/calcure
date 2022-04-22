import datetime
import enum

from helpers import monthrange_gregorian


class Screen():
    '''Main state of the program that describes what is displayed and how'''

    def __init__(self, stdscr, privacy, state):
        self.y_max, self.x_max = stdscr.getmaxyx()
        self.day = datetime.date.today().day
        self.month = datetime.date.today().month
        self.year = datetime.date.today().year
        self.privacy = privacy
        self.state = state
        self.selection_mode = False
        self.refresh_now = False
        self.key = None

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
        days_in_this_month = monthrange_gregorian(self.year, self.month)
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
            self.day = monthrange_gregorian(self.year, self.month)

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
        return True if (0 < number <= monthrange_gregorian(self.year, self.month)) else False
