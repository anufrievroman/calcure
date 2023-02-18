"""This module contains functions that react to user input on each screen"""

import curses
import importlib

# Modules:
from calcure.configuration import cf
from calcure.data import *
from calcure.dialogues import *

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


def control_monthly_screen(stdscr, user_events, screen, importer):
    """Handle user input on the daily screen"""
    try:
        # If we previously entered the selection mode, now we perform the action:
        if screen.selection_mode:
            screen.selection_mode = False

            # Change event status:
            if screen.key in ['i', 'h']:
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_HIGH)
                if user_events.filter_events_that_month(screen).is_valid_number(number):
                    event_id = user_events.filter_events_that_month(screen).items[number].item_id
                    user_events.toggle_item_status(event_id, Status.IMPORTANT)
            if screen.key == 'l':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_LOW)
                if user_events.filter_events_that_month(screen).is_valid_number(number):
                    event_id = user_events.filter_events_that_month(screen).items[number].item_id
                    user_events.toggle_item_status(event_id, Status.UNIMPORTANT)
            if screen.key == 'u':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_RESET)
                if user_events.filter_events_that_month(screen).is_valid_number(number):
                    event_id = user_events.filter_events_that_month(screen).items[number].item_id
                    user_events.toggle_item_status(event_id, Status.NORMAL)

            # Toggle event privacy:
            if screen.key == '.':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_PRIVACY)
                if user_events.filter_events_that_month(screen).is_valid_number(number):
                    event_id = user_events.filter_events_that_month(screen).items[number].item_id
                    user_events.toggle_item_privacy(event_id)

            # Delete event:
            if screen.key in ['d', 'x']:
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_DEL)
                if user_events.filter_events_that_month(screen).is_valid_number(number):
                    event_id = user_events.filter_events_that_month(screen).items[number].item_id
                    user_events.delete_item(event_id)

            # Edit event:
            if screen.key in ['e', 'c']:
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_REN)
                if user_events.filter_events_that_month(screen).is_valid_number(number):
                    event_id = user_events.filter_events_that_month(screen).items[number].item_id
                    clear_line(stdscr, screen.y_max-2)
                    new_name = input_string(stdscr, screen.y_max-2, 0, MSG_NEW_TITLE, screen.x_max-len(MSG_NEW_TITLE)-2)
                    user_events.rename_item(event_id, new_name)

            # Move event:
            if screen.key == 'm':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_MOVE)
                if user_events.filter_events_that_month(screen).is_valid_number(number):
                    event_id = user_events.filter_events_that_month(screen).items[number].item_id
                    clear_line(stdscr, screen.y_max-2)
                    question = f'{MSG_EVENT_MOVE_TO} {screen.year}/{screen.month}/'
                    day = input_day(stdscr, screen.y_max-2, 0, question)
                    if screen.is_valid_day(day):
                        user_events.change_day(event_id, day)

        # Otherwise, we check for user input:
        else:
            # Wait for user to press a key:
            screen.key = stdscr.getkey()

            # If we need to select an event, change to selection mode:
            if screen.key in ['h', 'l', 'u', 'i', 'd', 'x', 'e', 'c', 'm', '.']:
                screen.selection_mode = True

            # Navigation:
            if screen.key in ["n", "j", "KEY_UP", "KEY_RIGHT"]:
                screen.next_month()
            if screen.key in ["p", "k", "KEY_DOWN", "KEY_LEFT"]:
                screen.previous_month()
            if screen.key in ["KEY_HOME", "G"]:
                screen.reset_to_today()

            # Handle "g" as go to selected day:
            if screen.key == "g":
                question = f'Go to date: {str(screen.year)}/{str(screen.month)}/'
                day = input_day(stdscr, screen.y_max-2, 0, question)
                if screen.is_valid_day(day):
                    screen.day = day
                    screen.calendar_state = CalState.DAILY

            # Change the view to daily:
            if screen.key == "v":
                screen.day = 1
                screen.calendar_state = CalState.DAILY

            # Add single event:
            if screen.key == "a":
                question = f'{MSG_EVENT_DATE} {screen.year}/{screen.month}/'
                day = input_day(stdscr, screen.y_max-2, 0, question)
                if screen.is_valid_day(day):
                    clear_line(stdscr, screen.y_max-2)
                    name = input_string(stdscr, screen.y_max-2, 0, MSG_EVENT_TITLE, screen.x_max-len(MSG_EVENT_TITLE)-2)
                    event_id = user_events.items[-1].item_id + 1 if not user_events.is_empty() else 1
                    user_events.add_item(UserEvent(event_id, screen.year, screen.month, day, name, 1, Frequency.ONCE, Status.NORMAL, False))

            # Add a recurring event:
            if screen.key == "A":
                question = f'{MSG_EVENT_DATE}{screen.year}/{screen.month}/'
                day = input_day(stdscr, screen.y_max-2, 0, question)
                if screen.is_valid_day(day):
                    clear_line(stdscr, screen.y_max-2)
                    name = input_string(stdscr, screen.y_max-2, 0, MSG_EVENT_TITLE, screen.x_max-len(MSG_EVENT_TITLE)-2)
                    item_id = user_events.items[-1].item_id + 1 if not user_events.is_empty() else 1
                    reps = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_REP)
                    freq = input_frequency(stdscr, screen.y_max-2, 0, MSG_EVENT_FR)
                    if reps is not None and freq is not None:
                        reps = 1 if reps == 0 else reps
                        user_events.add_item(UserEvent(item_id, screen.year, screen.month, day, name, reps+1, freq, Status.NORMAL, False))

            # Imports:
            if screen.key == "C":
                confirmed = ask_confirmation(stdscr, MSG_EVENT_IMP, cf.ASK_CONFIRMATIONS)
                if confirmed:
                    importer.import_events_from_calcurse()
                    screen.refresh_now = True

            # Other actions:
            if vim_style_exit(stdscr, screen):
                confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
                screen.state = AppState.EXIT if confirmed else screen.state
            if screen.key == "*":
                screen.privacy = not screen.privacy
            if screen.key in [" ", "KEY_BTAB"]:
                screen.state = AppState.JOURNAL
            if screen.key == "?":
                screen.state = AppState.HELP
            if screen.key in ["q", "\b", "\x7f"]:
                confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
                screen.state = AppState.EXIT if confirmed else screen.state
            if screen.key in ["/"]:
                screen.split = not screen.split
                screen.refresh_now = True

    # Handle keyboard interruption with ctr+c:
    except KeyboardInterrupt:
        confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
        screen.state = AppState.EXIT if confirmed else screen.state

    # Prevent crash if no input:
    except curses.error:
        pass


