#!/usr/bin/env python

"""This is the main module that contains views and the main logic"""

import curses
import time
import getopt
import sys
import importlib
import logging

from calcure.calendars import Calendar
from calcure.configuration import cf
from calcure.weather import Weather
from calcure.importers import Importer
from calcure.dialogues import clear_line
from calcure.screen import Screen
from calcure.savers import TaskSaverCSV, EventSaverCSV
from calcure.colors import Color, initialize_colors
from calcure.loaders import *
from calcure.data import *
from calcure.controls import *


# Language:
if cf.LANG == "fr":
    from calcure.translations.fr import *
elif cf.LANG == "ru":
    from calcure.translations.ru import *
elif cf.LANG == "it":
    from calcure.translations.it import *
elif cf.LANG == "br":
    from calcure.translations.br import *
elif cf.LANG == "tr":
    from calcure.translations.tr import *
elif cf.LANG == "zh":
    from calcure.translations.zh import *
else:
    from calcure.translations.en import *


__version__ = "2.8.0"


def read_items_from_user_arguments(screen, user_tasks, user_events, task_saver_csv, event_saver_csv):
    """Read --task and --event flags from user arguments to create new tasks or events"""
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "pjhvi", ["folder=", "config=", "task=", "event="])
        for opt, arg in opts:
            if opt in '--task':
                name = arg
                user_tasks.add_item(Task(len(user_tasks.items), name, Status.NORMAL, Timer([]), False))
                screen.state = AppState.EXIT
                task_saver_csv.save()
            if opt in '--event':
                year = int(arg.split("-")[0])
                month = int(arg.split("-")[1])
                day = int(arg.split("-")[2])
                name = arg.split("-")[3]
                event_id = user_events.items[-1].item_id + 1 if not user_events.is_empty() else 1
                user_events.add_item(UserEvent(event_id, year, month, day, name,
                                        1, Frequency.ONCE, Status.NORMAL, False))
                screen.state = AppState.EXIT
                event_saver_csv.save()
    except (getopt.GetoptError, ValueError):
        pass


class View:
    """Parent class of a view that displays things at certain coordinates"""

    def __init__(self, stdscr, y, x):
        self.stdscr = stdscr
        self.y = y
        self.x = x

    def fill_background(self):
        """Fill the screen background with background color"""
        y_max, x_max = self.stdscr.getmaxyx()
        for index in range(y_max - 1):
            self.stdscr.addstr(index, 0, " " * x_max, curses.color_pair(1))

    def display_line(self, y, x, text, color, bold=False, underlined=False):
        """Display the line of text respecting the slyling and available space"""

        # Make sure that we display inside the screen:
        y_max, x_max = self.stdscr.getmaxyx()
        if y >= y_max or x >= x_max:
            return

        # Cut the text if it does not fit the screen:
        text = text[:(x_max - 1 - x)]

        if bold and underlined:
            self.stdscr.addstr(y, x, text, curses.color_pair(color.value) | curses.A_BOLD | curses.A_UNDERLINE)
        elif bold and not underlined:
            self.stdscr.addstr(y, x, text, curses.color_pair(color.value) | curses.A_BOLD)
        elif underlined and not bold:
            self.stdscr.addstr(y, x, text, curses.color_pair(color.value) | curses.A_UNDERLINE)
        else:
            self.stdscr.addstr(y, x, text, curses.color_pair(color.value))


class TaskView(View):
    """Display a single task"""

    def __init__(self, stdscr, y, x, task, screen):
        super().__init__(stdscr, y, x)
        self.task = task
        self.screen = screen
        self.info = f'{self.icon} {self.task.name[self.indent:]}'

    @property
    def color(self):
        """Select the color depending on the status"""
        if self.task.status == Status.DONE:
            return Color.DONE
        if self.task.status == Status.IMPORTANT:
            return Color.IMPORTANT
        if self.task.status == Status.UNIMPORTANT:
            return Color.UNIMPORTANT
        return Color.TODO

    @property
    def icon(self):
        """Select the icon for the task"""
        icon = cf.TODO_ICON
        if cf.DISPLAY_ICONS:
            for keyword in cf.ICONS:
                if keyword in self.task.name.lower():
                    icon = cf.ICONS[keyword]
        if self.task.status == Status.DONE:
            icon = cf.DONE_ICON
        if self.task.status == Status.IMPORTANT:
            icon = cf.IMPORTANT_ICON
        return icon

    @property
    def indent(self):
        """Calculate the left indentation depending on the task level"""
        if self.task.name[:4] == '----':
            return 4
        if self.task.name[:2] == '--':
            return 2
        return 0

    def obfuscate_info(self):
        """Obfuscate the info if privacy mode is on"""
        self.info = f'{cf.TODO_ICON} {cf.PRIVACY_ICON * len(self.task.name[self.indent:])}'

    def render(self):
        """Render a line with an icon, task, deadline, and timer"""
        if self.screen.privacy or self.task.privacy:
            self.obfuscate_info()
        self.display_line(self.y, self.x + self.indent, self.info, self.color)

        deadline_indentation = self.screen.x_min + 2 + len(self.info) + self.indent
        deadline_view = TaskDeadlineView(self.stdscr, self.y, deadline_indentation, self.task)
        deadline_view.render()

        addition_indentation = (deadline_view.has_deadline)*(4 + len(deadline_view.info))
        timer_indentation = deadline_indentation + addition_indentation
        timer_view = TimerView(self.stdscr, self.y, timer_indentation, self.task.timer)
        timer_view.render()


