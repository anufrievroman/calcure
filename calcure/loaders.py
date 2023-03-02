"""Module that controls loading data from files and libraries"""

import configparser
import pathlib
import csv
import os
import datetime
import ics
import urllib.request
import io
import logging

from calcure.data import *
from calcure.calendars import convert_to_persian_date, convert_to_gregorian_date


class LoaderCSV:
    """Load data from CSV files"""

    def create_file(self, filename):
        """Create CSV file"""
        try:
            with open(filename, "w+", encoding="utf-8") as file:
                pass
            return []
        except (FileNotFoundError, NameError):
            logging.error("Problem occured trying to create %s.", filename)
            return []

    def read_file(self, filename):
        """Read CSV file or create new one if it does not exist"""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = csv.reader(file, delimiter = ',')
                return list(lines)
        except IOError: # File does not exist
            logging.info("Creating %s.", filename)
            return self.create_file(filename)


class TaskLoaderCSV(LoaderCSV):
    """Load tasks from CSV files"""

    def __init__(self, cf):
        self.user_tasks = Tasks()
        self.tasks_file = cf.TASKS_FILE
        self.use_persian_calendar = cf.USE_PERSIAN_CALENDAR

    @property
    def is_task_format_old(self):
        """Check if the database format is old"""
        with open(self.tasks_file, "r", encoding="utf-8") as f:
            text = f.read()
        return text[0] == '"'

    def load(self):
        """Reads from CSV file"""
        lines = self.read_file(self.tasks_file)

        for index, row in enumerate(lines):
            task_id = index

            # Read task dates:
            if self.is_task_format_old:
                shift = 0
                year = 0
                month = 0
                day = 0
            else:
                shift = 3
                year = int(row[0])
                month = int(row[1])
                day = int(row[2])

            # Convert to persian date if needed and if it is not zero date:
            if self.use_persian_calendar and year != 0:
                year, month, day = convert_to_persian_date(year, month, day)

            # Read task name and statuses:
            if row[0 + shift][0] == '.':
                name = row[0 + shift][1:]
                is_private = True
            else:
                name = row[0 + shift]
                is_private = False
            status = Status[row[1 + shift].upper()]
            stamps = row[(2 + shift):] if len(row) > 2 else []
            timer = Timer(stamps)

            # Add task:
            new_task = Task(task_id, name, status, timer, is_private, year, month, day)
            self.user_tasks.add_item(new_task)
        return self.user_tasks


class EventLoaderCSV(LoaderCSV):
    """Load events from CSV files"""

    def __init__(self, cf):
        self.user_events = Events()
        self.events_file = cf.EVENTS_FILE
        self.use_persian_calendar = cf.USE_PERSIAN_CALENDAR

    def load(self):
        """Read from CSV file"""
        lines = self.read_file(self.events_file)
        for index, row in enumerate(lines):
            event_id = index
            year = int(row[1])
            month = int(row[2])
            day = int(row[3])
            if row[4][0] == '.':
                name = row[4][1:]
                is_private = True
            else:
                name = row[4]
                is_private = False

            # Account for old versions of the datafile:
            if len(row) > 5:
                repetition = int(row[5])
                if row[6] == 'd':
                    frequency = Frequency.DAILY
                elif row[6] == 'w':
                    frequency = Frequency.WEEKLY
                elif row[6] == 'm':
                    frequency = Frequency.MONTHLY
                elif row[6] == 'y':
                    frequency = Frequency.YEARLY
                else:
                    try:
                        frequency = Frequency[row[6].upper()]
                    except (ValueError, KeyError):
                        frequency = Frequency.ONCE
            else:
                repetition = '1'
                frequency = Frequency.ONCE
            if len(row) > 7:
                status = Status[row[7].upper()]
            else:
                status = Status.NORMAL

            # Convert to persian date if needed:
            if self.use_persian_calendar:
                year, month, day = convert_to_persian_date(year, month, day)

            # Add event:
            new_event = UserEvent(event_id, year, month, day, name, repetition, frequency, status, is_private)
            self.user_events.add_item(new_event)
        return self.user_events


