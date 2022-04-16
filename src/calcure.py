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


#################### TASK VIEWS ########################


class TaskView:
    '''Display a single task'''
    def __init__(self, task):
        self.task = task

    def color(self):
        '''Select the color depending on the status'''
        if self.task.status == 'done':
            return 12
        if self.task.status == 'important':
            return 13
        if self.task.status == 'unimportant':
            return 20
        return 11

    def icon(self, privacy):
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
        if privacy:
            icon = cf.PRIVACY_ICON
        return icon

    def render(self, stdscr, y, x, privacy):
        '''Display a line with a task with right indentation'''
        if self.task.name[:4] == '----':
            tab = 4
        elif self.task.name[:2] == '--':
            tab = 2
        else:
            tab = 0

        # Obfuscate the name if privacy mode is on:
        if privacy:
            name = cf.PRIVACY_ICON*len(self.task.name[tab:])
        else:
            name = self.task.name[tab:]

        # Display the icon, name, and timer:
        display_line(stdscr, y, x+tab, self.icon(privacy), self.color())
        display_line(stdscr, y, x+2+tab, name, self.color())
        timer_view = TimerView(self.task.timer)
        timer_view.render(stdscr, y, 5+len(self.task.name))


class TimerView:
    '''Display a single task'''
    def __init__(self, timer):
        self.timer = timer

    def color(self):
        '''Select the color depending on the status'''
        return 14 if self.timer.is_counting else 15

    def icon(self):
        '''Return icon corresponding to timer state'''
        if self.timer.is_counting == False and cf.DISPLAY_ICONS:
            icon = "⏯︎ "
        elif self.timer.is_counting == True and cf.DISPLAY_ICONS:
            icon = "⏵ "
        else:
            icon = ''
        return icon

    def render(self, stdscr, y, x):
        '''Display a line with a timer and icon'''
        time_string = self.timer.calculate_passed_time()
        time_string = self.icon() + time_string

        if self.timer.is_started:
            display_line(stdscr, y, x, time_string, self.color())


class JournalView:
    '''Displays a list of tasks'''
    def __init__(self, user_tasks):
        self.user_tasks = user_tasks

    def render(self, stdscr, y, x, screen):
        '''Render the list of tasks'''
        for index, task in enumerate(self.user_tasks.items):
            task_view = TaskView(task)
            task_view.render(stdscr, y, x, screen.privacy)
            if screen.selection_mode:
                display_line(stdscr, y, 1, str(index+1), 4)
            y += 1

class EventView:
    '''Parent class to display events'''
    def __init__(self, event):
        self.event = event

    def obfuscate_name(self, privacy):
        '''Obfuscate the info if privacy mode is on'''
        return cf.PRIVACY_ICON*len(self.event.name) if privacy else self.event.name


##################### EVENT VIEWS ##############################


class UserEventView(EventView):
    '''Display a single user event'''

    def color(self):
        '''Select the color depending on the status and type'''
        if self.event.status == 'important':
            return 13
        if self.event.status == 'unimportant':
            return 20
        return 17

    def icon(self, privacy):
        '''Select the right icon for the event'''
        icon = cf.EVENT_ICON
        if cf.DISPLAY_ICONS:
            for keyword in cf.ICONS:
                if keyword in self.event.name.lower():
                    icon = cf.ICONS[keyword]
        if privacy: icon = cf.PRIVACY_ICON
        return icon

    def render(self, stdscr, y, x, privacy, x_cell):
        '''Display a line with an event'''
        display_line(stdscr, y, x, self.icon(privacy), self.color())
        display_line(stdscr, y, x+2, self.obfuscate_name(privacy), self.color())


class BirthdayView(EventView):
    def render(self, stdscr, y, x, privacy):
        '''Display a line with birthday icon and name'''
        display_line(stdscr, y, x, cf.BIRTHDAY_ICON, 7)
        display_line(stdscr, y, x+2, self.obfuscate_name(privacy), 7)


class HolidayView(EventView):
    def render(self, stdscr, y, x, privacy):
        '''Display a line with holiday icon and occasion'''
        display_line(stdscr, y, x, cf.HOLIDAY_ICON, 16)
        display_line(stdscr, y, x+2, self.obfuscate_name(privacy), 16)