class TaskDeadlineView(View):
    """Display deadline for a task"""

    def __init__(self, stdscr, y, x, task):
        super().__init__(stdscr, y, x)
        self.task = task
        self.color = Color.DEADLINES
        self.icon = cf.DEADLINE_ICON
        self.info = f"{self.task.year}/{self.task.month}/{self.task.day}"
        self.has_deadline = (self.task.year > 0)

    def render(self):
        """Render a line with the deadline date and icon"""
        if self.has_deadline:
            self.display_line(self.y, self.x, f"{self.icon} {self.info}", self.color)


class TimerView(View):
    """Display timer for a task"""

    def __init__(self, stdscr, y, x, timer):
        super().__init__(stdscr, y, x)
        self.timer = timer
        self.color = Color.TIMER if self.timer.is_counting else Color.TIMER_PAUSED

    @property
    def icon(self):
        """Return icon corresponding to timer state"""
        TIMER_RUNS_ICON = "⏵" if cf.DISPLAY_ICONS else "·"
        TIMER_PAUSED_ICON = "⏯︎" if cf.DISPLAY_ICONS else "·"
        return TIMER_RUNS_ICON if self.timer.is_counting else TIMER_PAUSED_ICON

    def render(self):
        """Render a line with a timer and icon"""
        if self.timer.is_started:
            self.display_line(self.y, self.x, f"{self.icon} {self.timer.passed_time}", self.color)


class JournalView(View):
    """Displays a list of all tasks"""

    def __init__(self, stdscr, y, x, user_tasks, user_ics_tasks, screen):
        super().__init__(stdscr, y, x)
        self.user_tasks = user_tasks
        self.user_ics_tasks = user_ics_tasks
        self.screen = screen

    def render(self):
        """Render the list of tasks"""
        if not self.user_tasks.items and not self.user_ics_tasks.items and cf.SHOW_NOTHING_PLANNED:
            self.display_line(self.y, self.x, MSG_TS_NOTHING, Color.UNIMPORTANT)
        for index, task in enumerate(self.user_tasks.items):
            task_view = TaskView(self.stdscr, self.y, self.x, task, self.screen)
            task_view.render()
            if self.screen.selection_mode:
                self.display_line(self.y, self.x, str(index + 1), Color.TODAY)
            self.y += 1

        self.y += 1
        for index, task in enumerate(self.user_ics_tasks.items):
            task_view = TaskView(self.stdscr, self.y, self.x, task, self.screen)
            task_view.render()
            self.y += 1


class EventView(View):
    """Parent class to display events"""

    def __init__(self, stdscr, y, x, event, screen):
        super().__init__(stdscr, y, x)
        self.event = event
        self.screen = screen
        self.info = f"{self.icon} {self.event.name}"

    @property
    def icon(self):
        """Select the right icon for the event"""
        return cf.EVENT_ICON

    @property
    def color(self):
        """Assign color depending on the status or calendar number if it's from .ics file"""
        if self.event.calendar_number is None:
            if self.event.status == Status.IMPORTANT:
                return Color.IMPORTANT
            if self.event.status == Status.UNIMPORTANT:
                return Color.UNIMPORTANT
            return Color.EVENTS
        else:
            for color in Color:
                if color.value == Color.ICS_CALENDARS0.value + self.event.calendar_number:
                    return color
            return Color.EVENTS

    def obfuscate_info(self):
        """Obfuscate the info if privacy mode is on"""
        self.info = f'{cf.EVENT_ICON} {cf.PRIVACY_ICON * len(self.event.name)}'

    def cut_info(self):
        """Cut the name to fit into the cell of the calendar"""
        self.info = self.info[:self.screen.x_max - self.x]
        x_cell = self.screen.x_max // 7
        if (cf.CUT_TITLES or cf.SHOW_CALENDAR_BOARDERS) and self.screen.calendar_state == CalState.MONTHLY:
            self.info = self.info[:(x_cell - 1)]

    def minimize_info(self):
        """Reduce the info to just icon if not much space if available"""
        x_cell = self.screen.x_max // 7
        if x_cell < 7:
            self.info = self.icon

    def fill_remaining_space(self):
        """Fill rest of the line of the calendar with empty characters"""
        x_cell = self.screen.x_max // 7
        if len(self.info) < self.screen.x_max - self.x:
            self.info += " "*(self.screen.x_max - self.x - len(self.info))


