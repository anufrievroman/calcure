#!/usr/bin/env python
# Libraries
import curses
import datetime
import calendar
import csv
import os
import pathlib
import configparser
import re
import sys
import getopt
import time

# Modules
from config import cf
from screen import Screen
from data import *
from translation_en import *
from controls import *
from helpers import *


class View:
    '''Parent clalls of a view that displays information at certain coordinates'''
    def __init__(self, stdsrc, y, x):
        self.stdscr = stdsrc
        self.y = y
        self.x = x

    def fill_background(self):
        '''Fill the screen background with background color'''
        y_max, x_max = self.stdscr.getmaxyx()
        for index in range(y_max - 1):
            self.stdscr.addstr(index, 0, " " * x_max, curses.color_pair(1))

    def display_line(self, y, x, text, color, bold=False, underlined=False):
        '''Display the line of text respecting the slyling and available space'''

        # Make sure that we display inside the screen:
        y_max, x_max = self.stdscr.getmaxyx()
        if y >= y_max or x >= x_max: return

        # Cut the text if it does not fit the screen:
        text = text[:(x_max - 1 - x)]

        if bold and underlined:
            self.stdscr.addstr(y, x, text, curses.color_pair(color) | curses.A_BOLD | curses.A_UNDERLINE)
        elif bold and not underlined:
            self.stdscr.addstr(y, x, text, curses.color_pair(color) | curses.A_BOLD)
        elif underlined and not bold:
            self.stdscr.addstr(y, x, text, curses.color_pair(color) | curses.A_UNDERLINE)
        else:
            self.stdscr.addstr(y, x, text, curses.color_pair(color))


#################### TASK VIEWS ########################


class TaskView(View):
    '''Display a single task'''
    def __init__(self, stdscr, y, x, task, privacy):
        super().__init__(stdscr, y, x)
        self.task = task
        self.privacy = privacy

    @property
    def color(self):
        '''Select the color depending on the status'''
        color = 11
        if self.task.status == 'done':
            color = 12
        if self.task.status == 'important':
            color = 13
        if self.task.status == 'unimportant':
            color = 20
        return color

    @property
    def icon(self):
        '''Select the right icon for the task'''
        icon = cf.TODO_ICON
        if cf.DISPLAY_ICONS:
            for keyword in cf.ICONS:
                if keyword in self.task.name.lower():
                    icon = cf.ICONS[keyword]
        if self.task.status == 'done':
            icon = cf.DONE_ICON
        if self.task.status == 'important':
            icon = cf.IMPORTANT_ICON
        if self.privacy:
            icon = cf.PRIVACY_ICON
        return icon

    @property
    def tab(self):
        '''Calculate the tab depending on the task level'''
        if self.task.name[:4] == '----':
            return 4
        elif self.task.name[:2] == '--':
            return 2
        else:
            return 0

    @property
    def title(self):
        '''Obfuscate the name if privacy mode is on'''
        if self.privacy:
            return cf.PRIVACY_ICON*len(self.task.name[tab:])
        else:
            return self.task.name[self.tab:]

    def render(self):
        '''Display a line with an icon, task, and timer'''
        self.display_line(self.y, self.x + self.tab, f'{self.icon} {self.title}', self.color)
        timer_view = TimerView(self.stdscr, self.y, 5 + len(self.task.name), self.task.timer)
        timer_view.render()


class TimerView(View):
    '''Display a single task'''
    def __init__(self, stdscr, y, x, timer):
        super().__init__(stdscr, y, x)
        self.timer = timer

    @property
    def color(self):
        '''Select the color depending on the timer status'''
        color = 14 if self.timer.is_counting else 15
        return color

    @property
    def icon(self):
        '''Return icon corresponding to timer state'''
        if self.timer.is_counting == False and cf.DISPLAY_ICONS:
            icon = "⏯︎ "
        elif self.timer.is_counting == True and cf.DISPLAY_ICONS:
            icon = "⏵ "
        else:
            icon = ''
        return icon

    def render(self):
        '''Display a line with a timer and icon'''
        if self.timer.is_started:
            time_string = self.icon + self.timer.calculate_passed_time()
            self.display_line(self.y, self.x, time_string, self.color)


class JournalView(View):
    '''Displays a list of tasks'''
    def __init__(self, stdscr, y, x, user_tasks, screen):
        super().__init__(stdscr, y, x)
        self.user_tasks = user_tasks
        self.screen = screen

    def render(self):
        '''Render the list of tasks'''
        for index, task in enumerate(self.user_tasks.items):
            task_view = TaskView(self.stdscr, self.y, self.x, task, self.screen.privacy)
            task_view.render()
            if self.screen.selection_mode:
                self.display_line(self.y, self.x, str(index+1), 4)
            self.y += 1