class HolidayLoader:
    """Load holidays for this country around this year"""

    def __init__(self, cf):
        self.holidays = Events()
        self.country = cf.HOLIDAY_COUNTRY
        self.use_persian_calendar = cf.USE_PERSIAN_CALENDAR

    def load(self):
        """Load list of holidays from 'holidays' module"""
        try:
            import holidays as hl
            year = datetime.date.today().year
            holiday_events = eval("hl."+self.country+"(years=[year-2, year-1, year, year+1, year+2, year+3, year+4])")
            for date, name in holiday_events.items():

                # Convert to persian date if needed:
                if self.use_persian_calendar:
                    year, month, day = convert_to_persian_date(date.year, date.month, date.day)
                else:
                    year, month, day = date.year, date.month, date.day

                # Add holiday:
                holiday = Event(year, month, day, name)
                self.holidays.add_item(holiday)

        except ModuleNotFoundError:
            logging.error("Couldn't load holidays. Module holydays is not installed.")
            pass
        except (SyntaxError, AttributeError):
            logging.error("Couldn't load holidays. Country might be incorrect.")
            pass
        return self.holidays


class BirthdayLoader:
    """Load birthdays of contacts"""

    def __init__(self, cf):
        self.birthdays = Birthdays()
        self.abook_file = str(pathlib.Path.home())+"/.abook/addressbook"
        self.use_persian_calendar = cf.USE_PERSIAN_CALENDAR

    def load(self):
        """Loading birthdays from abook contacts"""

        # Quit if file does not exists:
        if not os.path.exists(self.abook_file):
            return self.birthdays

        abook = configparser.ConfigParser()
        abook.read(self.abook_file)
        for each_contact in abook.sections():
            for key, _ in abook.items(each_contact):
                if key in ["birthday", "anniversary"]:
                    month = int(abook[each_contact][key][-5:-3])
                    day = int(abook[each_contact][key][-2:])
                    name = abook[each_contact]["name"]

                    # Convert to persian date if needed:
                    if self.use_persian_calendar:
                        _, month, day = convert_to_persian_date(1000, month, day)

                    # Add birthday:
                    birthday = Event(1, month, day, name)
                    self.birthdays.add_item(birthday)
        return self.birthdays


class LoaderICS:
    """Load data from ICS files"""

    def read_lines(self, file):
        """Read the file line-by-line and remove multiple PRODID lines"""
        previous_line = ""
        text = ""
        for line in file:
            # If there is more than one PRODID line, skip them:
            if not ("PRODID:" in line and "PRODID:" in previous_line):
                text += line
            previous_line = line
        return text

    def read_file(self, path):
        """Parse an ics file if it exists"""
        if not os.path.exists(path):
            logging.error("Failed to load %s. Probably path is incorrect.", path)
            return ""
        with open(path, 'r', encoding="utf-8") as file:
            return self.read_lines(file)

    def read_url(self, path):
        """Parse an ics URL if it exists and networks works"""
        try:
            with urllib.request.urlopen(path) as response:
                file = io.TextIOWrapper(response, 'utf-8')
                return self.read_lines(file)
        except urllib.error.HTTPError:
            logging.error("Failed to load %s. Probably url is wrong.", path)
            return ""
        except urllib.error.URLError:
            logging.error("Failed to load %s. Probably no internet connection.", path)
            return ""

    def read_resource(self, path):
        """Determine type of the resourse, parse it, and return list of strings for each file"""
        ics_files = []

        # If it's a URL, try to load it:
        if path.startswith('http'):
            ics_files.append(self.read_url(path))
            return ics_files

        # If it's a local file, read it:
        if path.endswith('.ics'):
            ics_files.append(self.read_file(path))
            return ics_files

        # Otherwise, assume it's a folder, and read every file inside:
        for root, directories, files in os.walk(path):
            for filename in files:
                # Get the full path to the file
                file_path = os.path.join(root, filename)
                ics_files.append(self.read_file(file_path))
        return ics_files