class UserEventView(EventView):
    """Display a single user event"""

    @property
    def icon(self):
        """Select the right icon for the event"""
        icon = cf.EVENT_ICON
        if cf.DISPLAY_ICONS:
            for keyword in cf.ICONS:
                if keyword in self.event.name.lower():
                    icon = cf.ICONS[keyword]
        if self.screen.privacy or self.event.privacy:
            icon = cf.PRIVACY_ICON
        return icon

    def render(self):
        """Render this view on the screen"""
        if self.screen.privacy or self.event.privacy:
            self.obfuscate_info()
        self.fill_remaining_space()
        self.cut_info()
        self.minimize_info()
        self.display_line(self.y, self.x, self.info, self.color)


class BirthdayView(EventView):
    """Display a line with birthday icon and name"""

    @property
    def icon(self):
        """Set the icon for birthdays"""
        return cf.BIRTHDAY_ICON

    def render(self):
        """Render this view on the screen"""
        if self.screen.privacy:
            self.obfuscate_info()
        self.fill_remaining_space()
        self.cut_info()
        self.minimize_info()
        self.display_line(self.y, self.x, self.info, Color.BIRTHDAYS)


class HolidayView(EventView):
    """Display a line with holiday icon and occasion"""

    @property
    def icon(self):
        """Set the icon for holiday events"""
        return cf.HOLIDAY_ICON

    def render(self):
        """Render this view on the screen"""
        self.fill_remaining_space()
        self.cut_info()
        self.minimize_info()
        self.display_line(self.y, self.x, self.info, Color.HOLIDAYS)


class DeadlineView(EventView):
    """Display a line with deadline icon and task name"""

    def __init__(self, stdscr, y, x, event, screen):
        super().__init__(stdscr, y, x, event, screen)
        self.info = f"{self.icon} {self.event.name[self.indent:]}"

    @property
    def icon(self):
        """Set the icon for task deadline"""
        return cf.DEADLINE_ICON

    @property
    def indent(self):
        """Calculate the left indentation depending on the task level"""
        if self.event.name[:4] == '----':
            return 4
        if self.event.name[:2] == '--':
            return 2
        return 0

    def render(self):
        """Render this view on the screen"""
        if self.screen.privacy or self.event.privacy:
            self.obfuscate_info()
        self.fill_remaining_space()
        self.cut_info()
        self.minimize_info()
        self.display_line(self.y, self.x, self.info, Color.DEADLINES)


class DailyView(View):
    """Display all events occurring on this days"""

    def __init__(self, stdscr, y, x, repeated_user_events, user_events, user_ics_events, holidays,
                                birthdays, user_tasks, user_ics_tasks, screen, index_offset, is_selection_day=True):
        super().__init__(stdscr, y, x)
        self.repeated_user_events = repeated_user_events.filter_events_that_day(screen)
        self.user_events = user_events.filter_events_that_day(screen)
        self.user_ics_events = user_ics_events.filter_events_that_day(screen)
        self.holidays = holidays.filter_events_that_day(screen)
        self.birthdays = birthdays.filter_events_that_day(screen)
        self.deadlines = user_tasks.filter_events_that_day(screen)
        self.deadlines_ics = user_ics_tasks.filter_events_that_day(screen)
        self.screen = screen
        self.index_offset = index_offset
        self.y_cell = (self.screen.y_max - 3) // 6
        self.x_cell = self.screen.x_max // 7
        self.hidden_events_sign = cf.HIDDEN_ICON + " "*(self.x_cell-len(cf.HIDDEN_ICON))
        self.num_events_this_day = 0
        self.is_selection_day = is_selection_day

    def render(self):
        """Render this view on the screen"""
        index = 0

        # Show user events:
        for event in self.user_events.items:
            if index < self.y_cell - 1:
                user_event_view = UserEventView(self.stdscr, self.y + index, self.x, event, self.screen)
                user_event_view.render()
                if self.screen.selection_mode and self.is_selection_day:
                    self.display_line(self.y + index, self.x, str(index + self.index_offset + 1), Color.TODAY)
            else:
                self.display_line(self.y + self.y_cell - 2, self.x, self.hidden_events_sign, Color.EVENTS)
            index += 1

        # Show repeated user events and events from ics:
        for event_list in [self.repeated_user_events.items, self.user_ics_events.items]:
            for event in event_list:
                if index < self.y_cell - 1:
                    user_event_view = UserEventView(self.stdscr, self.y + index, self.x, event, self.screen)
                    user_event_view.render()
                else:
                    self.display_line(self.y + self.y_cell - 2, self.x, self.hidden_events_sign, Color.EVENTS)
                index += 1

        # Show deadlines for tasks, both from csv and ics files:
        for deadline_list in [self.deadlines.items, self.deadlines_ics.items]:
            for event in deadline_list:
                if index < self.y_cell - 1:
                    deadline_view = DeadlineView(self.stdscr, self.y + index, self.x, event, self.screen)
                    deadline_view.render()
                else:
                    self.display_line(self.y + self.y_cell - 2, self.x, self.hidden_events_sign, Color.DEADLINES)
                index += 1

        # Show holidays:
        if not cf.DISPLAY_HOLIDAYS:
            return
        for event in self.holidays.items:
            if index < self.y_cell - 1:
                holiday_view = HolidayView(self.stdscr, self.y + index, self.x, event, self.screen)
                holiday_view.render()
            else:
                self.display_line(self.y + self.y_cell - 2, self.x, self.hidden_events_sign, Color.HOLIDAYS)
            index += 1

        # Show birthdays:
        if not cf.BIRTHDAYS_FROM_ABOOK:
            return
        for event in self.birthdays.items:
            if index < self.y_cell - 1:
                birthday_view = BirthdayView(self.stdscr, self.y + index, self.x, event, self.screen)
                birthday_view.render()
            else:
                self.display_line(self.y + self.y_cell - 2, self.x, self.hidden_events_sign, Color.BIRTHDAYS)
            index += 1

        self.num_events_this_day = index


