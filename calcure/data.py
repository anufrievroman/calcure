"""Module provides datatypes used in the program"""

import time
import enum

from calcure.calendars import Calendar


class AppState(enum.Enum):
    """Possible focus states of the application"""
    CALENDAR = 1
    JOURNAL = 2
    HELP = 3
    EXIT = 4


class CalState(enum.Enum):
    """Possible states of the calendar view"""
    MONTHLY = 1
    DAILY = 2


class Status(enum.Enum):
    """Status of events and tasks"""
    NORMAL = 1
    DONE = 2
    IMPORTANT = 3
    UNIMPORTANT = 4


class Frequency(enum.Enum):
    """Frequency of repetitions of recurring events"""
    ONCE = 1
    DAILY = 2
    WEEKLY = 3
    MONTHLY = 4
    YEARLY = 5


class Color(enum.Enum):
    """Colors read from user config"""
    DAY_NAMES = 1
    WEEKENDS = 2
    HINTS = 3
    TODAY = 4
    DAYS = 5
    WEEKEND_NAMES = 6
    BIRTHDAYS = 7
    PROMPTS = 8
    CONFIRMATIONS = 9
    TITLE = 10
    TODO = 11
    DONE = 12
    IMPORTANT = 13
    TIMER = 14
    TIMER_PAUSED = 15
    HOLIDAYS = 16
    EVENTS = 17
    TIME = 18
    WEATHER = 19
    UNIMPORTANT = 20
    CALENDAR_HEADER = 21
    ACTIVE_PANE = 22
    SEPARATOR = 23
    EMPTY = 24
    CALENDAR_BOARDER = 24


class Task:
    """Task crated by user"""

    def __init__(self, item_id, name, status, timer, privacy):
        self.item_id = item_id
        self.name = name
        self.status = status
        self.timer = timer
        self.privacy = privacy


class Event:
    """Parent class of events"""

    def __init__(self, year, month, day, name):
        self.year = year
        self.month = month
        self.day = day
        self.name = name


class UserEvent(Event):
    """Events crated by user"""

    def __init__(self, item_id, year, month, day, name, repetition, frequency, status, privacy):
        super().__init__(year, month, day, name)
        self.item_id = item_id
        self.repetition = repetition
        self.frequency = frequency
        self.status = status
        self.privacy = privacy


class UserRepeatedEvent(Event):
    """Events that are repetitions of the original user events"""

    def __init__(self, item_id, year, month, day, name, status, privacy):
        super().__init__(year, month, day, name)
        self.item_id = item_id
        self.status = status
        self.privacy = privacy


class Timer:
    """Timer for a task"""

    def __init__(self, stamps):
        self.stamps = stamps

    @property
    def is_counting(self):
        """Evaluate if the time is currently counting"""
        return False if not self.stamps else (len(self.stamps)%2 == 1)

    @property
    def is_started(self):
        """Evaluate whether the timer has started"""
        return True if self.stamps else False

    @property
    def passed_time(self):
        """Calculate how much time passed in the un-paused intervals"""
        time_passed = 0

        # Calculate passed time, assuming that even timestamps are pauses:
        for index, _ in enumerate(self.stamps):
            if index > 0 and index % 2 == 1:
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


class Collection:
    """Parent class for collections of items like tasks or events"""

    def __init__(self):
        self.items = []
        self.changed = False

    def add_item(self, item):
        """Add an item to the collection"""
        if 100 > len(item.name) > 0 and item.name != "\[":
            self.items.append(item)
            self.changed = True

    def delete_item(self, selected_task_id):
        """Delete an item with provided id from the collection"""
        for item in self.items:
            if item.item_id == selected_task_id:
                self.items.remove(item)
                self.changed = True
                break

    def rename_item(self, selected_task_id, new_name):
        """Edit an item name in the collection"""
        for item in self.items:
            if item.item_id == selected_task_id and len(new_name) > 0:
                item.name = new_name
                self.changed = True

    def toggle_item_status(self, selected_task_id, new_status):
        """Toggle the status for the item with provided id"""
        for item in self.items:
            if item.item_id == selected_task_id:
                if item.status == new_status:
                    item.status = Status.NORMAL
                else:
                    item.status = new_status
                self.changed = True
                break

    def toggle_item_privacy(self, selected_task_id):
        """Toggle the privacy for the item with provided id"""
        for item in self.items:
            if item.item_id == selected_task_id:
                item.privacy = not item.privacy
                self.changed = True
                break

    def item_exists(self, item_name):
        """Check if such item already exists in collection"""
        for item in self.items:
            if item.name == item_name:
                return True
        return False

    def change_all_statuses(self, new_status):
        """Change statuses of all items"""
        for item in self.items:
            item.status = new_status
            self.changed = True

    def delete_all_items(self):
        """Delete all items from the collection"""
        self.items.clear()
        self.changed = True

    def is_empty(self):
        """Check if the collection is empty"""
        return len(self.items) == 0

    def is_valid_number(self, number):
        """Check if input is valid and corresponds to an item"""
        if number is None:
            return False
        return 0 <= number < len(self.items)


