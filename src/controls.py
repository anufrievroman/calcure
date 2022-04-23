import curses

from config import cf
from translation_en import *
from data import *
from dialogues import *


def vim_style_exit(stdscr, screen):
    '''Handle vim style key combinations like "ZZ" and "ZQ" for exit'''
    if screen.key == "Z":
        try:
            screen.key = stdscr.getkey()
            return True if screen.key in ["Z", "Q"] else False
        except KeyboardInterrupt:
            return True
    else:
        return False


########################## MONTHLY SCREEN CONTROL ###################################


def control_monthly_screen(stdscr, user_events, screen):
    '''Handle user input on the daily screen'''
    try:
        # If we previously entered the selection mode, now we perform the action:
        if screen.selection_mode:
            screen.selection_mode = False

            # Chance event status:
            if screen.key in ['i', 'h']:
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_HIGH)
                if user_events.filter_events_that_month(screen).is_valid_number(number):
                    id = user_events.filter_events_that_month(screen).items[number].id
                    user_events.toggle_item_status(id, Status.IMPORTANT)
            if screen.key == 'l':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_LOW)
                if user_events.filter_events_that_month(screen).is_valid_number(number):
                    id = user_events.filter_events_that_month(screen).items[number].id
                    user_events.toggle_item_status(id, Status.UNIMPORTANT)
            if screen.key == 'u':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_RESET)
                if user_events.filter_events_that_month(screen).is_valid_number(number):
                    id = user_events.filter_events_that_month(screen).items[number].id
                    user_events.toggle_item_status(id, Status.NORMAL)

            # Delete event:
            if screen.key in ['d', 'x']:
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_DEL)
                if user_events.filter_events_that_month(screen).is_valid_number(number):
                    id = user_events.filter_events_that_month(screen).items[number].id
                    user_events.delete_item(id)

            # Edit event:
            if screen.key in ['e', 'c']:
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_REN)
                if user_events.filter_events_that_month(screen).is_valid_number(number):
                    id = user_events.filter_events_that_month(screen).items[number].id
                    clear_line(stdscr, screen.y_max-2)
                    new_name = input_string(stdscr, screen.y_max-2, 0, MSG_NEW_TITLE, screen.x_max-len(MSG_NEW_TITLE)-2)
                    user_events.rename_item(id, new_name)

            # Move event:
            if screen.key == 'm':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_MOVE)
                if user_events.filter_events_that_month(screen).is_valid_number(number):
                    id = user_events.filter_events_that_month(screen).items[number].id
                    clear_line(stdscr, screen.y_max-2)
                    question = f'{MSG_EVENT_MOVE_TO} {screen.year}/{screen.month}/'
                    day = input_day(stdscr, screen.y_max-2, 0, question)
                    if screen.is_valid_day(day):
                        user_events.change_day(id, day)

        # Otherwise, we check for user input:
        else:
            # Wait for user to press a key:
            screen.key = stdscr.getkey()

            # If we need to select an event, change to selection mode:
            if screen.key in ['h','l','u','i','d','x','e','c','m']:
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
                question = "Go to date: "+str(screen.year)+"/"+str(screen.month)+"/"
                day = input_day(stdscr, screen.y_max-2, 0, question)
                if screen.is_valid_day(day):
                    screen.day = day
                    screen.state = State.DAILY

            # Add single event:
            if screen.key == "a":
                question = f'{MSG_EVENT_DATE} {screen.year}/{screen.month}/'
                day = input_day(stdscr, screen.y_max-2, 0, question)
                if screen.is_valid_day(day):
                    clear_line(stdscr, screen.y_max-2)
                    name = input_string(stdscr, screen.y_max-2, 0, MSG_EVENT_TITLE, screen.x_max-len(MSG_EVENT_TITLE)-2)
                    id = user_events.items[-1].id + 1 if not user_events.is_empty() else 1
                    user_events.add_item(UserEvent(id, screen.year, screen.month, day, name, 1, 'n', Status.NORMAL))

            # Add a recurring event:
            if screen.key == "A":
                question = f'{MSG_EVENT_DATE}{screen.year}/{screen.month}/'
                day = input_day(stdscr, screen.y_max-2, 0, question)
                if screen.is_valid_day(day):
                    clear_line(stdscr, screen.y_max-2)
                    name = input_string(stdscr, screen.y_max-2, 0, MSG_EVENT_TITLE, screen.x_max-len(MSG_EVENT_TITLE)-2)
                    id = user_events.items[-1].id + 1 if not user_events.is_empty() else 1
                    reps = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_REP)
                    freq = input_string(stdscr, screen.y_max-2, 0, MSG_EVENT_FR, 1)
                    if int(reps) > 0 and freq in ["d","w","m","y","n"]:
                        user_events.add_item(UserEvent(id, screen.year, screen.month, day, name, reps+1, freq, Status.NORMAL))

            # Imports:
            if screen.key == "C":
                confirmed = ask_confirmation(stdscr, MSG_EVENT_IMP, cf.ASK_CONFIRMATIONS)
                if confirmed:
                    EventImporters.import_from_calcurse(user_events, cf.CALCURSE_EVENTS_FILE)

            # Other actions:
            if vim_style_exit(stdscr, screen):
                confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
                if confirmed: screen.state = State.EXIT
            if screen.key == "*": screen.privacy = not screen.privacy
            if screen.key in [" ", "KEY_BTAB"]:
                screen.state = State.JOURNAL
            if screen.key == "?":
                screen.state = State.HELP
            if screen.key in ["q", "KEY_BACKSPACE", "\b", "\x7f"]:
                confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
                if confirmed: screen.state = State.EXIT
            if screen.key in ["/"]:
                screen.split = not screen.split
                screen.refresh_now = True

            # Handle screen resize:
            if screen.key == "KEY_RESIZE":
                # screen.y_max, screen.x_max = stdscr.getmaxyx()
                screen.y_max, _ = stdscr.getmaxyx()

    # Handle keybard interruption with ctr+c:
    except KeyboardInterrupt:
        confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
        if confirmed: screen.state = State.EXIT

    # Prevent crash if no input:
    except Exception:
        pass