class DayNumberView(View):
    """Display the date of the day in month with proper styling"""

    def __init__(self, stdscr, y, x, screen, day, day_in_week, x_cell):
        super().__init__(stdscr, y, x)
        self.screen = screen
        self.day = day
        self.day_in_week = day_in_week
        self.x_cell = x_cell
        self.screen.day = self.day

    def render(self):
        """Render this view on the screen"""
        if self.screen.date == self.screen.today:
            today = f"{self.day}{cf.TODAY_ICON}{' '*(self.x_cell - len(str(self.day)) - 2)}"
            self.display_line(self.y, self.x, today, Color.TODAY, cf.BOLD_TODAY, cf.UNDERLINED_TODAY)
        elif self.day_in_week + 1 in cf.WEEKEND_DAYS:
            weekend = f"{self.day}{' '*(self.x_cell - len(str(self.day)) - 1)}"
            self.display_line(self.y, self.x, weekend, Color.WEEKENDS, cf.BOLD_WEEKENDS, cf.UNDERLINED_WEEKENDS)
        else:
            weekday = f"{self.day}{' '*(self.x_cell - len(str(self.day)) - 1)}"
            self.display_line(self.y, self.x, weekday, Color.DAYS, cf.BOLD_DAYS, cf.UNDERLINED_DAYS)


class TitleView(View):
    """Show the title in the header"""

    def __init__(self, stdscr, y, x, title, screen):
        super().__init__(stdscr, y, x)
        self.title = title
        self.screen = screen

    def render(self):
        """Render this view on the screen"""
        if self.screen.active_pane and self.screen.split:
            self.display_line(0, self.screen.x_min, self.title, Color.ACTIVE_PANE, cf.BOLD_ACTIVE_PANE, cf.UNDERLINED_ACTIVE_PANE)
        else:
            self.display_line(0, self.screen.x_min, self.title, Color.CALENDAR_HEADER, cf.BOLD_TITLE, cf.UNDERLINED_TITLE)


