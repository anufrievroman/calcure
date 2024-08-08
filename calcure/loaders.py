"""Module that controls loading data from files and libraries"""

import configparser
import csv
import os
import datetime
import icalendar
import urllib.request
import io
import logging

from pathlib import Path

from calcure.data import *
from calcure.calendars import convert_to_persian_date


class LoaderCSV:
    """Load data from CSV files"""

    def create_file(self, filename):
        """Create CSV file"""
        try:
            with open(filename, "w+", encoding="utf-8") as file:
                pass
            return []
        except (FileNotFoundError, NameError) as e_message:
            logging.error("Problem occured trying to create %s. %s", filename, e_message)
            return []

    def read_file(self, filename):
        """Read CSV file or create new one if it does not exist"""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = csv.reader(file, delimiter = ',')
                return list(lines)
        except IOError: # File does not exist
            # logging.info("Creating %s.", filename)
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

        self.user_tasks.delete_all_items()
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
        self.user_tasks.changed = False
        return self.user_tasks


class EventLoaderCSV(LoaderCSV):
    """Load events from CSV files"""

    def __init__(self, cf):
        self.user_events = Events()
        self.events_file = cf.EVENTS_FILE
        self.use_persian_calendar = cf.USE_PERSIAN_CALENDAR

    def load(self):
        """Read from CSV file"""
        self.user_events.delete_all_items()
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
        self.user_events.changed = False
        return self.user_events


class HolidayLoader:
    """Load holidays for this country around this year"""

    def __init__(self, cf):
        self.holidays = Events()
        self.countries = cf.HOLIDAY_COUNTRY.split(',')
        self.use_persian_calendar = cf.USE_PERSIAN_CALENDAR

    def load(self):
        """Run and collect holidays for each country"""
        holidays = Events()
        for country in self.countries:
            self.load_country(country)
        return self.holidays

    def load_country(self, country):
        """Load list of holidays from 'holidays' module"""

        def get_country_and_subdivision(country):
            """Get country and subdivision, where encoded."""
            if ":" in country:
                return tuple(country.split(":"))
            else:
                return (country, None)

        try:
            import holidays as hl
            from holidays import registry

            (country, subdivision) = get_country_and_subdivision(country)
            country_codes = {x[0]: x[2] for x in registry.COUNTRIES.values()}
            country_code = country_codes.get(country)
            year = datetime.date.today().year
            holiday_events = (getattr(hl, country))(subdiv=subdivision, years=[year+x for x in range(-2, 5)])
            for date, name in holiday_events.items():

                # Convert to persian date if needed:
                if self.use_persian_calendar:
                    year, month, day = convert_to_persian_date(date.year, date.month, date.day)
                else:
                    year, month, day = date.year, date.month, date.day

                # Add holiday:
                holiday = Event(year, month, day, f'{name} ({country_code})' if len(self.countries) > 1 else name)
                self.holidays.add_item(holiday)

        except ModuleNotFoundError:
            logging.error("Couldn't load holidays. Module holidays is not installed. Try 'pip install holidays'")
            pass
        except (SyntaxError, AttributeError) as e_message:
            logging.error("Couldn't load holidays. Country might be incorrect. %s", e_message)
            pass
        return self.holidays


class BirthdayLoader:
    """Load birthdays of contacts"""

    def __init__(self, cf):
        self.birthdays = Birthdays()
        self.abook_file = Path.home() / ".abook" / "addressbook"
        self.use_persian_calendar = cf.USE_PERSIAN_CALENDAR
        self.load_birthdays = cf.BIRTHDAYS_FROM_ABOOK

    def load(self):
        """Loading birthdays from abook contacts"""

        # Quit if birthdays do not need to be loaded:
        if not self.load_birthdays:
            return self.birthdays

        # Quit if file does not exists:
        if not self.abook_file.exists():
            logging.warning("Couldn't load birthdays. File. %s does not exist.", str(self.abook_file))
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
        already_has_prodid = False
        text = io.StringIO()
        for line in file:
            # If there is more than one PRODID line or a TZUNTIL line, skip them:
            if ((not (already_has_prodid and "PRODID:" in line)) and
                (not "TZUNTIL" in line)):
                text.write(line)

            if "PRODID:" in line:
                already_has_prodid = True
        return text.getvalue()

    def read_file(self, path):
        """Parse an ics file if it exists"""
        if not os.path.exists(path):
            logging.error("Failed to load %s because file does not exist.", path)
            return ""
        with open(path, 'r', encoding="utf-8") as file:
            return self.read_lines(file)

    def read_url(self, path):
        """Parse an ics URL if it exists and networks works"""
        try:
            with urllib.request.urlopen(path) as response:
                file = io.TextIOWrapper(response, 'utf-8')
                return self.read_lines(file)
        except urllib.error.HTTPError as e_message:
            logging.error("Failed to load from %s. Probably url is wrong. %s", path, e_message)
            return ""
        except urllib.error.URLError as e_message:
            logging.error("Failed to load from %s. Probably no internet connection. %s", path, e_message)
            return ""

    def read_resource(self, path):
        """Determine type of the resource, parse it, and return list of strings for each file"""
        ics_files = []
        path = os.path.expanduser(path)

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

                # `path` may contain files with metadata, e.g. `color` and
                # `displayname`. For now, exclude those while loading.
                if file_path.endswith('.ics'):
                    ics_files.append(self.read_file(file_path))

        return ics_files