def control_daily_screen(stdscr, user_events, screen, importer):
    """Handle user input on the daily screen"""
    try:
        # If we previously entered the selection mode, now we perform the action:
        if screen.selection_mode:
            screen.selection_mode = False

            # Chance event status:
            if screen.key in ['i', 'h']:
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_HIGH)
                if user_events.filter_events_that_day(screen).is_valid_number(number):
                    item_id = user_events.filter_events_that_day(screen).items[number].item_id
                    user_events.toggle_item_status(item_id, Status.IMPORTANT)
            if screen.key == 'l':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_LOW)
                if user_events.filter_events_that_day(screen).is_valid_number(number):
                    item_id = user_events.filter_events_that_day(screen).items[number].item_id
                    user_events.toggle_item_status(item_id, Status.UNIMPORTANT)
            if screen.key == 'u':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_RESET)
                if user_events.filter_events_that_day(screen).is_valid_number(number):
                    item_id = user_events.filter_events_that_day(screen).items[number].item_id
                    user_events.toggle_item_status(item_id, Status.NORMAL)

            # Toggle event privacy:
            if screen.key == '.':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_PRIVACY)
                if user_events.filter_events_that_day(screen).is_valid_number(number):
                    event_id = user_events.filter_events_that_day(screen).items[number].item_id
                    user_events.toggle_item_privacy(event_id)

            # Delete event:
            if screen.key in ['d', 'x']:
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_DEL)
                if user_events.filter_events_that_day(screen).is_valid_number(number):
                    item_id = user_events.filter_events_that_day(screen).items[number].item_id
                    user_events.delete_item(item_id)

            # Edit event:
            if screen.key in ['e', 'c']:
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_REN)
                if user_events.filter_events_that_day(screen).is_valid_number(number):
                    item_id = user_events.filter_events_that_day(screen).items[number].item_id
                    clear_line(stdscr, screen.y_max-2)
                    new_name = input_string(stdscr, screen.y_max-2, 0, MSG_NEW_TITLE, screen.x_max-len(MSG_NEW_TITLE)-2)
                    user_events.rename_item(item_id, new_name)

            # Move event:
            if screen.key == 'm':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_MOVE)
                if user_events.filter_events_that_day(screen).is_valid_number(number):
                    item_id = user_events.filter_events_that_day(screen).items[number].item_id
                    clear_line(stdscr, screen.y_max-2)
                    question = f'{MSG_EVENT_MOVE_TO}{screen.year}/{screen.month}/'
                    day = input_day(stdscr, screen.y_max-2, 0, question)
                    if screen.is_valid_day(day):
                        user_events.change_day(item_id, day)

        # Otherwise, we check for user input:
        else:
            # Wait for user to press a key:
            screen.key = stdscr.getkey()

            # If we need to select an event, change to selection mode:
            if screen.key in ['h', 'l', 'u', 'i', 'd', 'x', 'e', 'c', 'm', '.']:
                screen.selection_mode = True

            # Navigation:
            if screen.key in ["n", "j", "KEY_UP", "KEY_RIGHT"]:
                screen.next_day()
            if screen.key in ["p", "k", "KEY_DOWN", "KEY_LEFT"]:
                screen.previous_day()
            if screen.key in ["KEY_HOME", "G"]:
                screen.reset_to_today()

            # Add single event:
            if screen.key == "a":
                name = input_string(stdscr, screen.y_max-2, 0, MSG_EVENT_TITLE, screen.x_max-len(MSG_EVENT_TITLE)-2)
                item_id = user_events.items[-1].item_id + 1 if not user_events.is_empty() else 1
                user_events.add_item(UserEvent(item_id, screen.year, screen.month, screen.day, name, 1, Frequency.ONCE, Status.NORMAL, False))

            # Add a recurring event:
            if screen.key == "A":
                name = input_string(stdscr, screen.y_max-2, 0, MSG_EVENT_TITLE, screen.x_max-len(MSG_EVENT_TITLE)-2)
                item_id = user_events.items[-1].item_id + 1 if not user_events.is_empty() else 1
                reps = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_REP)
                freq = input_frequency(stdscr, screen.y_max-2, 0, MSG_EVENT_FR)
                if reps is not None and freq is not None:
                    reps = 1 if reps == 0 else reps
                    user_events.add_item(UserEvent(item_id, screen.year, screen.month, screen.day, name, reps+1, freq, Status.NORMAL, False))

            # Import from calcurse:
            if screen.key == "C":
                confirmed = ask_confirmation(stdscr, MSG_EVENT_IMP, cf.ASK_CONFIRMATIONS)
                if confirmed:
                    importer.import_events_from_calcurse()

            # Change the view to monthly:
            if screen.key == "v":
                screen.calendar_state = CalState.MONTHLY

            # Other actions:
            if vim_style_exit(stdscr, screen):
                confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
                screen.state = AppState.EXIT if confirmed else screen.state
            if screen.key == "*":
                screen.privacy = not screen.privacy
            if screen.key in [" ", "KEY_BTAB"]:
                screen.state = AppState.JOURNAL
            if screen.key == "?":
                screen.state = AppState.HELP
            if screen.key in ["q", "KEY_BACKSPACE", "\b", "\x7f"]:
                screen.calendar_state = CalState.MONTHLY
            if screen.key in ["/"]:
                screen.split = not screen.split
                screen.refresh_now = True

    # Handle keyboard interruption with ctr+c:
    except KeyboardInterrupt:
        confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
        screen.state = AppState.EXIT if confirmed else screen.state

    # Prevent crash if no input:
    except curses.error:
        pass


