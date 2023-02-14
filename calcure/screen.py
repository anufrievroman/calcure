"""Module that controls the overall state of the program screen"""

import datetime
import jdatetime

from calcure.data import Events, AppState, CalState
from calcure.calendars import Calendar


class Screen:
    """Main state of the program that describes what is displayed and how"""
    def __init__(self, stdscr, cf):
        self.stdscr = stdscr
        self.privacy = cf.PRIVACY_MODE
        self.state = cf.DEFAULT_VIEW
        self.calendar_state = CalState.DAILY if cf.DEFAULT_CALENDAR_VIEW == "daily" else CalState.MONTHLY
        self.use_persian_calendar = cf.USE_PERSIAN_CALENDAR
        self.split = cf.SPLIT_SCREEN
        self.right_pane_percentage = cf.RIGHT_PANE_PERCENTAGE
        self.active_pane = False
        self.selection_mode = False
        self.refresh_now = False
        self.key = None
        self.day = self.today.day
        self.month = self.today.month
        self.year = self.today.year

    @property
    def y_max(self):
        """Get maximum size of the screen"""
        y_max, _ = self.stdscr.getmaxyx()
        return y_max

    @property
    def journal_pane_width(self):
        """Calculate the width of the right pane if the value is adequate"""
        _, x_max = self.stdscr.getmaxyx()
        if 5 < self.right_pane_percentage < 95:
            return int(x_max//(100/self.right_pane_percentage))
        return x_max//4

    @property
    def x_max(self):
        """Calculate the right boundary of the screen"""
        _, x_max = self.stdscr.getmaxyx()
        if x_max < 40:
            self.split = False
        if self.split and self.state != AppState.JOURNAL:
            return x_max - self.journal_pane_width
        return x_max

    @property
    def x_min(self):
        """Calculate the left boundary of the screen"""
        _, x_max = self.stdscr.getmaxyx()
        if x_max < self.journal_pane_width:
            self.split = False
        if self.split and self.state == AppState.JOURNAL:
            return x_max - self.journal_pane_width + 2
        return 0

    @property
    def date(self) -> datetime:
        """Return displayed date in datetime format"""
        if self.use_persian_calendar:
            return jdatetime.date(self.year, self.month, self.day)
        else:
            return datetime.date(self.year, self.month, self.day)

    @property
    def today(self) -> datetime:
        """Return todays's date in datetime format"""
        if self.use_persian_calendar:
            return jdatetime.date.today()
        else:
            return datetime.date.today()

    def next_month(self):
        """Switches to the next month"""
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year += 1

    def previous_month(self):
        """Switches to the previous month"""
        if self.month > 1:
            self.month -= 1
        else:
            self.month = 12
            self.year -= 1

    def next_day(self):
        """Switch to the next day"""
        days_in_this_month = Calendar(0, self.use_persian_calendar).last_day(self.year, self.month)
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
        """Switch to the previous day"""
        if self.day > 1:
            self.day -= 1
        else:
            if self.month > 1:
                self.month -= 1
            else:
                self.month = 12
                self.year -= 1
            self.day = Calendar(0, self.use_persian_calendar).last_day(self.year, self.month)

    def reset_to_today(self):
        """Reset the day, month, and year to the current date"""
        self.month = self.today.month
        self.year = self.today.year
        self.day = self.today.day

    def is_valid_day(self, number) -> bool:
        """Check if input corresponds to a date in this month"""
        if number is None:
            return False
        return 0 < number <= Calendar(0, self.use_persian_calendar).last_day(self.year, self.month)


    def is_valid_date(self, year, month, day) -> bool:
        """Check if a date corresponds to any actually existing date"""
        if None in [year, month, day]:
            return False
        if 1 <= month <= 12:
            return 0 < day <= Calendar(0, self.use_persian_calendar).last_day(year, month)
        return False