class DailyView():
    def __init__(self, user_events, holidays, birthdays, screen):
        self.user_events = user_events.filter_events_that_day(screen.date)
        self.holidays = holidays.filter_events_that_day(screen.date)
        self.birthdays = birthdays

    def render(self, stdscr, y, x, screen, y_cell, x_cell):
        '''Display all events occuring on this days'''
        index = 0

        # Show holidays:
        if not cf.DISPLAY_HOLIDAYS: return
        for event in self.holidays.items:
            holiday_view = HolidayView(event)
            holiday_view.render(stdscr, y+index, x, screen.privacy)
            index += 1

        # Show birthdays:
        if not cf.BIRTHDAYS_FROM_ABOOK: return
        for event in self.birthdays.items:
            if event.day == screen.day and event.month == screen.month:
                birthday_view = BirthdayView(event)
                birthday_view.render(stdscr, y+index, x, screen.privacy)
                index += 1

        # Show user events:
        for event in self.user_events.items:
            user_event_view = UserEventView(event)
            if index < y_cell-2:
                user_event_view.render(stdscr, y+index, x, screen.privacy, x_cell)
                if screen.selection_mode:
                    display_line(stdscr, y+index, x, str(index+1), 4)
            else:
                display_line(stdscr, y+y_cell-2, x, cf.HIDDEN_ICON, 17)
            index += 1


##################### ADDITIONAL VIEWS ##############################


class DayNumberView:
    @staticmethod
    def render(stdscr, y, x, screen, day, day_in_week, x_cell):
        '''Display number of the day in month with proper styling'''
        # Today:
        if datetime.date(screen.year, screen.month, day) == datetime.date.today():
            display_line(stdscr, y, x, str(day)+cf.TODAY_ICON+' '*x_cell, 4, cf.BOLD_TODAY, cf.UNDERLINED_TODAY)
        # Week days:
        elif day_in_week+1 in cf.WEEKEND_DAYS:
            display_line(stdscr, y, x, str(day)+' '*x_cell, 2, cf.BOLD_WEEKENDS, cf.UNDERLINED_WEEKENDS)
        # Weekend days:
        else:
            display_line(stdscr, y, x, str(day)+' '*x_cell, 5, cf.BOLD_DAYS, cf.UNDERLINED_DAYS)


class WeatherView:
    @staticmethod
    def render(stdscr, weather):
        '''Display the weather if space allows'''
        if not cf.SHOW_WEATHER: return
        _, x_max   = stdscr.getmaxyx()
        if weather.loaded:
            stdscr.addstr(0, x_max - len(weather.forcast), weather.forcast, curses.color_pair(19))
            display_line(stdscr, 0, x_max-len(weather.forcast), weather.forcast, 19)