class TaskLoaderICS(LoaderICS):
    """Load tasks from ICS files"""

    def __init__(self, cf):
        self.user_ics_tasks = Tasks()
        self.ics_task_files = cf.ICS_TASK_FILES
        self.use_persian_calendar = cf.USE_PERSIAN_CALENDAR

    def load(self):
        """Load tasks from each of the ics files"""

        # Quit if the files are not specified in config:
        if self.ics_task_files is None:
            return self.user_ics_tasks

        for calendar_number, filename in enumerate(self.ics_task_files):

            # For each resourse from config, load a list that has one or more ics files:
            ics_files = self.read_resource(filename)
            for ics_file in ics_files:

                # Try parcing content of the ics file:
                try:
                    cal = ics.Calendar(ics_file)
                except NotImplementedError: # More than one calendar in the file
                    logging.error("Failed to load %s.", filename)
                    return self.user_ics_tasks

                for task in cal.todos:
                    if task.status != "CANCELLED":
                        task_id = self.user_ics_tasks.generate_id()

                        # Assign status from priority:
                        status = Status.NORMAL
                        if task.priority is not None:
                            if task.priority > 5:
                                status = Status.UNIMPORTANT
                            if task.priority < 5:
                                status = Status.IMPORTANT

                        # Correct according to status:
                        if task.status == "COMPLETED":
                            status = Status.DONE

                        name = task.name

                        # Try reading task due date:
                        try:
                            year = task.due.year
                            month = task.due.month
                            day = task.due.day
                        except AttributeError:
                            year, month, day = 0, 0, 0

                        timer = Timer([])
                        is_private = False

                        # Add task:
                        new_task = Task(task_id, name, status, timer, is_private,
                                        year, month, day, calendar_number)
                        self.user_ics_tasks.add_item(new_task)

        return self.user_ics_tasks


class EventLoaderICS(LoaderICS):
    """Load events from ICS files"""

    def __init__(self, cf):
        self.user_ics_events = Events()
        self.ics_event_files = cf.ICS_EVENT_FILES
        self.use_persian_calendar = cf.USE_PERSIAN_CALENDAR

    def load(self):
        """Load events from each of the ics files"""

        # Quit if the files are not specified in config:
        if self.ics_event_files is None:
            return self.user_ics_events

        for calendar_number, filename in enumerate(self.ics_event_files):

            # For each resourse from config, load a list that has one or more ics files:
            ics_files = self.read_resource(filename)
            for ics_file in ics_files:

                # Try parcing content of the ics file:
                try:
                    cal = ics.Calendar(ics_file)
                except NotImplementedError:  # More than one calendar in the file
                    logging.error("Failed to load %s.", filename)
                    return self.user_ics_events

                for index, event in enumerate(cal.events):

                    # Default parameters:
                    event_id = index
                    repetition = '1'
                    frequency = Frequency.ONCE
                    status = Status.NORMAL
                    is_private = False

                    # Parameters of the event from ics if they exist:
                    name = event.name if event.name is not None else ""
                    all_day = event.all_day if event.all_day is not None else True
                    year = event.begin.year if event.begin else 0
                    month = event.begin.month if event.begin else 1
                    day = event.begin.day if event.begin else 1

                    # Add start time to name of non-all-day events:
                    if not all_day:
                        hour = event.begin.hour if event.begin else 0
                        minute = event.begin.minute if event.begin else 0
                        name = f"{hour:0=2}:{minute:0=2} {name}"

                    # Convert to persian date if needed:
                    if self.use_persian_calendar:
                        year, month, day = convert_to_persian_date(year, month, day)

                    # Add event:
                    new_event = UserEvent(event_id, year, month, day, name, repetition,
                                          frequency, status, is_private, calendar_number)
                    self.user_ics_events.add_item(new_event)

        return self.user_ics_events