########################## DAILY SCREEN CONTROL ###################################


def control_daily_screen(stdscr, user_events, screen):
    '''Handle user input on the daily screen'''
    try:
        # If we previously entered the selection mode, now we perform the action:
        if screen.selection_mode:
            screen.selection_mode = False

            # Chance event status:
            if screen.key in ['i', 'h']:
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_HIGH)
                if user_events.filter_events_that_day(screen).is_valid_number(number):
                    id = user_events.filter_events_that_day(screen).items[number].id
                    user_events.toggle_item_status(id, Status.IMPORTANT)
            if screen.key == 'l':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_LOW)
                if user_events.filter_events_that_day(screen).is_valid_number(number):
                    id = user_events.filter_events_that_day(screen).items[number].id
                    user_events.toggle_item_status(id, Status.UNIMPORTANT)
            if screen.key == 'u':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_RESET)
                if user_events.filter_events_that_day(screen).is_valid_number(number):
                    id = user_events.filter_events_that_day(screen).items[number].id
                    user_events.toggle_item_status(id, Status.NORMAL)

            # Delete event:
            if screen.key in ['d', 'x']:
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_DEL)
                if user_events.filter_events_that_day(screen).is_valid_number(number):
                    id = user_events.filter_events_that_day(screen).items[number].id
                    user_events.delete_item(id)

            # Edit event:
            if screen.key in ['e', 'c']:
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_REN)
                if user_events.filter_events_that_day(screen).is_valid_number(number):
                    id = user_events.filter_events_that_day(screen).items[number].id
                    clear_line(stdscr, screen.y_max-2)
                    new_name = input_string(stdscr, screen.y_max-2, 0, MSG_NEW_TITLE, screen.x_max-len(MSG_NEW_TITLE)-2)
                    user_events.rename_item(id, new_name)

            # Move event:
            if screen.key == 'm':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_MOVE)
                if user_events.filter_events_that_day(screen).is_valid_number(number):
                    id = user_events.filter_events_that_day(screen).items[number].id
                    clear_line(stdscr, screen.y_max-2)
                    question = f'{MSG_EVENT_MOVE_TO}{screen.year}/{screen.month}/'
                    day = input_day(stdscr, screen.y_max-2, 0, question)
                    if screen.is_valid_day(day):
                        user_events.change_day(id, day)

        # Otherwise, we check for user input:
        else:
            # Wait for user to press a key:
            screen.key = stdscr.getkey()

            # If we need to select an event, change to selection mode:
            if screen.key in ['h','l','u','i','d','x','e','c','m']:
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
                id = user_events.items[-1].id + 1 if not user_events.is_empty() else 1
                user_events.add_item(UserEvent(id, screen.year, screen.month, screen.day, name, 1, 'n', Status.NORMAL))

            # Add a recurring event:
            if screen.key == "A":
                name = input_string(stdscr, screen.y_max-2, 0, MSG_EVENT_TITLE, screen.x_max-len(MSG_EVENT_TITLE)-2)
                id = user_events.items[-1].id + 1 if not user_events.is_empty() else 1
                reps = input_integer(stdscr, screen.y_max-2, 0, MSG_EVENT_REP)
                freq = input_string(stdscr, screen.y_max-2, 0, MSG_EVENT_FR, 1)
                if int(reps) > 0 and freq in ["d","w","m","y","n"]:
                    user_events.add_item(UserEvent(id, screen.year, screen.month, screen.day, name, reps+1, freq, Status.NORMAL))

            # Import from calcurse:
            if screen.key == "C":
                confirmed = ask_confirmation(stdscr, MSG_EVENT_IMP, cf.ASK_CONFIRMATIONS)
                if confirmed:
                    EventImporters.import_from_calcurse(user_events, cf.CALCURSE_EVENTS_FILE)

            # Other actions:
            if vim_style_exit(stdscr, screen):
                confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
                if confirmed: screen.state = State.EXIT
            if screen.key == "*": screen.privacy = not screen.privacy
            if screen.key in [" ", "KEY_BTAB"]:
                screen.state = State.JOURNAL
            if screen.key == "?":
                screen.state = State.HELP
            if screen.key in ["q", "KEY_BACKSPACE", "\b", "\x7f"]:
                screen.state = State.MONTHLY
            if screen.key in ["/"]:
                screen.split = not screen.split
                screen.refresh_now = True

            # Handle screen resize:
            if screen.key == "KEY_RESIZE":
                # screen.y_max, screen.x_max = stdscr.getmaxyx()
                screen.y_max, _ = stdscr.getmaxyx()

    # Handle keybard interruption with ctr+c:
    except KeyboardInterrupt:
        confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
        if confirmed: screen.state = State.EXIT

    # Prevent crash if no input:
    except Exception:
        pass


