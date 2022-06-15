"""Module that controls import and export of the user data"""

import configparser
import pathlib
import csv
import os

import datetime
import jdatetime

from calcure.data import *


def convert_to_persian_date(year, month, day):
    """Convert date from Gregorian to Persian calendar"""
    persian_date =  jdatetime.date.fromgregorian(day=day, month=month, year=year)
    day = persian_date.day
    month = persian_date.month
    year = persian_date.year
    return year, month, day


def convert_to_gregorian_date(year, month, day):
    """Convert date from Persian to Gregorian calendar"""
    gregorian_date = jdatetime.date(year, month, day).togregorian()
    day = gregorian_date.day
    month = gregorian_date.month
    year = gregorian_date.year
    return year, month, day


class FileRepository:
    """Load and save events and tasks to files"""

    def __init__(self, tasks_file, events_file, country, use_persian_calendar):
        self.user_tasks = Tasks()
        self.user_events = Events()
        self.holidays = Events()
        self.birthdays = Birthdays()
        self.abook_file = str(pathlib.Path.home())+"/.abook/addressbook"
        self.tasks_file = tasks_file
        self.events_file = events_file
        self.country = country
        self.use_persian_calendar = use_persian_calendar

    @property
    def is_task_format_old(self):
        """Check if the database format is old"""
        with open(self.tasks_file, "r", encoding="utf-8") as f:
            text = f.read()
        return text[0] == '"'

    def read_or_create_file(self, file):
        """Read user's csv file or create new one if it does not exist"""
        # Try to read the file line by line:
        try:
            with open(file, "r", encoding="utf-8") as f:
                read_lines = csv.reader(f, delimiter = ',')
                return list(read_lines)

        # Create file if it does not exist:
        except IOError:
            try:
                with open(file, "w+", encoding="utf-8") as f:
                    pass
                return []
            # Pass if there was a problem with file system:
            except (FileNotFoundError, NameError):
                return []

    def load_tasks_from_csv(self):
        """Reads from user's file or create new one if it does not exist"""
        lines = self.read_or_create_file(self.tasks_file)

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
                privacy = True
            else:
                name = row[0 + shift]
                privacy = False
            status = Status[row[1 + shift].upper()]
            stamps = row[(2 + shift):] if len(row) > 2 else []
            self.user_tasks.add_item(Task(task_id, name, status, Timer(stamps), privacy, year, month, day))
        return self.user_tasks

    def load_events_from_csv(self):
        """Reads from user's file or create it if it does not exist"""
        lines = self.read_or_create_file(self.events_file)
        for index, row in enumerate(lines):
            event_id = index
            year = int(row[1])
            month = int(row[2])
            day = int(row[3])
            if row[4][0] == '.':
                name = row[4][1:]
                privacy = True
            else:
                name = row[4]
                privacy = False

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

            self.user_events.add_item(UserEvent(event_id, year, month, day,
                                name, repetition, frequency, status, privacy))
        return self.user_events

    def save_tasks_to_csv(self):
        """Rewrite the data file with changed tasks"""
        original_file = self.tasks_file
        dummy_file = self.tasks_file + '.bak'
        with open(dummy_file, "w", encoding="utf-8") as f:
            for task in self.user_tasks.items:
                dot = "."

                # If persian calendar was used, we convert event back to Gregorian for storage:
                if self.use_persian_calendar and task.year != 0:
                    year, month, day = convert_to_gregorian_date(task.year, task.month, task.day)
                else:
                    year, month, day = task.year, task.month, task.day

                f.write(f'{year},{month},{day},"{dot*task.privacy}{task.name}",{task.status.name.lower()}')
                for stamp in task.timer.stamps:
                    f.write(f',{str(stamp)}')
                f.write("\n")
        os.remove(original_file)
        os.rename(dummy_file, original_file)
        self.user_tasks.changed = False

    def save_events_to_csv(self):
        """Rewrite the data file with changed events"""
        original_file = self.events_file
        dummy_file = self.events_file + '.bak'
        with open(dummy_file, "w", encoding="utf-8") as f:
            for ev in self.user_events.items:

                # If persian calendar was used, we convert event back to Gregorian for storage:
                if self.use_persian_calendar:
                    year, month, day = convert_to_gregorian_date(ev.year, ev.month, ev.day)
                else:
                    year, month, day = ev.year, ev. month, ev.day

                name = f'{"."*ev.privacy}{ev.name}'
                f.write(f'{ev.item_id},{year},{month},{day},"{name}",{ev.repetition},{ev.frequency.name.lower()},{ev.status.name.lower()}\n')
        os.remove(original_file)
        os.rename(dummy_file, original_file)
        self.user_events.changed = False

    def load_deadlines(self):
        """Create collection of events that are deadlines for tasks"""
        for task in self.user_tasks.items:
            self.deadlines.add_item(DeadlineEvent(task.item_id, task.year, task.month, task.day, task.name, task.status, task.privacy))
        return self.deadlines

    def load_holidays(self):
        """Load list of holidays in this country around this year"""
        try:
            import holidays as hl
            year = datetime.date.today().year
            holiday_events = eval("hl."+self.country+"(years=[year-1, year, year+3])")
            for date, name in holiday_events.items():

                # Convert to persian date if needed:
                if self.use_persian_calendar:
                    year, month, day = convert_to_persian_date(date.year, date.month, date.day)
                else:
                    year, month, day = date.year, date.month, date.day

                self.holidays.add_item(Event(year, month, day, name))
        except (ModuleNotFoundError, SyntaxError, AttributeError):
            pass
        return self.holidays

    def load_birthdays_from_abook(self):
        """Loading birthdays from abook contacts"""
        abook = configparser.ConfigParser()
        abook.read(self.abook_file)
        for each_contact in abook.sections():
            for key, _ in abook.items(each_contact):
                if key == "birthday":
                    month = int(abook[each_contact]["birthday"][-5:-3])
                    day = int(abook[each_contact]["birthday"][-2:])
                    name = abook[each_contact]["name"]

                    # Convert to persian date if needed:
                    if self.use_persian_calendar:
                        _, month, day = convert_to_persian_date(1000, month, day)

                    self.birthdays.add_item(Event(1, month, day, name))
        return self.birthdays


