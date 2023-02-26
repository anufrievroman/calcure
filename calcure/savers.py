"""Module that controls saving data files"""

import os

from calcure.data import *
from calcure.calendars import convert_to_persian_date, convert_to_gregorian_date


class TaskSaverCSV:
    """Save tasks into CSV files"""

    def __init__(self, user_tasks, cf):
        self.user_tasks = user_tasks
        self.tasks_file = cf.TASKS_FILE
        self.use_persian_calendar = cf.USE_PERSIAN_CALENDAR

    def save(self):
        """Rewrite CSV file with changed tasks"""
        original_file = self.tasks_file
        dummy_file = self.tasks_file + '.bak'
        with open(dummy_file, "w", encoding="utf-8") as f:
            for task in self.user_tasks.items:

                # If persian calendar was used, we convert event back to Gregorian for storage:
                if self.use_persian_calendar and task.year != 0:
                    year, month, day = convert_to_gregorian_date(task.year, task.month, task.day)
                else:
                    year, month, day = task.year, task.month, task.day

                dot = "."
                f.write(f'{year},{month},{day},"{dot*task.privacy}{task.name}",{task.status.name.lower()}')
                for stamp in task.timer.stamps:
                    f.write(f',{str(stamp)}')
                f.write("\n")
        os.remove(original_file)
        os.rename(dummy_file, original_file)
        self.user_tasks.changed = False


class EventSaverCSV:
    """Save events into CSV files"""

    def __init__(self, user_events, cf):
        self.user_events = user_events
        self.events_file = cf.EVENTS_FILE
        self.use_persian_calendar = cf.USE_PERSIAN_CALENDAR

    def save(self):
        """Rewrite the data file with changed events"""
        original_file = self.events_file
        dummy_file = self.events_file + '.bak'
        with open(dummy_file, "w", encoding="utf-8") as file:
            for ev in self.user_events.items:

                # If persian calendar was used, we convert event back to Gregorian for storage:
                if self.use_persian_calendar:
                    year, month, day = convert_to_gregorian_date(ev.year, ev.month, ev.day)
                else:
                    year, month, day = ev.year, ev. month, ev.day

                name = f'{"."*ev.privacy}{ev.name}'
                file.write(f'{ev.item_id},{year},{month},{day},"{name}",{ev.repetition},{ev.frequency.name.lower()},{ev.status.name.lower()}\n')
        os.remove(original_file)
        os.rename(dummy_file, original_file)
        self.user_events.changed = False
