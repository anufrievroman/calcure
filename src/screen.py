"""Module that controls the overal state of the program"""

import datetime
from data import Events, State


class Screen:
    """Main state of the program that describes what is displayed and how"""
    def __init__(self, stdscr, privacy, state, split, right_pane_percentage):
        self.stdscr = stdscr
        self.day = datetime.date.today().day
        self.month = datetime.date.today().month
        self.year = datetime.date.today().year
        self.privacy = privacy
        self.state = state
        self.right_pane_percentage = right_pane_percentage
        self.split = split
        self.active_pane = False
        self.selection_mode = False
        self.refresh_now = False
        self.key = None
        self.y_max, _ = self.stdscr.getmaxyx()

    @property
    def journal_pane_width(self):
        """Calculate the widht of the right pane"""
        _, x_max = self.stdscr.getmaxyx()
        if 0 < self.right_pane_percentage < 99:
            return int(x_max//(100/self.right_pane_percentage))
        return x_max//4

    @property
    def x_max(self):
        """Calculate the right boundary of the screen"""
        _, x_max = self.stdscr.getmaxyx()
        if x_max < 40:
            self.split = False
        if self.split and self.state != State.JOURNAL:
            return x_max - self.journal_pane_width
        return x_max

    @property
    def x_min(self):
        """Calculate the left boundary of the screen"""
        _, x_max = self.stdscr.getmaxyx()
        if x_max < self.journal_pane_width:
            self.split = False
        if self.split and self.state == State.JOURNAL:
            return x_max - self.journal_pane_width + 2
        return 0

    @property
    def date(self) -> datetime:
        """Return displayed date in datetime format"""
        return datetime.date(self.year, self.month, self.day)

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
        """Switch to the previous day"""
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
        """Reset the day, month, and year to the current date"""
        today = datetime.date.today()
        self.month = today.month
        self.year = today.year
        self.day = int(today.day)

    def is_valid_day(self, number) -> bool:
        """Check if input corresponds to a date this month"""
        if number is None:
            return False
        return 0 < number <= Events.monthrange_gregorian(self.year, self.month)