class Importer:
    """Import tasks and events from files of other programs"""
    def __init__(self, user_tasks, user_events, tasks_file, events_file, calcurse_todo_file,
                            calcurse_events_file, taskwarrior_folder, use_persian_calendar):
        self.user_tasks = user_tasks
        self.user_events = user_events
        self.tasks_file = tasks_file
        self.events_file = events_file
        self.calcurse_todo_file = calcurse_todo_file
        self.calcurse_events_file = calcurse_events_file
        self.taskwarrior_folder = taskwarrior_folder
        self.use_persian_calendar = use_persian_calendar

    def read_file(self, file):
        """Try to read a file and return its lines"""
        try:
            with open(file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            return lines
        except (IOError, FileNotFoundError, NameError):
            return []

    def import_tasks_from_calcurse(self):
        """Import tasks from calcurse database"""
        lines = self.read_file(self.calcurse_todo_file)
        for line in lines:
            name = line[4:-1]
            importance = line[1]
            if (len(name) > 0) and not self.user_tasks.item_exists(name):
                if importance in ['1', '2']:
                    status = Status.IMPORTANT
                elif importance in ['8', '9', '10']:
                    status = Status.UNIMPORTANT
                else:
                    status = Status.NORMAL
                task_id = self.user_tasks.generate_id()
                privacy = False
                self.user_tasks.add_item(Task(task_id, name, status, Timer([]), privacy))

    def import_tasks_from_taskwarrior(self):
        """Import tasks from taskwarrior database"""
        lines = self.read_file(self.taskwarrior_folder+"/pending.data")
        for line in lines:
            if len(line) > 0:
                name = line.split('description:"', 1)[1]
                name = name.split('"', 1)[0]
                if not self.user_tasks.item_exists(name):
                    task_id = self.user_tasks.generate_id()
                    privacy = False
                    self.user_tasks.add_item(Task(task_id, name, Status.NORMAL, Timer([]), privacy))

    def import_events_from_calcurse(self):
        """Importing events from calcurse apt file into our events file"""
        lines = self.read_file(self.calcurse_events_file)
        for line in lines:
            month = int(line[0:2])
            day = int(line[3:5])
            year = int(line[6:10])
            if line[11] == "[":
                name = line[15:-1]
            elif line[11] == "@":
                name = line[35:-1]
                name = name.replace('|',' ')
            else:
                name = ''
            if not self.user_events.items:
                event_id = 0
            else:
                event_id = self.user_events.items[-1].item_id + 1
            privacy = False

            # Convert to persian date if needed:
            if self.use_persian_calendar:
                year, month, day = convert_to_persian_date(year, month, day)

            imported_event = UserEvent(event_id, year, month, day, name, 1,
                                       Frequency.ONCE, Status.NORMAL, privacy)
            if not self.user_events.event_exists(imported_event):
                self.user_events.add_item(imported_event)