class Tasks(Collection):
    """List of tasks created by the user"""

    def add_subtask(self, task, number):
        """Add a subtask for certain task in the journal"""
        level = '----'if (self.items[number].name[:2] == '--') else '--'
        task.name = level + task.name
        if 100 > len(task.name) > 0:
            self.items.insert(number+1, task)
            self.changed = True

    def add_timestamp_for_task(self, number):
        """Add a timestamp to this task"""
        self.items[number].timer.stamps.append(int(time.time()))
        self.changed = True

    def reset_timer_for_task(self, number):
        """Reset the timer for one of the tasks"""
        self.items[number].timer.stamps = []
        self.changed = True

    def toggle_subtask_state(self, number):
        """Toggle the state of the task-subtask"""
        if self.items[number].name[:2] == '--':
            self.items[number].name = self.items[number].name[2:]
        else:
            self.items[number].name = '--' + self.items[number].name
        self.changed = True

    def move_task(self, number_from, number_to):
        """Move task from certain place to another in the list"""
        self.items.insert(number_to, self.items.pop(number_from))
        self.changed = True


class Events(Collection):
    """List of events created by the user or imported"""

    def event_exists(self, new_event):
        """Check if such event already exists in collection"""
        for event in self.items:
            if (event.name == new_event.name
                and event.year == new_event.year
                and event.month == new_event.month
                and event.day == new_event.day):
                return True
        return False

    def filter_events_that_day(self, screen):
        """Filter only events that happen on the particular day"""
        events_of_the_day = Events()
        for event in self.items:
            if (event.year == screen.year
                and event.month == screen.month
                and event.day == screen.day):
                events_of_the_day.add_item(event)
        return events_of_the_day

    def filter_events_that_month(self, screen):
        """Filter only events that happen on the particular month and sort them by day"""
        events_of_the_month = Events()
        for event in self.items:
            if event.month == screen.month and event.year == screen.year:
                events_of_the_month.add_item(event)
        events_of_the_month.items = sorted(events_of_the_month.items, key=lambda item: item.day)
        return events_of_the_month

    def change_day(self, selected_item_id, new_day):
        """Move task from certain place to another in the list"""
        for item in self.items:
            if item.item_id == selected_item_id:
                item.day = new_day
                self.changed = True
                break


class Birthdays(Events):
    """List of birthdays"""

    def filter_events_that_day(self, screen):
        """Filter only birthdays that happen on the particular day"""
        events_of_the_day = Events()
        for event in self.items:
            if event.month == screen.month and event.day == screen.day:
                events_of_the_day.add_item(event)
        return events_of_the_day


class RepeatedEvents(Events):
    """List of events that are repetitions of the main events"""

    def __init__(self, user_events, use_persian_calendar):
        super().__init__()
        self.user_events = user_events
        self.use_persian_calendar = use_persian_calendar

        for event in self.user_events.items:
            if event.repetition >= 1:
                for rep in range(1, event.repetition):
                    temp_year = event.year + rep*(event.frequency == Frequency.YEARLY)
                    temp_month = event.month + rep*(event.frequency == Frequency.MONTHLY)
                    temp_day = event.day + rep*(event.frequency == Frequency.DAILY) + 7*rep*(event.frequency == Frequency.WEEKLY)
                    year, month, day = self.calculate_recurring_events(temp_year, temp_month, temp_day, event.frequency)
                    self.add_item(UserRepeatedEvent(event.item_id, year, month, day, event.name, event.status, event.privacy))

    def calculate_recurring_events(self, year, month, day, frequency):
        """Calculate the date of recurring events so that they occur in the next month or year"""
        new_day = day
        new_month = month
        new_year = year
        skip_days = 0

        # Weekly and daily recurrence:
        if frequency in [Frequency.WEEKLY, Frequency.DAILY]:

            # Calculate how many days and month to skip to next event:
            for i in range(1000):
                if month + i > 12:
                    year = year + 1
                    month = month - 12

                last_day = Calendar(0, self.use_persian_calendar).last_day(year, month+i)
                if day > skip_days + last_day:
                    skip_days += last_day
                    skip_months = i + 1
                else:
                    skip_months = i
                    break
            new_day = day - skip_days
            new_month = month + skip_months
            new_year = year

        # Monthly recurrence:
        if frequency == Frequency.MONTHLY:
            if month > 12:
                new_year = year + (month - 1)//12
                new_month = month - 12*(new_year - year)
        return new_year, new_month, new_day