class HeaderView(View):
    """Show the header that includes the weather, time, and title"""

    def __init__(self, stdscr, y, x, title, weather, screen):
        super().__init__(stdscr, y, x)
        self.title = title
        self.weather = weather
        self.screen = screen

    def render(self):
        """Render this view on the screen"""
        _, x_max = self.stdscr.getmaxyx()

        # Show title:
        title_view = TitleView(self.stdscr, 0, self.screen.x_min, self.title, self.screen)
        title_view.render()

        if self.screen.state == AppState.JOURNAL and self.screen.split:
            return

        # Show weather is space allows and it is loaded:
        size_allows = len(self.weather.forcast) < self.screen.x_max - len(self.title)
        if cf.SHOW_WEATHER and size_allows:
            self.display_line(0, self.screen.x_max - len(self.weather.forcast) - 1, self.weather.forcast, Color.WEATHER)

        # Show time:
        time_string = time.strftime("%H:%M", time.localtime())
        size_allows = len(self.weather.forcast) < self.screen.x_max - len(self.title) - len(time_string)
        if cf.SHOW_CURRENT_TIME and size_allows:
            self.display_line(0, (self.screen.x_max // 2 - 2), time_string, Color.TIME)


class FooterView(View):
    """Display the footer with keybinding"""

    def __init__(self, stdscr, y, x, screen):
        super().__init__(stdscr, y, x)
        self.screen = screen

    def render(self):
        """Render this view on the screen"""
        if not cf.SHOW_KEYBINDINGS: return
        clear_line(self.stdscr, self.screen.y_max - 1)
        if self.screen.state == AppState.CALENDAR:
            if self.screen.calendar_state == CalState.MONTHLY:
                hint = CALENDAR_HINT
            else:
                hint = CALENDAR_HINT_D
        elif self.screen.state == AppState.JOURNAL:
            hint = JOURNAL_HINT
        self.display_line(self.screen.y_max - 1, 0, hint, Color.HINTS)


class SeparatorView(View):
    """Display the separator in the split screen"""

    def __init__(self, stdscr, y, x, screen):
        super().__init__(stdscr, y, x)
        self.screen = screen

    def render(self):
        """Render this view on the screen"""
        _, x_max = self.stdscr.getmaxyx()
        x_separator = x_max - self.screen.journal_pane_width
        y_cell = (self.screen.y_max - 3) // 6
        height = 6*y_cell + 2 if cf.SHOW_CALENDAR_BOARDERS else self.screen.y_max
        for row in range(height):
            self.display_line(row, x_separator, cf.SEPARATOR_ICON, Color.SEPARATOR)

        if cf.SHOW_CALENDAR_BOARDERS and self.screen.calendar_state == CalState.MONTHLY:
            for row in range(1, 7):
                self.display_line(row*y_cell + 1, x_separator, "┤", Color.CALENDAR_BOARDER)
            self.display_line(6*y_cell + 1, x_separator, "┘", Color.CALENDAR_BOARDER)


class CalenarBoarderView(View):
    """Display the boarders in the monthly view"""

    def __init__(self, stdscr, y, x, screen):
        super().__init__(stdscr, y, x)
        self.screen = screen

    def render(self):
        """Render this view on the screen"""
        x_cell = self.screen.x_max // 7
        y_cell = (self.screen.y_max - 3) // 6

        # Vertical lines:
        for column in range(1, 7):
            for row in range(y_cell*6):
                self.display_line(row + 2, column*x_cell - 1, "│", Color.CALENDAR_BOARDER)

        # Horizontal lines:
        for row in range(1, 7):
            for column in range(0, self.screen.x_max):
                self.display_line(row*y_cell + 1, column, "─", Color.CALENDAR_BOARDER)

        # Connectors:
        for row in range(1, 6):
            for column in range(1, 7):
                self.display_line(row*y_cell + 1, column*x_cell - 1, "┼", Color.CALENDAR_BOARDER)
        for column in range(1, 7):
            self.display_line(6*y_cell + 1, column*x_cell - 1, "┴", Color.CALENDAR_BOARDER)


class DaysNameView(View):
    """Display day name depending on the screen available and with right style"""

    def __init__(self, stdscr, y, x, screen):
        super().__init__(stdscr, y, x)
        self.screen = screen

    def render(self):
        """Render this view on the screen"""
        num = 2 if self.screen.x_max < 74 else 12
        x_cell = int(self.screen.x_max // 7)

        # Depending on which day we start the week, weekends are shifted:
        for i in range(7):
            shift = cf.START_WEEK_DAY - 1
            day_number = i + shift - 7*((i + shift) > 6)
            day_names = DAYS_PERSIAN if cf.USE_PERSIAN_CALENDAR else DAYS
            name = day_names[day_number][:num]
            x = self.x + i*x_cell
            if day_number + 1 not in cf.WEEKEND_DAYS:
                self.display_line(self.y, x, name, Color.DAY_NAMES, cf.BOLD_DAY_NAMES, cf.UNDERLINED_DAY_NAMES)
            else:
                self.display_line(self.y, x, name, Color.WEEKEND_NAMES, cf.BOLD_WEEKEND_NAMES, cf.UNDERLINED_WEEKEND_NAMES)


##################### SCREENS ##########################


class DailyScreenView(View):
    """Daily view showing events of the day"""

    def __init__(self, stdscr, y, x, weather, user_events, user_ics_events, holidays, birthdays, user_tasks, user_ics_tasks, screen):
        super().__init__(stdscr, y, x)
        self.weather = weather
        self.user_events = user_events
        self.user_ics_events = user_ics_events
        self.holidays = holidays
        self.birthdays = birthdays
        self.user_tasks = user_tasks
        self.user_ics_tasks = user_ics_tasks
        self.screen = screen

    @property
    def dates(self):
        """Return dates that exist in this month"""
        return Calendar(cf.START_WEEK_DAY - 1, cf.USE_PERSIAN_CALENDAR).monthdayscalendar(self.screen.year, self.screen.month)

    @property
    def week_day(self):
        """Number of the day in week"""
        for week in self.dates:
            try:
                weekday = week.index(self.screen.day)
            except ValueError:
                pass
        return weekday

    @property
    def color(self):
        """Color of the date and dayname"""
        if self.screen.date == self.screen.today:
            return Color.TODAY
        if self.week_day + 1 in cf.WEEKEND_DAYS:
            return Color.WEEKENDS
        return Color.DAYS

    @property
    def icon(self):
        """Icon of today"""
        return cf.TODAY_ICON if self.screen.date == self.screen.today else ''

    def render(self):
        """Render this view on the screen"""
        self.screen.state = AppState.CALENDAR
        if self.screen.x_max < 6 or self.screen.y_max < 3:
            return
        # self.fill_background()
        curses.halfdelay(255)

        # Form a string with month, year, and day with today icon:
        month_names = MONTHS_PERSIAN if cf.USE_PERSIAN_CALENDAR else MONTHS
        month_string = str(month_names[self.screen.month-1])
        # date_string = f'{month_string} {self.screen.day}, {self.screen.year} {icon}'
        date_string = f'{month_string} {self.screen.year}'

        # Display header and footer:
        header_view = HeaderView(self.stdscr, 0, 0, date_string, self.weather, self.screen)
        header_view.render()

        # Display the events from current day to as many as possible days:
        repeated_user_events = RepeatedEvents(self.user_events, cf.USE_PERSIAN_CALENDAR)
        max_num_days = (self.screen.y_max - 5)//2
        vertical_shift = 0

        is_selection_day = True
        for _ in range(max_num_days):
            day_string = f'{self.screen.day} {DAYS[self.week_day]} {self.icon}'
            self.display_line(self.y + 2 + vertical_shift, self.x, day_string, self.color)

            daily_view = DailyView(self.stdscr, self.y + 3 + vertical_shift, self.x, repeated_user_events,
                                   self.user_events, self.user_ics_events, self.holidays, self.birthdays,
                                   self.user_tasks, self.user_ics_tasks, self.screen, 0, is_selection_day)
            daily_view.render()
            vertical_shift += daily_view.num_events_this_day + 3
            self.screen.next_day()
            is_selection_day = False

        # Return screen day back to the original day:
        for _ in range(max_num_days):
            self.screen.previous_day()


class MonthlyScreenView(View):
    """Monthly view showing events of the month"""

    def __init__(self, stdscr, y, x, weather, user_events, user_ics_events, holidays, birthdays, user_tasks, user_ics_tasks, screen):
        super().__init__(stdscr, y, x)
        self.weather = weather
        self.user_events = user_events
        self.user_ics_events = user_ics_events
        self.holidays = holidays
        self.birthdays = birthdays
        self.user_tasks = user_tasks
        self.user_ics_tasks = user_ics_tasks
        self.screen = screen

    def render(self):
        """Render this view on the screen"""
        self.screen.state = AppState.CALENDAR
        if self.screen.x_max < 6 or self.screen.y_max < 3: return
        curses.halfdelay(255)

        # Info about the month:
        month_names = MONTHS_PERSIAN if cf.USE_PERSIAN_CALENDAR else MONTHS
        month_year_string = month_names[self.screen.month-1] + " " + str(self.screen.year)
        dates = Calendar(cf.START_WEEK_DAY - 1, cf.USE_PERSIAN_CALENDAR).monthdayscalendar(self.screen.year, self.screen.month)

        y_cell = (self.screen.y_max - 3) // 6
        x_cell = self.screen.x_max // 7

        header_view = HeaderView(self.stdscr, 0, 0, month_year_string, self.weather, self.screen)
        days_name_view = DaysNameView(self.stdscr, 1, 0, self.screen)
        header_view.render()
        days_name_view.render()

        # Displaying the dates and events:
        repeated_user_events = RepeatedEvents(self.user_events, cf.USE_PERSIAN_CALENDAR)
        num_events_this_month = 0
        for row, week in enumerate(dates):
            for col, day in enumerate(week):
                if day != 0:
                    # Display dates of the month with proper styles:
                    day_in_week = col + (cf.START_WEEK_DAY - 1) - 7 * ((col + (cf.START_WEEK_DAY - 1)) > 6)
                    day_number_view = DayNumberView(self.stdscr, 2 + row * y_cell, col * x_cell, self.screen, day, day_in_week, x_cell)
                    day_number_view.render()

                    # Display the events:
                    self.screen.day = day
                    daily_view = DailyView(self.stdscr, 3 + row * y_cell, col * x_cell, repeated_user_events,
                                           self.user_events, self.user_ics_events, self.holidays, self.birthdays,
                                           self.user_tasks, self.user_ics_tasks, self.screen, num_events_this_month)
                    daily_view.render()
                    num_events_this_month += len(self.user_events.filter_events_that_day(self.screen).items)

        if cf.SHOW_CALENDAR_BOARDERS:
            calendar_boarder_view = CalenarBoarderView(self.stdscr, 0, 0, self.screen)
            calendar_boarder_view.render()


class JournalScreenView(View):
    def __init__(self, stdscr, y, x, weather, user_tasks, user_ics_tasks, screen):
        super().__init__(stdscr, y, x)
        self.weather = weather
        self.user_tasks = user_tasks
        self.user_ics_tasks = user_ics_tasks
        self.screen = screen
        self.refresh_time = 255

    def calculate_refresh_rate(self):
        """Check if a timer is running and change the refresh rate"""
        self.refresh_time = 255
        for task in self.user_tasks.items:
            if task.timer.is_counting:
                self.refresh_time = cf.REFRESH_INTERVAL * 10
                self.screen.refresh_now = False
                break

    def render(self):
        """Journal view showing all tasks"""
        self.screen.state = AppState.JOURNAL
        if self.screen.x_max < 6 or self.screen.y_max < 3:
            return

        # Check if any of the timers is counting, and increase the update time:
        self.calculate_refresh_rate()
        curses.halfdelay(self.refresh_time)

        # Display header and footer:
        header_view = HeaderView(self.stdscr, 0, 0, cf.JOURNAL_HEADER, self.weather, self.screen)
        header_view.render()

        # Display the tasks:
        journal_view = JournalView(self.stdscr, 2, self.screen.x_min, self.user_tasks, self.user_ics_tasks, self.screen)
        journal_view.render()


class WelcomeScreenView(View):
    """Welcome screen displaying greeting info on the first run"""

    def __init__(self, stdscr, y, x, screen):
        super().__init__(stdscr, y, x)
        self.screen = screen

    def calibrate_position(self):
        """Depending on the screen space calculate the best position"""
        self.y_max, self.x_max = self.stdscr.getmaxyx()

    def render(self):
        """Draw the welcome screen"""
        self.calibrate_position()
        curses.halfdelay(255)
        self.stdscr.clear()
        self.fill_background()

        if self.x_max < len(MSG_WELCOME_4)+2 or self.y_max < 12:
            self.display_line(0, 0, "Welcome!", Color.ACTIVE_PANE)
            return

        d_x = self.x_max//2
        d_y = self.y_max//2 - 5

        self.display_line(d_y, d_x - len(MSG_WELCOME_1+__version__+" ")//2, f"{MSG_WELCOME_1} {__version__}", Color.ACTIVE_PANE)
        self.display_line(d_y + 1, d_x - len(MSG_WELCOME_2)//2, MSG_WELCOME_2, Color.TODO)
        self.display_line(d_y + 3, d_x - len(MSG_WELCOME_3)//2, MSG_WELCOME_3, Color.TODO)
        self.display_line(d_y + 4, d_x - len(cf.config_folder)//2, cf.config_folder, Color.TITLE)
        self.display_line(d_y + 6, d_x - len(MSG_WELCOME_4)//2, MSG_WELCOME_4, Color.TODO)
        self.display_line(d_y + 7, d_x - len(MSG_SITE)//2, MSG_SITE, Color.TITLE)
        self.display_line(d_y + 9, d_x - len(MSG_WELCOME_5)//2, MSG_WELCOME_5, Color.TODO)


class HelpScreenView(View):
    """Help screen displaying information about keybindings"""

    def __init__(self, stdscr, y, x, screen):
        super().__init__(stdscr, y, x)
        self.screen = screen

    def calibrate_position(self):
        """Depending on the screen space calculate the best position"""
        self.y_max, self.x_max = self.stdscr.getmaxyx()

        if self.x_max < 102:
            self.global_shift_x = 0
            self.shift_x = 0
            self.shift_y = 6 + len(KEYS_GENERAL) + len(KEYS_CALENDAR)
        else:
            self.global_shift_x = (self.x_max - 102) // 2
            self.shift_x = 45
            self.shift_y = 2

        if self.y_max > 20 and self.x_max >= 102:
            self.global_shift_y = (self.y_max - 20) // 2
        else:
            self.global_shift_y = 0

    def render(self):
        """Draw the help screen"""
        self.calibrate_position()
        if self.x_max < 6 or self.y_max < 3:
            return
        curses.halfdelay(255)
        self.stdscr.clear()
        self.fill_background()

        # Left column:
        self.display_line(self.global_shift_y, self.global_shift_x + 1, f"{MSG_NAME} {__version__}",
                            Color.ACTIVE_PANE, cf.BOLD_TITLE, cf.UNDERLINED_TITLE)
        self.display_line(self.global_shift_y + 2, self.global_shift_x + 8,
                          TITLE_KEYS_GENERAL, Color.TITLE, cf.BOLD_TITLE, cf.UNDERLINED_TITLE)
        for index, key in enumerate(KEYS_GENERAL):
            self.display_line(self.global_shift_y + index + 3, self.global_shift_x, key, Color.TODAY)
            self.display_line(self.global_shift_y + index + 3, self.global_shift_x + 8, KEYS_GENERAL[key], Color.TODO)

        self.display_line(self.global_shift_y + 4 + len(KEYS_GENERAL), self.global_shift_x + 8,
                          TITLE_KEYS_CALENDAR, Color.TITLE, cf.BOLD_TITLE, cf.UNDERLINED_TITLE)
        for index, key in enumerate(KEYS_CALENDAR):
            self.display_line(self.global_shift_y + index + 5 + len(KEYS_GENERAL), self.global_shift_x, key, Color.TODAY)
            self.display_line(self.global_shift_y + index + 5 + len(KEYS_GENERAL), self.global_shift_x + 8,
                                                                            KEYS_CALENDAR[key], Color.TODO)

        # Right column:
        d_x = self.global_shift_x + self.shift_x
        d_y = self.global_shift_y + self.shift_y
        self.display_line(d_y, d_x + 8, TITLE_KEYS_JOURNAL, Color.TITLE, cf.BOLD_TITLE, cf.UNDERLINED_TITLE)
        for index, key in enumerate(KEYS_TODO):
            self.display_line(d_y + index + 1, d_x, key, Color.TODAY)
            self.display_line(d_y + index + 1, d_x + 8, KEYS_TODO[key], Color.TODO)

        # Additional info:
        d_x = self.global_shift_x + self.shift_x + 8
        d_y = self.global_shift_y + len(KEYS_TODO) + self.shift_y
        self.display_line(d_y + 2, d_x, MSG_VIM, Color.ACTIVE_PANE)
        self.display_line(d_y + 4, d_x, MSG_INFO, Color.TODO)
        self.display_line(d_y + 5, d_x, MSG_SITE, Color.TITLE)


def main(stdscr) -> None:
    """Main function that runs and switches screens"""

    # Load the data:
    weather = Weather(cf.WEATHER_CITY)
    if cf.SHOW_WEATHER:
        sys.stdout.write(f"\r{MSG_WEATHER}")
        weather.load_from_wttr()
    screen = Screen(stdscr, cf)

    # Initialise loaders:
    event_loader_csv = EventLoaderCSV(cf)
    task_loader_csv = TaskLoaderCSV(cf)
    event_loader_ics = EventLoaderICS(cf)
    task_loader_ics = TaskLoaderICS(cf)
    birthday_loader = BirthdayLoader(cf)
    holiday_loader = HolidayLoader(cf)

    # Load the data:
    user_events = event_loader_csv.load()
    user_tasks = task_loader_csv.load()
    user_ics_events = event_loader_ics.load()
    user_ics_tasks = task_loader_ics.load()
    holidays = holiday_loader.load()
    birthdays = birthday_loader.load()

    # Initialise savers and importers:
    event_saver_csv = EventSaverCSV(user_events, cf)
    task_saver_csv = TaskSaverCSV(user_tasks, cf)
    importer = Importer(user_tasks, user_events, cf)

    read_items_from_user_arguments(screen, user_tasks, user_events, task_saver_csv, event_saver_csv)

    # Initialise terminal screen:
    stdscr = curses.initscr()
    curses.noecho()
    curses.curs_set(False)
    initialize_colors(cf)

    # Initialise screen views:
    app_view = View(stdscr, 0, 0)
    monthly_screen_view = MonthlyScreenView(stdscr, 0, 0, weather, user_events, user_ics_events,
                                            holidays, birthdays, user_tasks, user_ics_tasks, screen)
    daily_screen_view = DailyScreenView(stdscr, 0, 0, weather, user_events, user_ics_events,
                                        holidays, birthdays, user_tasks, user_ics_tasks, screen)
    journal_screen_view = JournalScreenView(stdscr, 0, 0, weather, user_tasks, user_ics_tasks, screen)
    help_screen_view = HelpScreenView(stdscr, 0, 0, screen)
    welcome_screen_view = WelcomeScreenView(stdscr, 0, 0, screen)
    footer_view = FooterView(stdscr, 0, 0, screen)
    separator_view = SeparatorView(stdscr, 0, 0, screen)

    # Show welcome screen on the first run:
    if cf.is_first_run:
        screen.state = AppState.WELCOME
    while screen.state == AppState.WELCOME:
        welcome_screen_view.render()
        control_welcome_screen(stdscr, screen)

    # Running different screens depending on the state:
    while screen.state != AppState.EXIT:
        if not screen.split:
            stdscr.clear()
            app_view.fill_background()
        screen.active_pane = False

        # CALENDARS

        # Monthly (active) screen:
        if screen.state == AppState.CALENDAR and screen.calendar_state == CalState.MONTHLY:
            if screen.split and not screen.selection_mode:
                stdscr.clear()
                app_view.fill_background()
                journal_screen_view.render()
            screen.active_pane = True
            monthly_screen_view.render()
            if screen.split: separator_view.render()
            footer_view.render()
            control_monthly_screen(stdscr, user_events, screen, importer)

        # Daily (active) screen:
        elif screen.state == AppState.CALENDAR and screen.calendar_state == CalState.DAILY:
            if screen.split and not screen.selection_mode:
                stdscr.clear()
                app_view.fill_background()
                journal_screen_view.render()
            screen.active_pane = True
            daily_screen_view.render()
            if screen.split: separator_view.render()
            footer_view.render()
            control_daily_screen(stdscr, user_events, screen, importer)

        # JOURNAL

        # Journal (active) screen:
        elif screen.state == AppState.JOURNAL:
            if screen.split and not screen.selection_mode:
                if screen.refresh_now:
                    stdscr.clear()
                    app_view.fill_background()
                if screen.calendar_state == CalState.MONTHLY:
                    monthly_screen_view.render()
                else:
                    daily_screen_view.render()
            screen.active_pane = True
            journal_screen_view.render()
            if screen.split: separator_view.render()
            footer_view.render()
            control_journal_screen(stdscr, user_tasks, screen, importer)

        # Help screen:
        elif screen.state == AppState.HELP:
            help_screen_view.render()
            control_help_screen(stdscr, screen)

        else:
            break

        # If something has been changed, save the data:
        if user_events.changed:
            event_saver_csv.save()
            screen.refresh_now = True
        if user_tasks.changed:
            task_saver_csv.save()
            screen.refresh_now = True

    # Cleaning up before quitting:
    curses.echo()
    curses.curs_set(True)
    curses.endwin()


def cli() -> None:
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    cli()