def control_journal_screen(stdscr, user_tasks, screen, importer):
    """Process user input on the journal screen"""
    try:
        # If we previously selected a task, now we perform the action:
        if screen.selection_mode:

            # Timer operations:
            if screen.key == 't':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TM_ADD)
                if user_tasks.is_valid_number(number):
                    task_id = user_tasks.items[number].item_id
                    if cf.ONE_TIMER_AT_A_TIME:
                        user_tasks.pause_all_other_timers(task_id)
                    user_tasks.add_timestamp_for_task(task_id)

            if screen.key == 'T':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TM_RESET)
                if user_tasks.is_valid_number(number):
                    task_id = user_tasks.items[number].item_id
                    user_tasks.reset_timer_for_task(task_id)

            # Add deadline:
            if screen.key == "f":
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_DEAD_ADD)
                if user_tasks.is_valid_number(number):
                    task_id = user_tasks.items[number].item_id
                    clear_line(stdscr, screen.y_max-2, 0)
                    year, month, day = input_date(stdscr, screen.y_max-2, 0, MSG_TS_DEAD_DATE)
                    if screen.is_valid_date(year, month, day):
                        user_tasks.change_deadline(task_id, year, month, day)

            # Remove deadline:
            if screen.key == "F":
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_DEAD_DEL)
                if user_tasks.is_valid_number(number):
                    task_id = user_tasks.items[number].item_id
                    user_tasks.change_deadline(task_id, 0, 0, 0)

            # Change the status:
            if screen.key in ['i', 'h']:
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_HIGH)
                if user_tasks.is_valid_number(number):
                    task_id = user_tasks.items[number].item_id
                    user_tasks.toggle_item_status(task_id, Status.IMPORTANT)
            if screen.key == 'l':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_LOW)
                if user_tasks.is_valid_number(number):
                    task_id = user_tasks.items[number].item_id
                    user_tasks.toggle_item_status(task_id, Status.UNIMPORTANT)
            if screen.key == 'u':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_RES)
                if user_tasks.is_valid_number(number):
                    task_id = user_tasks.items[number].item_id
                    user_tasks.toggle_item_status(task_id, Status.NORMAL)
            if screen.key == 'v':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_DONE)
                if user_tasks.is_valid_number(number):
                    task_id = user_tasks.items[number].item_id
                    user_tasks.toggle_item_status(task_id, Status.DONE)

            # Toggle task privacy:
            if screen.key == '.':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_PRIVACY)
                if user_tasks.is_valid_number(number):
                    task_id = user_tasks.items[number].item_id
                    user_tasks.toggle_item_privacy(task_id)

            # Modify the task:
            if screen.key in ['d', 'x']:
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_DEL)
                if user_tasks.is_valid_number(number):
                    task_id = user_tasks.items[number].item_id
                    user_tasks.delete_item(task_id)
            if screen.key == 'm':
                number_from = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_MOVE)
                if user_tasks.is_valid_number(number_from):
                    clear_line(stdscr, screen.y_max-2)
                    number_to = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_MOVE_TO)
                    user_tasks.move_task(number_from, number_to)
            if screen.key in ['e', 'c']:
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_EDIT)
                if user_tasks.is_valid_number(number):
                    task_id = user_tasks.items[number].item_id
                    clear_line(stdscr, number+2, screen.x_min)
                    new_name = input_string(stdscr, number+2, screen.x_min, cf.TODO_ICON+' ', screen.x_max-4)
                    user_tasks.rename_item(task_id, new_name)

            # Subtask operations:
            if screen.key == 's':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_TOG)
                if user_tasks.is_valid_number(number):
                    task_id = user_tasks.items[number].item_id
                    user_tasks.toggle_subtask_state(task_id)
            if screen.key == 'A':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_SUB)
                if user_tasks.is_valid_number(number):
                    clear_line(stdscr, screen.y_max-2, 0)
                    task_name = input_string(stdscr, screen.y_max-2, 0, MSG_TS_TITLE, screen.x_max-len(MSG_TS_TITLE)-2)
                    task_id = user_tasks.generate_id()
                    user_tasks.add_subtask(Task(task_id, task_name, Status.NORMAL, Timer([]), False), number)
            screen.selection_mode = False

        # Otherwise, we check for user input:
        else:
            # Wait for user to press a key:
            screen.key = stdscr.getkey()

            # If we need to select a task, change to selection mode:
            if screen.key in ['t', 'T', 'h', 'l', 'v', 'u', 'i', 's', 'd', 'x', 'e', 'c', 'A', 'm', '.', 'f', 'F']:
                screen.selection_mode = True

            # Add single task:
            if screen.key == "a":
                clear_line(stdscr, len(user_tasks.items) + 2, screen.x_min)
                task_name = input_string(stdscr, len(user_tasks.items) + 2, screen.x_min, cf.TODO_ICON+' ', screen.x_max - 4)
                task_id = user_tasks.generate_id()
                user_tasks.add_item(Task(task_id, task_name, Status.NORMAL, Timer([]), False))

            # Bulk operations:
            if screen.key == "V":
                user_tasks.change_all_statuses(Status.DONE)
            if screen.key == "U":
                user_tasks.change_all_statuses(Status.NORMAL)
            if screen.key == "L":
                user_tasks.change_all_statuses(Status.UNIMPORTANT)
            if screen.key in ["I", "H"]:
                user_tasks.change_all_statuses(Status.IMPORTANT)
            if screen.key in ["D", "X"]:
                confirmed = ask_confirmation(stdscr, MSG_TS_DEL_ALL, cf.ASK_CONFIRMATIONS)
                if confirmed:
                    user_tasks.delete_all_items()

            # Imports:
            if screen.key == "C":
                confirmed = ask_confirmation(stdscr, MSG_TS_IM, cf.ASK_CONFIRMATIONS)
                if confirmed:
                    importer.import_tasks_from_calcurse()
                    screen.refresh_now = True
            if screen.key == "W":
                confirmed = ask_confirmation(stdscr, MSG_TS_TW, cf.ASK_CONFIRMATIONS)
                if confirmed:
                    importer.import_tasks_from_taskwarrior()
                    screen.refresh_now = True

            # Other actions:
            if vim_style_exit(stdscr, screen):
                confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
                screen.state = AppState.EXIT if confirmed else screen.state
            if screen.key == "*":
                screen.privacy = not screen.privacy
            if screen.key in [" ", "KEY_BTAB"]:
                screen.state = AppState.CALENDAR
            if screen.key == "?":
                screen.state = AppState.HELP
            if screen.key == "q":
                confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
                screen.state = AppState.EXIT if confirmed else screen.state
            if screen.key in ["/"]:
                screen.split = not screen.split
                screen.refresh_now = True

    # Handle keybard interruption with ctr+c:
    except KeyboardInterrupt:
        confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
        screen.state = AppState.EXIT if confirmed else screen.state

    # Prevent crash if no input:
    except curses.error:
        pass


def control_help_screen(stdscr, screen):
    """Process user input on the help screen"""
    try:
        # Getting user's input:
        screen.key = stdscr.getkey()

        # Handle vim-style exit on "ZZ" and "ZQ":
        if vim_style_exit(stdscr, screen):
            confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
            screen.state = AppState.EXIT if confirmed else screen.state

        # Handle keys to exit the help screen:
        if screen.key in [" ", "?", "q", "KEY_BACKSPACE", "^[", "\x7f"]:
            screen.state = AppState.CALENDAR

    except KeyboardInterrupt:
        confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
        screen.state = AppState.EXIT if confirmed else screen.state

    # Prevent crash if no input:
    except curses.error:
        pass


def control_welcome_screen(stdscr, screen):
    """Process user input on the welcome screen"""
    try:
        # Getting user's input:
        screen.key = stdscr.getkey()

        # Handle key to call help screen:
        if screen.key in ["?"]:
            screen.state = AppState.HELP
        else:
            screen.state = AppState.CALENDAR

    except KeyboardInterrupt:
        confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
        screen.state = AppState.EXIT if confirmed else screen.state

    # Prevent crash if no input:
    except curses.error:
        pass