class TaskLoaderICS(LoaderICS):
    """Load tasks from ICS files"""

    def __init__(self, cf):
        self.user_ics_tasks = Tasks()
        self.ics_task_files = cf.ICS_TASK_FILES
        self.use_persian_calendar = cf.USE_PERSIAN_CALENDAR

    def parse_task(self, component, calendar_number):
        """Parse single task and add it to the user_ics_tasks"""
        task_status = component.get('status')

        if task_status == "CANCELLED":
            return

        task_priority = component.get('priority')
        task_name = str(component.get('summary'))
        task_id = self.user_ics_tasks.generate_id()

        # Assign status from priority:
        status = Status.NORMAL
        if task_priority is not None:
            if task_priority > 5:
                status = Status.UNIMPORTANT
            if task_priority < 5:
                status = Status.IMPORTANT

        # Correct according to status:
        if task_status == "COMPLETED":
            status = Status.DONE

        # Try reading task due date:
        due_dt = None
        try:
            due_dt = component.get('due').dt
            year, month, day = due_dt.year, due_dt.month, due_dt.day
        except AttributeError:
            year, month, day = 0, 0, 0

        timer = Timer([])
        is_private = False

        # Add task:
        new_task = Task(task_id, task_name, status, timer, is_private,
                        year, month, day, calendar_number)
        self.user_ics_tasks.add_item(new_task)


    def load(self):
        """Load tasks from each of the ics files"""

        # Quit if the files are not specified in config:
        if self.ics_task_files is None:
            return self.user_ics_tasks

        self.user_ics_tasks.delete_all_items()
        for calendar_number, filename in enumerate(self.ics_task_files):
            # For each resource from config, load a list that has one or more ics files:
            ics_files = self.read_resource(filename)
            for ics_file in ics_files:
                try:
                    cal = icalendar.Calendar.from_ical(ics_file)
                    for component in cal.walk():
                        if component.name == 'VTODO':
                            self.parse_task(component, calendar_number)
                except Exception as e_message:
                    logging.error("Failed to parse %s. %s", filename, e_message)

        return self.user_ics_tasks


class EventLoaderICS(LoaderICS):
    """Load events from ICS files"""

    def __init__(self, cf):
        self.user_ics_events = Events()
        self.ics_event_files = cf.ICS_EVENT_FILES
        self.use_persian_calendar = cf.USE_PERSIAN_CALENDAR
        self.local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

    def parse_event(self, component, index, calendar_number):
        """Parse single event and add it to user_ics_events"""

        # Default parameters:
        hour = None
        minute = None
        event_id = index
        repetition = 1
        frequency = Frequency.ONCE
        status = Status.NORMAL
        is_private = False
        rrule = None
        exdate = None

        # Parameters of the event from ics file, if they exist:
        name = str(component.get('summary', ''))
        dt = None
        try:
            dt = component.get('dtstart').dt

            # Convert to local timezone if it's provided:
            if hasattr(dt, "tzinfo"):
                dt = dt.astimezone(self.local_timezone)

            year, month, day = dt.year, dt.month, dt.day
        except AttributeError:
            year, month, day = 0, 1, 1

        # See if this event takes multiple days:
        try:
            dt_end = component.get('dtend').dt

            # Convert to local timezone if it's provided:
            if hasattr(dt_end, "tzinfo"):
                dt_end = dt_end.astimezone(self.local_timezone)

            # For events with time:
            try:
                dt_difference = dt_end.date() - dt.date()
                if dt_difference.days > 0:
                    repetition = dt_difference.days + 1
                    frequency = Frequency.DAILY

            # For all day events, last day does not count:
            except:
                dt_difference = dt_end - dt
                if dt_difference.days > 0:
                    repetition = dt_difference.days
                    frequency = Frequency.DAILY
            
            # Parsing recuring rules:
            if 'rrule' in component:
                rrule = component.get('rrule').to_ical().decode('utf-8')
                exdate = component.get('exdate')
                repetition = 0

        except AttributeError:
            logging.error("Failed to parse event %s on %s.", name, dt)
            pass

        # Add start time to non-all-day events:
        all_day = component.get('dtstart').params.get('VALUE') == 'DATE' if component.get('dtstart') else False
        if not all_day:
            hour = dt.hour if dt else 0
            minute = dt.minute if dt else 0

        # Convert to persian date if needed:
        if self.use_persian_calendar:
            year, month, day = convert_to_persian_date(year, month, day)

        # Add event:
        new_event = UserEvent(event_id, year, month, day, name, repetition, frequency,
                              status, is_private, calendar_number, hour, minute, rrule, exdate)
        self.user_ics_events.add_item(new_event)

    def load(self):
        """Load events from each of the ics files"""

        # Quit if the files are not specified in config:
        if self.ics_event_files is None:
            return self.user_ics_events

        self.user_ics_events.delete_all_items()
        for calendar_number, filename in enumerate(self.ics_event_files):

            # For each resource from config, load a list that has one or more ics files:
            ics_files = self.read_resource(filename)
            for ics_file in ics_files:
                try:
                    cal = icalendar.Calendar.from_ical(ics_file)
                    index = 0
                    for component in cal.walk():
                        if component.name == 'VEVENT':
                            index += 1
                            self.parse_event(component, index, calendar_number)

                except Exception as e_message:
                    logging.error("Failed to parse %s. %s", filename, e_message)
        return self.user_ics_events
