import csv
import os
import time
import datetime
import configparser
import pathlib
import subprocess

class Weather():
    '''Information about the weather loaded from wttr.in'''
    def __init__(self, city):
        self.loaded = False
        self.forcast = " "
        self.city = city


######################## ITEMS ###########################


class Task:
    '''Task crated by user'''
    def __init__(self, id, name, status, timer):
        self.id = id
        self.name = name
        self.status = status
        self.timer = timer


class Event:
    '''Parent class of events'''
    def __init__(self, year, month, day, name):
        self.year = year
        self.month = month
        self.day = day
        self.name = name

    @property
    def date(self):
        '''Return date in datetime format'''
        return datetime.date(self.year, self.month, self.day)


class UserEvent(Event):
    '''Events crated by user'''
    def __init__(self, id, year, month, day, name, repetition, frequency, status):
        super().__init__(year, month, day, name)
        self.id = id
        self.repetition = repetition
        self.frequency = frequency
        self.status = status


class Timer:
    '''Timer for a task'''
    def __init__(self, stamps):
        self.stamps = stamps

    @property
    def is_counting(self) -> bool:
        '''Evaluate whether the time is currently counting'''
        if not self.stamps:
            return False
        else:
            return (len(self.stamps)%2 == 1)

    @property
    def is_started(self) -> bool:
        '''Evaluate whether the timer has started'''
        return True if self.stamps else False

    def calculate_passed_time(self):
        '''Calculate how much time passed in the unpaused intervals'''
        time_passed = 0

        # Calculate passed time, assuming that even timestamps are pauses:
        for index, _ in enumerate(self.stamps):
            if index > 0 and index%2 == 1:
                time_passed += float(self.stamps[index]) - float(self.stamps[index-1])

        # Add time passed during the current run:
        if self.is_counting:
            time_passed += time.time() - float(self.stamps[-1])

        # Depending on how much time has passed, show in different formats:
        one_hour = 60*60.0
        one_day = 24*one_hour
        if time_passed < one_hour:
            format_string = "%M:%S"
        else:
            format_string = "%H:%M:%S"
        time_string = str(time.strftime(format_string, time.gmtime(int(time_passed))))

        if 2*one_day > time_passed > one_day:
            time_string = "1 day " + time_string
        if time_passed >= 2*one_day:
            time_string = str(int(time_passed//one_day)) + " days " + time_string
        return time_string


######################## COLLECTIONS ###########################


class Collection:
    '''Parent class for collections of items like tasks or events'''
    def __init__(self):
        self.items = []
        self.changed = False

    def add_item(self, item):
        '''Add an item to the collection'''
        if len(item.name) > 0 and item.name != "\[":
            self.items.append(item)
            self.changed = True

    def delete_item(self, id):
        '''Delete an item with provided id from the collection'''
        for index, item in enumerate(self.items):
            if item.id == id:
                del self.items[index]
                self.changed = True
                break

    def rename_item(self, id, new_name):
        '''Edit an item name in the collection'''
        for item in self.items:
            if item.id == id and len(new_name) > 0:
                item.name = new_name
                self.changed = True

    def toggle_item_status(self, id, new_status):
        '''Toggle the status for the item with provided id'''
        for item in self.items:
            if item.id == id:
                if item.status == new_status:
                    item.status = 'normal'
                else:
                    item.status = new_status
                self.changed = True
                break

    def item_exists(self, item_name):
        '''Check if such item already exists in collection'''
        for item in self.items:
            if item.name == item_name:
                return True
        return False

    def change_all_statuses(self, new_status):
        '''Change statuses of all items'''
        for item in self.items:
            item.status = new_status
            self.changed = True

    def delete_all_items(self):
        '''Delete all items from the collection'''
        self.items = []
        self.changed = True

    def is_empty(self):
        '''Check if the collection is empty'''
        return True if len(self.items) == 0 else False

    def is_valid_number(self, number):
        '''Check if input is valid and corresponds to an item'''
        if number is None:
            return False
        return True if (0 <= number < len(self.items)) else False


class Events(Collection):
    '''List of events created by the user or imported'''
    def __init__(self):
        Collection.__init__(self)

    def filter_events_that_day(self, date):
        '''Filter only events that happen on the particular day'''
        events_of_the_day = Events()
        for event in self.items:
            if event.date == date:
                events_of_the_day.add_item(event)
        return events_of_the_day

    def change_day(self, id, new_day):
        '''Move task from certain place to another in the list'''
        for item in self.items:
            if item.id == id:
                item.day == new_day
                self.changed = True
                break


class Tasks(Collection):
    '''List of tasks created by the user'''

    def add_subtask(self, task, number):
        '''Add a subtask for certain task in the journal'''
        level = '----'if (self.items[number].name[:2] == '--') else '--'
        task.name = level + task.name
        if len(task.name) > 0:
            self.items.insert(number+1, task)
            self.changed = True

    def add_timestamp_for_task(self, number):
        '''Add a timestamp to this task'''
        if self.is_valid_number(number):
            self.items[number].timer.stamps.append(int(time.time()))
            self.changed = True

    def reset_timer_for_task(self, number):
        '''Reset the timer for one of the tasks'''
        if self.is_valid_number(number):
            self.items[number].timer.stamps = []
            self.changed = True

    def toggle_subtask_state(self, number):
        '''Toggle the state of the task-subtask'''
        if self.is_valid_number(number):
            if self.items[number].name[:2] == '--':
                self.items[number].name = self.items[number].name[2:]
            else:
                self.items[number].name = '--' + self.items[number].name
            self.changed = True

    def move_task(self, number_from, number_to):
        '''Move task from certain place to another in the list'''
        if self.is_valid_number(number_to):
            self.items.insert(number_to, self.items.pop(number_from))
            self.changed = True


#################### LOADERS, SAVERS, IMPORTERS ######################


class UserTasksLoader:
    @staticmethod
    def load_from_file(file):
        '''Reads from user's file or create it if it does not exist'''
        user_tasks = Tasks()
        try:
            with open(file, "r") as f:
                lines = csv.reader(f, delimiter = ',')
                for index, row in enumerate(lines):
                    id = index
                    name   = row[0]
                    status = row[1]
                    stamps = row[2:] if len(row) > 2 else []
                    user_tasks.add_item(Task(id, name, status, Timer(stamps) ))
        # Create file if it does not exist:
        except IOError:
            try:
                with open(file, "w+") as f:
                    pass
            # Pass if there was a problem with file system:
            except (FileNotFoundError, NameError):
                pass
        return user_tasks


class UserTasksSaver:
    @staticmethod
    def save_to_file(user_tasks, file):
        '''Rewrite the data file with changed tasks'''
        original_file = file
        dummy_file = file + '.bak'
        with open(dummy_file, "w") as f:
            for task in user_tasks.items:
                f.write(f'"{task.name}",{task.status}')
                for stamp in task.timer.stamps:
                    f.write(f',{str(stamp)}')
                f.write("\n")
        os.remove(original_file)
        os.rename(dummy_file, original_file)


class TasksImporters:
    @staticmethod
    def import_from_calcurse(user_tasks, calcurse_todo_file):
        '''Import todo events from calcurse database'''
        with open(calcurse_todo_file, 'r') as f:
            for task in f.readlines():
                name = task[4:-1]
                importance = task[1]
                if (name > 0) and not user_tasks.item_exists(name):
                    if importance in ['1','2']:
                        user_tasks.add_item(Task(name, 'important', Timer([])))
                    elif importance in ['8','9','10']:
                        user_tasks.add_item(Task(name, 'unimportant', Timer([])))
                    else:
                        user_tasks.add_item(Task(name, 'todo', Timer([])))

    @staticmethod
    def import_from_taskwarrior(user_tasks, taskwarrior_folder):
        '''Import tasks from taskwarrior database'''
        with open(taskwarrior_folder+"/pending.data", 'r') as f:
            for task in f.readlines():
                if len(task) > 0:
                    name = task.split('description:"',1)[1]
                    name = name.split('"',1)[0]
                    if not user_tasks.item(name):
                        user_tasks.add_item(Task(name, 'todo', Timer([])))


class UserEventsLoader:
    @staticmethod
    def load_from_file(file):
        '''Reads from user's file or create it if it does not exist'''
        user_events = Events()
        try:
            with open(file, "r") as f:
                lines = csv.reader(f, delimiter = ',')
                for index, row in enumerate(lines):
                    id = index
                    year = int(row[1])
                    month = int(row[2])
                    day = int(row[3])
                    name = row[4]

                    # Account for old versions of the datafile:
                    if len(row) > 5:
                        repetition = row[5]
                        frequency = row[6]
                    else:
                        repetition = '1'
                        frequency = 'n'
                    if len(row) > 7:
                        status = row[7]
                    else:
                        status = 'normal'

                    user_events.add_item(UserEvent(id, year, month, day,
                                name, repetition, frequency, status))
        # Create file if it does not exist:
        except IOError:
            try:
                with open(file, "w+") as f:
                    pass
            # Pass if there was a problem with file system:
            except (FileNotFoundError, NameError):
                pass
        return user_events


class UserEventsSaver:
    @staticmethod
    def save_to_file(user_events, original_file):
        '''Rewrite the data file with changed events'''
        dummy_file = original_file + '.bak'
        with open(dummy_file, "w") as f:
            for ev in user_events.items:
                f.write(f'{ev.id},{ev.year},{ev.month},{ev.day},"{ev.name}",{ev.repetition},{ev.frequency},{ev.status}\n')
        os.remove(original_file)
        os.rename(dummy_file, original_file)


class HolidaysLoader:
    @staticmethod
    def load_holidays(year, country):
        '''Load list of holidays in this country around this year'''
        try:
            import holidays as hl
            holidays = Events()
            holiday_events = eval("hl."+country+"(years=[year-1, year, year+1])")
            for date, name in holiday_events.items():
                holidays.add_item(Event(date.year, date.month, date.day, name))

        except (ModuleNotFoundError, SyntaxError, AttributeError):
            holidays = Events()
        return holidays


class BirthdaysLoader:
    @staticmethod
    def load_birthdays_from_abook():
        '''Loading birthdays from abook contacts'''
        abook_file = str(pathlib.Path.home())+"/.abook/addressbook"
        abook = configparser.ConfigParser()
        abook.read(abook_file)
        birthdays = Events()
        for each_contact in abook.sections():
            for (key, value) in abook.items(each_contact):
                if key == "birthday":
                    month = int(abook[each_contact]["birthday"][-5:-3])
                    day = int(abook[each_contact]["birthday"][-2:])
                    name = abook[each_contact]["name"]
                    birthdays.add_item(Event(1, month, day, name))
        return birthdays


class EventImporters:
    @staticmethod
    def import_from_calcurse(user_events, calcurse_events_file):
        '''Importing events from calcurse apt file into our events file'''
        with open(calcurse_events_file, "r") as f:
            lines = f.readlines()
        for index, line in enumerate(lines):
            month = int(line[0:2])
            day = int(line[3:5])
            year = int(line[6:10])
            if line[11] == "[":
                name = line[15:-1]
            elif line[11] == "@":
                name = line[35:-1]
                name = name.replace('|',' ')
            if len(user_events.items) > 0:
                id = 0
            else:
                id = user_events.items[-1].id+1
            user_events.add_item(UserEvent(id, year, month, day, name, 1, n, 'normal'))


class WeatherLoader:
    @staticmethod
    def load_from_wttr(city):
        '''Load the weather at launch and display weather widget.'''
        weather = Weather(city)
        try:
            max_load_time = 2 # seconds
            request_url = f"wttr.in/{city}?format=3"
            weather.forcast = str(subprocess.check_output(["curl", "-s", request_url],
                          timeout=max_load_time, encoding='utf-8'))[:-1]
            weather.forcast = weather.forcast.split(':')[1]
            weather.loaded = True
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            pass
        return weather