##################### EVENT VIEWS ##############################


class EventView(View):
    '''Parent class to display events'''
    def __init__(self, stdscr, y, x, event, screen):
        super().__init__(stdscr, y, x)
        self.event = event
        self.screen = screen

    @property
    def color(self):
        '''Select the color depending on the status and type'''
        color = 17
        if self.event.status == 'important':
            color = 13
        if self.event.status == 'unimportant':
            color = 20
        return color

    def obfuscate_name(self, privacy):
        '''Obfuscate the info if privacy mode is on'''
        if privacy:
            return cf.PRIVACY_ICON*len(self.event.name)
        else:
            return self.event.name

class UserEventView(EventView):
    '''Display a single user event'''
    @property
    def icon(self):
        '''Select the right icon for the event'''
        icon = cf.EVENT_ICON
        if cf.DISPLAY_ICONS:
            for keyword in cf.ICONS:
                if keyword in self.event.name.lower():
                    icon = cf.ICONS[keyword]
        if self.screen.privacy: icon = cf.PRIVACY_ICON
        return icon

    def render(self):
        '''Display a line with an event'''
        title = self.obfuscate_name(self.screen.privacy)
        self.display_line(self.y, self.x, f'{self.icon} {title}', self.color)


class BirthdayView(EventView):
    def render(self):
        '''Display a line with birthday icon and name'''
        title = self.obfuscate_name(self.screen.privacy)
        self.display_line(self.y, self.x, f'{cf.BIRTHDAY_ICON} {title}', 7)


class HolidayView(EventView):
    def render(self):
        '''Display a line with holiday icon and occasion'''
        self.display_line(self.y, self.x, f'{cf.HOLIDAY_ICON} {self.event.name}', 16)


class DailyView(View):
    def __init__(self, stdscr, y, x, user_events, holidays, birthdays, screen, index_offset):
        super().__init__(stdscr, y, x)
        self.user_events = user_events.filter_events_that_day(screen)
        self.holidays = holidays.filter_events_that_day(screen)
        self.birthdays = birthdays
        self.screen = screen
        self.index_offset = index_offset
        self.y_cell = (self.screen.y_max-3)//6
        self.x_cell = self.screen.x_max//7

    def render(self):
        '''Display all events occuring on this days'''
        index = 0

        # Show holidays:
        if not cf.DISPLAY_HOLIDAYS: return
        for event in self.holidays.items:
            holiday_view = HolidayView(self.stdscr, self.y + index, self.x, event, self.screen)
            holiday_view.render()
            index += 1

        # Show birthdays:
        if not cf.BIRTHDAYS_FROM_ABOOK: return
        for event in self.birthdays.items:
            if event.day == self.screen.day and event.month == self.screen.month:
                birthday_view = BirthdayView(self.stdscr, self.y + index, self.x, event, self.screen)
                birthday_view.render()
                index += 1

        # Show user events:
        for event in self.user_events.items:
            if index < self.y_cell-2:
                user_event_view = UserEventView(self.stdscr, self.y + index, self.x, event, self.screen)
                user_event_view.render()
                if self.screen.selection_mode:
                    self.display_line(self.y + index, self.x, str(index + self.index_offset + 1), 4)
            else:
                self.display_line(self.y + self.y_cell - 2, self.x, cf.HIDDEN_ICON, 17)
            index += 1


##################### ADDITIONAL VIEWS ##############################


class DayNumberView(View):
    def __init__(self, stdscr, y, x, screen, day, day_in_week, x_cell):
        super().__init__(stdscr, y, x)
        self.screen = screen
        self.day = day
        self.day_in_week = day_in_week
        self.x_cell = x_cell

    def render(self):
        '''Display number of the day in month with proper styling'''
        # Today:
        if datetime.date(self.screen.year, self.screen.month, self.day) == datetime.date.today():
            self.display_line(self.y, self.x, str(self.day)+cf.TODAY_ICON+' '*self.x_cell, 4, cf.BOLD_TODAY, cf.UNDERLINED_TODAY)
        # Week days:
        elif self.day_in_week+1 in cf.WEEKEND_DAYS:
            self.display_line(self.y, self.x, str(self.day)+' '*self.x_cell, 2, cf.BOLD_WEEKENDS, cf.UNDERLINED_WEEKENDS)
        # Weekend days:
        else:
            self.display_line(self.y, self.x, str(self.day)+' '*self.x_cell, 5, cf.BOLD_DAYS, cf.UNDERLINED_DAYS)