class CurrentTimeView:
    @staticmethod
    def render(stdscr):
        '''Show the widget with current time if space allows'''
        if not cf.SHOW_CURRENT_TIME: return
        _, x_max   = stdscr.getmaxyx()
        time_string = time.strftime("%H:%M", time.localtime())
        stdscr.addstr(0, x_max//2-2, time_string, curses.color_pair(18))


class TitleView:
    @staticmethod
    def render(stdscr, title):
        '''Show the title such as month, date, of jounal name'''
        if not cf.SHOW_TITLE: return
        display_line(stdscr, 0, 0, title, 21, cf.BOLD_TITLE, cf.UNDERLINED_TITLE)


class HeaderView:
    @staticmethod
    def render(stdscr, title, weather, x_max):
        '''Show the header that includes the weather, time, and title'''
        # Show title:
        TitleView.render(stdscr, title)

        # Show current time:
        if x_max > 2*len(title) + 6:
            CurrentTimeView.render(stdscr)

        # Show weather:
        if len(weather.forcast) < x_max - len(title):
            WeatherView.render(stdscr, weather)


class FooterView:
    @staticmethod
    def render(stdscr, y_max, info):
        '''Display the footer with keybinding'''
        if not cf.SHOW_KEYBINDINGS: return
        display_line(stdscr, y_max - 1, 0, info, 3)


class DaysNameView:
    @staticmethod
    def render(stdscr, x_max):
        '''Display day name depending on the screen available and with right style'''
        if not cf.SHOW_DAY_NAMES: return

        num = 2 if x_max < 80 else 10
        x_cell = int(x_max//7)
        # Depending on which day is the start of the week, weekends are shifted:
        for i in range(7):
            shift = cf.START_WEEK_DAY-1
            day_number = i + shift - 7*((i+shift) > 6)
            name = calendar.day_name[day_number][:num].upper()
            if day_number + 1 not in cf.WEEKEND_DAYS:
                display_line(stdscr, 1, i*x_cell, name, 1, cf.BOLD_DAY_NAMES, cf.UNDERLINED_DAY_NAMES)
            else:
                display_line(stdscr, 1, i*x_cell, name, 6, cf.BOLD_WEEKEND_NAMES, cf.UNDERLINED_WEEKEND_NAMES)


##################### SCREENS ################################




class DailyScreenView:
    @staticmethod
    def render(stdscr, screen, weather, user_events, holidays, birthdays):
        '''Daily view showing events of the day'''
        stdscr.clear()
        if screen.x_max < 6 or screen.y_max < 3: return
        fill_background(stdscr)
        curses.halfdelay(255)

        # Form a string with month, year, and day with today icon:
        icon = cf.TODAY_ICON if screen.date == datetime.date.today() else ''
        month_string = str(calendar.month_name[screen.month].upper())
        date_string = (f'{month_string} {screen.day}, {screen.year} {icon}')

        # Display header and footer:
        HeaderView.render(stdscr, date_string, weather, screen.x_max)
        FooterView.render(stdscr, screen.y_max, CALENDAR_HINT)

        # Display the events:
        daily_view = DailyView(user_events, holidays, birthdays, screen)
        daily_view.render(stdscr, 2, 0, screen, screen.y_max-4, screen.x_max)


class MonthlyScreenView:
    @staticmethod
    def render(stdscr, screen, weather, user_events, holidays, birthdays):
        '''Monthly view showing events of the month'''
        stdscr.clear()
        if screen.x_max < 6 or screen.y_max < 3: return
        curses.halfdelay(255)
        fill_background(stdscr)

        y_cell = (screen.y_max-2)//6
        x_cell = screen.x_max//7

        # Info about the month:
        month_year_string = calendar.month_name[screen.month].upper() + " " + str(screen.year)
        dates = calendar.Calendar(firstweekday=cf.START_WEEK_DAY-1).monthdayscalendar(screen.year, screen.month)

        # Displaying header and footer:
        HeaderView.render(stdscr, month_year_string, weather, screen.x_max)
        DaysNameView.render(stdscr, screen.x_max)
        FooterView.render(stdscr, screen.y_max, CALENDAR_HINT)

        # Displaying the dates and events:
        day_number = 0
        event_number = 0
        for row, week in enumerate(dates):
            for col, day in enumerate(week):
                if day != 0:
                    # Display dates of the month with proper styles:
                    day_in_week = col+(cf.START_WEEK_DAY-1) - 7*((col+(cf.START_WEEK_DAY-1)) > 6)
                    DayNumberView.render(stdscr, 2+row*y_cell, col*x_cell, screen, day, day_in_week, x_cell)

                    # Display the events:
                    screen.day = day
                    daily_view = DailyView(user_events, holidays, birthdays, screen)
                    daily_view.render(stdscr, 3+row*y_cell, col*x_cell, screen, y_cell, x_cell)

class JournalScreenView:
    def __init__(self):
        self.refresh_time = 255
        self.refresh_now = True

    def calculate_refresh_rate(self, user_tasks):
        '''Check if a timer is running and change the refresh rate'''
        for task in user_tasks.items:
            if task.timer.is_counting:
                self.refresh_time = cf.REFRESH_INTERVAL*10
                self.refresh_now = False
                break

    def render(self, stdscr, weather, user_tasks, screen):
        '''Journal view showing all tasks'''
        if self.refresh_now: stdscr.clear()
        if screen.x_max < 6 or screen.y_max < 3: return
        fill_background(stdscr)

        # Check if any of the timers is counting, and increase the update time:
        self.calculate_refresh_rate(user_tasks)
        curses.halfdelay(self.refresh_time)

        # Display header and footer:
        HeaderView.render(stdscr, cf.JOURNAL_HEADER, weather, screen.x_max)
        FooterView.render(stdscr, screen.y_max, TODO_HINT)

        # Display the tasks:
        journal_view = JournalView(user_tasks)
        journal_view.render(stdscr, 2, 1, screen)


class HelpScreenView:
    '''Help screen displaying information about keybindings'''
    def __init__(self):
        self.global_shift_x = 0
        self.global_shift_y = 0
        self.shift_x = 0
        self.shift_y = 0

    def calculate_shift(self, screen):
        '''Depending on the screen space calculate the best position'''
        if screen.x_max < 102:
            self.global_shift_x = 0
            self.shift_x = 0
            self.shift_y = 6 + len(KEYS_GENERAL) + len(KEYS_CALENDAR)
        else:
            self.global_shift_x = (screen.x_max - 102)//2
            self.shift_x = 45
            self.shift_y = 2

        if screen.y_max > 20 and screen.x_max >= 102:
            self.global_shift_y = (screen.y_max - 20)//2
        else:
            self.global_shift_y = 0

    def render(self, stdscr, screen):
        '''Draw the help screen'''
        if screen.x_max < 6 or screen.y_max < 3: return
        stdscr.clear()
        fill_background(stdscr)

        # Depending on the available screen size, adopt the layout:
        self.calculate_shift(screen)

        # Left column:
        display_line(stdscr,self.global_shift_y,self.global_shift_x + 1, MSG_NAME[:screen.x_max-3], 6, cf.BOLD_TITLE, cf.UNDERLINED_TITLE)
        display_line(stdscr,self.global_shift_y + 2,self.global_shift_x + 8,
                TITLE_KEYS_GENERAL[:screen.x_max-3], 4, cf.BOLD_TITLE, cf.UNDERLINED_TITLE)
        for index, key in enumerate(KEYS_GENERAL):
            line = str(key+" "+KEYS_GENERAL[key])[:screen.x_max-3]
            display_line(stdscr,self.global_shift_y + index + 3,self.global_shift_x, line, 5)

        display_line(stdscr,self.global_shift_y + 4+len(KEYS_GENERAL),self.global_shift_x + 8,
                TITLE_KEYS_CALENDAR[:screen.x_max-3], 4, cf.BOLD_TITLE, cf.UNDERLINED_TITLE)
        for index, key in enumerate(KEYS_CALENDAR):
            line = str(key+" "+KEYS_CALENDAR[key])[:screen.x_max-3]
            display_line(stdscr,self.global_shift_y + index + 5 + len(KEYS_GENERAL), self.global_shift_x, line, 5)

        # Right column:
        d_x = self.global_shift_x + self.shift_x
        d_y = self.global_shift_y + self.shift_y
        display_line(stdscr, d_y, d_x + 8, TITLE_KEYS_JOURNAL[:screen.x_max-3], 4, cf.BOLD_TITLE, cf.UNDERLINED_TITLE)
        for index, key in enumerate(KEYS_TODO):
            line = str(key + " " + KEYS_TODO[key])[:screen.x_max-3]
            display_line(stdscr, d_y + index + 1, d_x, line, 5)

        # Additional info:
        d_x = self.global_shift_x + self.shift_x + 8
        d_y = self.global_shift_y + len(KEYS_TODO) + self.shift_y
        display_line(stdscr, d_y + 2, d_x, MSG_VIM, 6)
        display_line(stdscr, d_y + 4, d_x, MSG_INFO, 5)
        display_line(stdscr, d_y + 5, d_x, MSG_SITE, 4)


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

        # Monthly screen:
        if screen.state == 'calendar':
            while screen.state == 'calendar':
                MonthlyScreenView.render(stdscr, screen, weather, user_events, holidays, birthdays)
                control_monthly_screen(stdscr, screen, user_events)
                if user_events.changed:
                    UserEventsSaver.save_to_file(user_events, cf.EVENTS_FILE)
                    user_events = UserEventsLoader.load_from_file(cf.EVENTS_FILE)

        # Daily screen:
        elif screen.state == 'daily_calendar':
            while screen.state == 'daily_calendar':
                DailyScreenView.render(stdscr, screen, weather, user_events, holidays, birthdays)
                control_daily_screen(stdscr, screen, user_events)
                if user_events.changed:
                    UserEventsSaver.save_to_file(user_events, cf.EVENTS_FILE)
                    user_events = UserEventsLoader.load_from_file(cf.EVENTS_FILE)

        # Journal screen:
        elif screen.state == 'journal':
            journal_screen_view = JournalScreenView()
            while screen.state == 'journal':
                journal_screen_view.render(stdscr, weather, user_tasks, screen)
                control_journal_screen(stdscr, user_tasks, screen)
                if user_tasks.changed:
                    UserTasksSaver.save_to_file(user_tasks, cf.TASKS_FILE)
                    user_tasks = UserTasksLoader.load_from_file(cf.TASKS_FILE)

        # Help screen:
        elif screen.state == 'help':
            help_screen_view = HelpScreenView()
            while screen.state == 'help':
                help_screen_view.render(stdscr, screen)
                control_help_screen(stdscr, screen)

        else:
            break

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