########################## JOURNAL SCREEN CONTROL ###################################


def control_journal_screen(stdscr, user_tasks, screen):
    '''Process user input on the journal screen'''
    try:
        # If we previously selected a task, now we perform the action:
        if screen.selection_mode:

            # Timer operations:
            if screen.key == 't':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TM_ADD)
                user_tasks.add_timestamp_for_task(number)
            if screen.key == 'T':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TM_RESET)
                user_tasks.reset_timer_for_task(number)

            # Change the status:
            if screen.key in ['i', 'h']:
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_HIGH)
                task_id = user_tasks.items[number].id
                user_tasks.toggle_item_status(task_id, Status.IMPORTANT)
            if screen.key == 'l':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_LOW)
                task_id = user_tasks.items[number].id
                user_tasks.toggle_item_status(task_id, Status.UNIMPORTANT)
            if screen.key == 'u':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_RES)
                task_id = user_tasks.items[number].id
                user_tasks.toggle_item_status(task_id, Status.NORMAL)
            if screen.key == 'v':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_LOW)
                task_id = user_tasks.items[number].id
                user_tasks.toggle_item_status(task_id, Status.DONE)

            # Modify the task:
            if screen.key in ['d', 'x']:
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_DEL)
                task_id = user_tasks.items[number].id
                user_tasks.delete_item(task_id)
            if screen.key == 'm':
                number_from = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_MOVE)
                if user_tasks.is_valid_number(number_from):
                    number_to = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_MOVE_TO)
                    user_tasks.move_task(number_from, number_to)
            if screen.key in ['e', 'c']:
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_EDIT)
                if user_tasks.is_valid_number(number):
                    task_id = user_tasks.items[number].id
                    new_name = input_string(stdscr, number+2, screen.x_min, cf.TODO_ICON+' ', screen.x_max-4)
                    user_tasks.rename_item(task_id, new_name)

            # Subtask operations:
            if screen.key == 's':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_TOG)
                user_tasks.toggle_subtask_state(number)
            if screen.key == 'A':
                number = input_integer(stdscr, screen.y_max-2, 0, MSG_TS_SUB)
                if user_tasks.is_valid_number(number):
                    clear_line(stdscr, screen.y_max-2)
                    task_name = input_string(stdscr, screen.y_max-2, 0, MSG_TS_TITLE, screen.x_max-len(MSG_TS_TITLE)-2)
                    user_tasks.add_subtask(Task(None, task_name, Status.NORMAL, Timer([])), number)
            screen.selection_mode = False

        # Otherwise, we check for user input:
        else:
            # Wait for user to press a key:
            screen.key = stdscr.getkey()

            # If we need to select a task, change to selection mode:
            if screen.key in ['t','T','h','l','v','u','i','s','d','x','e','c','A','m']:
                screen.selection_mode = True

            # Add single task:
            if screen.key == 'a':
                task_name = input_string(stdscr, len(user_tasks.items) + 2, screen.x_min, cf.TODO_ICON+' ', screen.x_max - 4)
                user_tasks.add_item(Task(len(user_tasks.items), task_name, Status.NORMAL, Timer([])))

            # Bulk operations:
            if screen.key == "V":
                user_tasks.change_all_statuses(Status.DONE)
            if screen.key == "U":
                user_tasks.change_all_statuses(Status.NORMAL)
            if screen.key == "L":
                user_tasks.change_all_statuses(Status.UNIMPORTANT)
            if screen.key in ['I','H']:
                user_tasks.change_all_statuses(Status.IMPORTANT)
            if screen.key in ['D','X']:
                confirmed = ask_confirmation(stdscr, MSG_TS_DEL_ALL, cf.ASK_CONFIRMATIONS)
                if confirmed: user_tasks.delete_all_items()

            # Imports:
            if screen.key == "C":
                confirmed = ask_confirmation(stdscr, MSG_TS_IM, cf.ASK_CONFIRMATIONS)
                if confirmed:
                    TasksImporters.import_from_calcurse(user_tasks, cf.CALCURSE_TODO_FILE)
            if screen.key == "W":
                confirmed = ask_confirmation(stdscr, MSG_TS_TW, cf.ASK_CONFIRMATIONS)
                if confirmed:
                    TasksImporters.import_from_taskwarrior(user_tasks, cf.TASKWARRIOR_FOLDER)

            # Other actions:
            if vim_style_exit(stdscr, screen):
                confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
                if confirmed: screen.state = State.EXIT
            if screen.key == "*": screen.privacy = not screen.privacy
            if screen.key in [" ", "KEY_BTAB"]:
                screen.state = State.MONTHLY
            if screen.key == "?":
                screen.state = State.HELP
            if screen.key == "q":
                confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
                if confirmed: screen.state = State.EXIT
            if screen.key in ["/"]:
                screen.split = not screen.split
                screen.refresh_now = True

            # Handle screen resize:
            if screen.key == "KEY_RESIZE":
                # screen.y_max, screen.x_max = stdscr.getmaxyx()
                screen.y_max, _ = stdscr.getmaxyx()

    # Handle keybard interruption with ctr+c:
    except KeyboardInterrupt:
        confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
        if confirmed: screen.state = State.EXIT

    # Prevent crash if no input:
    except Exception:
        pass


########################## HELP SCREEN CONTROL #############################


def control_help_screen(stdscr, screen):
    '''Process user input on the help screen'''
    try:
        # Getting user's input:
        screen.key = stdscr.getkey()

        # Handle vim-style exit on "ZZ" and "ZQ":
        if vim_style_exit(stdscr, screen):
            confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
            if confirmed: screen.state = State.EXIT

        # Handle keys to exit the help screen:
        if screen.key in [" ", "?", "q", "KEY_BACKSPACE", "^[", "\x7f"]:
            screen.state = State.MONTHLY

        # Handle screen resize:
        if screen.key == "KEY_RESIZE":
            # screen.y_max, screen.x_max = stdscr.getmaxyx()
            screen.y_max, _ = stdscr.getmaxyx()

    except KeyboardInterrupt:
        confirmed = ask_confirmation(stdscr, MSG_EXIT, cf.ASK_CONFIRMATIONS)
        if confirmed: screen.state = State.EXIT

    # Prevent crash if no input:
    except Exception:
        pass