class WeatherView(View):
    '''Display weather forcast in the corner'''
    def __init__(self, stdscr, y, x, weather):
        super().__init__(stdscr, y, x)
        self.weather = weather

    def render(self):
        '''Display the weather if space allows'''
        if not cf.SHOW_WEATHER or not self.weather.loaded: return
        _, x_max   = self.stdscr.getmaxyx()

        self.display_line(0, x_max-len(self.weather.forcast), self.weather.forcast, 19)


class CurrentTimeView(View):
    '''Display current time in the center'''
    def render(self):
        if not cf.SHOW_CURRENT_TIME: return
        time_string = time.strftime("%H:%M", time.localtime())
        self.display_line(self.y, self.x, time_string, 18)


class TitleView(View):
    '''Show the title such as month, date, of jounal name'''
    def __init__(self, stdscr, y, x, title):
        super().__init__(stdscr, y, x)
        self.title = title

    def render(self):
        if not cf.SHOW_TITLE: return

        _, x_max = self.stdscr.getmaxyx()
        if x_max > 2*len(self.title) + 6:
            self.display_line(0, 0, self.title, 21, cf.BOLD_TITLE, cf.UNDERLINED_TITLE)


class HeaderView(View):
    '''Show the header that includes the weather, time, and title'''
    def __init__(self, stdscr, y, x, title, weather, screen):
        super().__init__(stdscr, y, x)
        self.title = title
        self.weather = weather
        self.screen = screen

    def render(self):
        title_view = TitleView(self.stdscr, 0, 0, self.title)
        current_time_view = CurrentTimeView(self.stdscr, 0, (self.screen.x_max//2-2))
        weather_view = WeatherView(self.stdscr, 0, 0, self.weather)

        title_view.render()
        current_time_view.render()
        if len(self.weather.forcast) < self.screen.x_max - len(self.title):
            weather_view.render()


class FooterView(View):
    '''Display the footer with keybinding'''
    def __init__(self, stdscr, y, x, info):
        super().__init__(stdscr, y, x)
        self.info = info

    def render(self):
        if not cf.SHOW_KEYBINDINGS: return
        self.display_line(self.y, self.x, self.info, 3)


class DaysNameView(View):
    '''Display day name depending on the screen available and with right style'''
    def __init__(self, stdscr, y, x, screen):
        super().__init__(stdscr, y, x)
        self.screen = screen

    def render(self):
        if not cf.SHOW_DAY_NAMES: return

        num = 2 if self.screen.x_max < 80 else 10
        x_cell = int(self.screen.x_max//7)
        # Depending on which day we start the week, weekends are shifted:
        for i in range(7):
            shift = cf.START_WEEK_DAY-1
            day_number = i + shift - 7*((i+shift) > 6)
            name = calendar.day_name[day_number][:num].upper()
            if day_number + 1 not in cf.WEEKEND_DAYS:
                self.display_line(self.y, self.x+i*x_cell, name, 1, cf.BOLD_DAY_NAMES, cf.UNDERLINED_DAY_NAMES)
            else:
                self.display_line(self.y, self.x+i*x_cell, name, 6, cf.BOLD_WEEKEND_NAMES, cf.UNDERLINED_WEEKEND_NAMES)


##################### SCREENS ##########################


class DailyScreenView(View):
    '''Daily view showing events of the day'''
    def __init__(self, stdscr, y, x, weather, user_events, holidays, birthdays, screen):
        super().__init__(stdscr, y, x)
        self.weather = weather
        self.user_events = user_events
        self.holidays = holidays
        self.birthdays = birthdays
        self.screen = screen

    def render(self):
        self.stdscr.clear()
        if self.screen.x_max < 6 or self.screen.y_max < 3: return
        self.fill_background()
        curses.halfdelay(255)

        # Form a string with month, year, and day with today icon:
        icon = cf.TODAY_ICON if self.screen.date == datetime.date.today() else ''
        month_string = str(calendar.month_name[self.screen.month].upper())
        date_string = (f'{month_string} {self.screen.day}, {self.screen.year} {icon}')

        # Display header and footer:
        header_view = HeaderView(self.stdscr, 0, 0, date_string, self.weather, self.screen)
        footer_view = FooterView(self.stdscr, self.screen.y_max-2, 0, CALENDAR_HINT)
        header_view.render()
        footer_view.render()

        # Display the events:
        daily_view = DailyView(self.stdscr, self.y + 2, self.x, self.user_events, self.holidays, self.birthdays, self.screen, 0)
        daily_view.render()


class MonthlyScreenView(View):
    '''Monthly view showing events of the month'''

    def __init__(self, stdscr, y, x, weather, user_events, holidays, birthdays, screen):
        super().__init__(stdscr, y, x)
        self.weather = weather
        self.user_events = user_events
        self.holidays = holidays
        self.birthdays = birthdays
        self.screen = screen

    def render(self):
        self.stdscr.clear()
        if self.screen.x_max < 6 or self.screen.y_max < 3: return
        curses.halfdelay(255)
        self.fill_background()

        # Info about the month:
        month_year_string = calendar.month_name[self.screen.month].upper() + " " + str(self.screen.year)
        dates = calendar.Calendar(firstweekday=cf.START_WEEK_DAY-1).monthdayscalendar(self.screen.year, self.screen.month)

        y_cell = (self.screen.y_max-3)//6
        x_cell = self.screen.x_max//7

        # Displaying header and footer:
        header_view = HeaderView(self.stdscr, 0, 0, month_year_string, self.weather, self.screen)
        days_name_view = DaysNameView(self.stdscr, 1, 0, self.screen)
        footer_view = FooterView(self.stdscr, self.screen.y_max-2, 0, CALENDAR_HINT)
        header_view.render()
        days_name_view.render()
        footer_view.render()

        # Displaying the dates and events:
        num_events_this_month = 0
        for row, week in enumerate(dates):
            for col, day in enumerate(week):
                if day != 0:
                    # Display dates of the month with proper styles:
                    day_in_week = col+(cf.START_WEEK_DAY-1) - 7*((col+(cf.START_WEEK_DAY-1)) > 6)
                    day_number_view = DayNumberView(self.stdscr, 2+row*y_cell, col*x_cell, self.screen, day, day_in_week, x_cell)
                    day_number_view.render()

                    # Display the events:
                    self.screen.day = day
                    daily_view = DailyView(self.stdscr, 3+row*y_cell, col*x_cell, self.user_events,
                            self.holidays, self.birthdays, self.screen, num_events_this_month)
                    daily_view.render()
                    num_events_this_month += len(self.user_events.filter_events_that_day(self.screen).items)


class JournalScreenView(View):
    def __init__(self, stdscr, y, x, weather, user_tasks, screen):
        super().__init__(stdscr, y, x)
        self.weather = weather
        self.user_tasks = user_tasks
        self.screen = screen
        self.refresh_time = 255
        self.refresh_now = True

    def calculate_refresh_rate(self):
        '''Check if a timer is running and change the refresh rate'''
        for task in self.user_tasks.items:
            if task.timer.is_counting:
                self.refresh_time = cf.REFRESH_INTERVAL*10
                self.refresh_now = False
                break

    def render(self):
        '''Journal view showing all tasks'''
        if self.refresh_now: self.stdscr.clear()
        if self.screen.x_max < 6 or self.screen.y_max < 3: return
        self.fill_background()

        # Check if any of the timers is counting, and increase the update time:
        self.calculate_refresh_rate()
        curses.halfdelay(self.refresh_time)

        # Display header and footer:
        header_view = HeaderView(self.stdscr, 0, 0, cf.JOURNAL_HEADER, self.weather, self.screen)
        footer_view = FooterView(self.stdscr, self.screen.y_max-2, 0, TODO_HINT)
        header_view.render()
        footer_view.render()

        # Display the tasks:
        journal_view = JournalView(self.stdscr, 2, 0, self.user_tasks, self.screen)
        journal_view.render()


class HelpScreenView(View):
    '''Help screen displaying information about keybindings'''
    def __init__(self, stdscr, y, x, screen):
        super().__init__(stdscr, y, x)
        self.screen = screen

        # Depending on the screen space calculate the best position:
        if self.screen.x_max < 102:
            self.global_shift_x = 0
            self.shift_x = 0
            self.shift_y = 6 + len(KEYS_GENERAL) + len(KEYS_CALENDAR)
        else:
            self.global_shift_x = (self.screen.x_max - 102)//2
            self.shift_x = 45
            self.shift_y = 2

        if self.screen.y_max > 20 and self.screen.x_max >= 102:
            self.global_shift_y = (self.screen.y_max - 20)//2
        else:
            self.global_shift_y = 0

    def render(self):
        '''Draw the help screen'''
        if self.screen.x_max < 6 or self.screen.y_max < 3: return
        curses.halfdelay(255)
        self.stdscr.clear()
        self.fill_background()

        # Left column:
        self.display_line(self.global_shift_y,self.global_shift_x + 1,
                MSG_NAME[:self.screen.x_max-3], 6, cf.BOLD_TITLE, cf.UNDERLINED_TITLE)
        self.display_line(self.global_shift_y + 2,self.global_shift_x + 8,
                TITLE_KEYS_GENERAL, 4, cf.BOLD_TITLE, cf.UNDERLINED_TITLE)
        for index, key in enumerate(KEYS_GENERAL):
            line = str(key+" "+KEYS_GENERAL[key])
            self.display_line(self.global_shift_y + index + 3,self.global_shift_x, line, 5)

        self.display_line(self.global_shift_y + 4+len(KEYS_GENERAL),self.global_shift_x + 8,
                TITLE_KEYS_CALENDAR[:self.screen.x_max-3], 4, cf.BOLD_TITLE, cf.UNDERLINED_TITLE)
        for index, key in enumerate(KEYS_CALENDAR):
            line = str(key+" "+KEYS_CALENDAR[key])
            self.display_line(self.global_shift_y + index + 5 + len(KEYS_GENERAL), self.global_shift_x, line, 5)

        # Right column:
        d_x = self.global_shift_x + self.shift_x
        d_y = self.global_shift_y + self.shift_y
        self.display_line(d_y, d_x + 8, TITLE_KEYS_JOURNAL, 4, cf.BOLD_TITLE, cf.UNDERLINED_TITLE)
        for index, key in enumerate(KEYS_TODO):
            line = str(key + " " + KEYS_TODO[key])
            self.display_line(d_y + index + 1, d_x, line, 5)

        # Additional info:
        d_x = self.global_shift_x + self.shift_x + 8
        d_y = self.global_shift_y + len(KEYS_TODO) + self.shift_y
        self.display_line(d_y + 2, d_x, MSG_VIM, 6)
        self.display_line(d_y + 4, d_x, MSG_INFO, 5)
        self.display_line(d_y + 5, d_x, MSG_SITE, 4)


########################## MAIN ###############################


def main(stdscr):
    '''Main function that runs and switches screens'''

    # Load the data
    weather = Weather(cf.WEATHER_CITY)
    if cf.SHOW_WEATHER:
        print("Weather is loading...")
        WeatherLoader.load_from_wttr(weather)
    screen = Screen(stdscr, cf.PRIVACY_MODE, cf.DEFAULT_VIEW)
    user_events = UserEventsLoader.load_from_file(cf.EVENTS_FILE)
    holidays = HolidaysLoader.load_holidays(screen.year, cf.HOLIDAY_COUNTRY)
    birthdays = BirthdaysLoader.load_birthdays_from_abook()
    user_tasks = UserTasksLoader.load_from_file(cf.TASKS_FILE)


    # Initialise the terminal screen
    stdscr = curses.initscr()
    curses.noecho()
    curses.curs_set(False)
    initialize_colors(stdscr)


    # Running different screens depending on the state:
    while screen.state != 'exit':

        # Initialise screens:
        monthly_screen_view = MonthlyScreenView(stdscr, 0, 0, weather, user_events, holidays, birthdays, screen)
        daily_screen_view = DailyScreenView(stdscr, 0, 0, weather, user_events, holidays, birthdays, screen)
        journal_screen_view = JournalScreenView(stdscr, 0, 0, weather, user_tasks, screen)
        help_screen_view = HelpScreenView(stdscr, 0, 0, screen)

        # Monthly screen:
        if screen.state == 'calendar':
            monthly_screen_view.render()
            control_monthly_screen(stdscr, user_events, screen)

        # Daily screen:
        elif screen.state == 'daily_calendar':
            daily_screen_view.render()
            control_daily_screen(stdscr, user_events, screen)

        # Journal screen:
        elif screen.state == 'journal':
            journal_screen_view.render()
            control_journal_screen(stdscr, user_tasks, screen)

        # Help screen:
        elif screen.state == 'help':
            help_screen_view.render()
            control_help_screen(stdscr, screen)

        else:
            break

        # If something changed, save and reload the data:
        if user_events.changed:
            UserEventsSaver.save_to_file(user_events, cf.EVENTS_FILE)
            user_events = UserEventsLoader.load_from_file(cf.EVENTS_FILE)
        if user_tasks.changed:
            UserTasksSaver.save_to_file(user_tasks, cf.TASKS_FILE)
            user_tasks = UserTasksLoader.load_from_file(cf.TASKS_FILE)

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
