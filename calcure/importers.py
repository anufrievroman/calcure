"""Module that provides methods to import data from other programs"""
import logging

from calcure.data import *
from calcure.calendars import convert_to_persian_date


class Importer:
    """Import tasks and events from files of other programs"""

    def __init__(self, user_tasks, user_events, cf):
        self.user_tasks = user_tasks
        self.user_events = user_events
        self.tasks_file = cf.TASKS_FILE
        self.events_file = cf.EVENTS_FILE
        self.calcurse_todo_file = cf.CALCURSE_TODO_FILE
        self.calcurse_events_file = cf.CALCURSE_EVENTS_FILE
        self.taskwarrior_folder = cf.TASKWARRIOR_FOLDER
        self.use_persian_calendar = cf.USE_PERSIAN_CALENDAR

    def read_file(self, filename):
        """Try to read a file and return its lines"""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
            return lines
        except (IOError, FileNotFoundError, NameError):
            logging.error("Problem occured acessing %s.", filename)
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
                is_private = False
                timer = Timer([])
                self.user_tasks.add_item(Task(task_id, name, status, timer, is_private))

    def import_tasks_from_taskwarrior(self):
        """Import tasks from taskwarrior database"""
        lines = self.read_file(self.taskwarrior_folder+"/pending.data")
        for line in lines:
            if len(line) > 0:
                name = line.split('description:"', 1)[1]
                name = name.split('"', 1)[0]
                if not self.user_tasks.item_exists(name):
                    task_id = self.user_tasks.generate_id()
                    is_private = False
                    timer = Timer([])
                    status = Status.NORMAL
                    self.user_tasks.add_item(Task(task_id, name, status, timer, is_private))

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
            is_private = False

            # Convert to persian date if needed:
            if self.use_persian_calendar:
                year, month, day = convert_to_persian_date(year, month, day)

            imported_event = UserEvent(event_id, year, month, day, name, 1,
                                       Frequency.ONCE, Status.NORMAL, is_private)
            if not self.user_events.event_exists(imported_event):
                self.user_events.add_item(imported_event)
