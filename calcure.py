#!/usr/bin/env python
from curses import *
import datetime
import calendar
import csv
import os
import pathlib
import configparser
import subprocess
import re
import sys, getopt
import time

__version__ = "1.7.3"

# Write configuration file if it does not exist already:
config_folder = str(pathlib.Path.home()) + "/.config/calcure"
if not os.path.exists(config_folder):
    os.makedirs(config_folder)
config_file = config_folder + "/config.ini"

# Read config.ini file from user arguments, if provided:
try:
    opts, args = getopt.getopt(sys.argv[1:], "pjchv", ["folder=", "config="])
    for opt, arg in opts:
        if opt in ("--config"):
            config_file = arg
except getopt.GetoptError:
    pass

conf = configparser.ConfigParser()

# Construct strings that will be used in config:
taskwarrior_folder    = str(pathlib.Path.home()) + "/.task"
calcurse_todo_file    = str(pathlib.Path.home()) + "/.local/share/calcurse/todo"
calcurse_events_file  = str(pathlib.Path.home()) + "/.local/share/calcurse/apts"
default_calendar_hint = "Space · Tasks   n/p · Change month   a · Add event   ? · All keybindings"
default_todo_hint     = "Space · Calendar   a · Add   v · Done   i · Important   ? · All keybindings"


def help_screen_info():
    '''Create dictionaries of keybindings to display in help screen'''
    keys_general = {
            ' Space ': 'Switch between calendar and journal',
            '   ?   ': 'Toggle this help',
            '   *   ': 'Toggle privacy mode',
            '   q   ': 'Quit',
            }

    keys_calendar = {
            '  a(A) ': 'Add a (recurring) event',
            '  n,🠒  ': 'Next month (day)',
            '  p,🠐  ': 'Previous month (day)',
            '  d,x  ': 'Delete an event',
            '  e,c  ': 'Edit an event',
            '   g   ': 'Go to a certain day',
            '   h   ': 'Toggle event as high priority',
            '   l   ': 'Toggle event as low priority',
            '   C   ': 'Import events from calcurse',
            '   G   ': 'Return to current month (day)',
            }

    keys_todo = {
            '  a(A) ': 'Add new (sub)task',
            '  h(H) ': 'Toggle one (all) of the tasks as high priority',
            '  l(L) ': 'Toggle one (all) of the tasks as low priority',
            '  v(V) ': 'Toggle one (all) of the tasks as done',
            '  u(U) ': 'Unmark one (all) of the tasks',
            '  d(D) ': 'Delete one (all) of the tasks (with all subtasks)',
            '  t(T) ': 'Start/pause (reset) timer for a task',
            '  e,c  ': 'Edit a task',
            '   s   ': 'Toggle between task and subtask',
            '   m   ': 'Move a task',
            '  C(W) ': 'Import tasks from calcurse (taskwarrior)',
            }
    return keys_general, keys_calendar, keys_todo


def create_config():
    '''Create config.ini file if it does not exist yet'''
    conf["Parameters"] = {
            "folder_with_datafiles":     str(config_folder),
            "calcurse_todo_file":        str(calcurse_todo_file),
            "calcurse_events_file":      str(calcurse_events_file),
            "taskwarrior_folder":        str(taskwarrior_folder),
            "default_view":              "calendar",
            "birthdays_from_abook":      "Yes",
            "show_keybindings":          "Yes",
            "privacy_mode":              "No",
            "show_weather":              "No",
            "weather_city":              "",
            "show_day_names":            "Yes",
            "minimal_today_indicator":   "Yes",
            "minimal_days_indicator":    "Yes",
            "minimal_weekend_indicator": "Yes",
            "cut_titles_by_cell_length": "No",
            "ask_confirmations":         "Yes",
            "use_unicode_icons":         "Yes",
            "show_current_time":         "No",
            "show_holidays":             "Yes",
            "start_week_day":            "1",
            "weekend_days":              "[6,7]",
            "refresh_interval":          "1",
            "event_icon":                "•",
            "privacy_icon":              "•",
            "today_icon":                "•",
            "birthday_icon":             "★",
            "holiday_icon":              "☘️",
            "hidden_icon":               "...",
            "done_icon":                 "✔",
            "todo_icon":                 "•",
            "important_icon":            "‣",
            "timer_icon":                "⌚",
            "show_journal_header":       "Yes",
            "journal_header":            "JOURNAL",
            }

    conf["Colors"] = {
            "color_today":         "2",
            "color_events":        "4",
            "color_days":          "7",
            "color_day_names":     "4",
            "color_weekends":      "1",
            "color_weekend_names": "1",
            "color_hints":         "7",
            "color_prompts":       "7",
            "color_confirmations": "1",
            "color_birthdays":     "1",
            "color_holidays":      "2",
            "color_todo":          "7",
            "color_done":          "6",
            "color_title":         "4",
            "color_important":     "1",
            "color_unimportant":   "6",
            "color_timer":         "2",
            "color_timer_paused":  "7",
            "color_time":          "7",
            "color_weather":       "2",
            "color_background":    "-1",
            }

    conf["Styles"] = {
            "bold_today":               "No",
            "bold_days":                "No",
            "bold_day_names":           "No",
            "bold_weekends":            "No",
            "bold_weekend_names":       "No",
            "bold_title":               "No",
            "underlined_today":         "No",
            "underlined_days":          "No",
            "underlined_day_names":     "No",
            "underlined_weekends":      "No",
            "underlined_weekend_names": "No",
            "underlined_title":         "No",
            }

    conf["Dialogues"] = {
            "calendar_hint": default_calendar_hint,
            "todo_hint": default_todo_hint,
            }

    conf["Event icons"] = {
            "travel":      "✈",
            "plane":       "✈",
            "voyage":      "✈",
            "flight":      "✈",
            "airport":     "✈",
            "trip":        "🏕",
            "vacation":    "⛱",
            "holiday":     "⛱",
            "day-off":     "⛱",
            "hair":        "✂",
            "barber":      "✂",
            "beauty":      "✂",
            "nails":       "✂",
            "game":        "♟",
            "match":       "♟",
            "play":        "♟",
            "interview":   "🎙️",
            "conference":  "🎙️",
            "hearing":     "🎙️",
            "date":        "♥",
            "concert":     "♪",
            "dance":       "♪",
            "music":       "♪",
            "rehersal":    "♪",
            "call":        "🕻",
            "phone":       "🕻",
            "zoom":        "🕻",
            "deadline":    "⚑",
            "over":        "⚑",
            "finish":      "⚑",
            "end":         "⚑",
            "doctor":      "✚",
            "dentist":     "✚",
            "medical":     "✚",
            "hospital":    "✚",
            "party":       "☘",
            "bar":         "☘",
            "museum":      "⛬",
            "meet":        "⛬",
            "talk":        "⛬",
            "sport":       "⛷",
            "gym":         "🏋",
            "training":    "⛷",
            "email":       "✉",
            "letter":      "✉",
            }

    with open(config_file, 'w', encoding="utf-8") as f:
        conf.write(f)

# Load configuration file or create if it does not exist:
if not os.path.exists(config_file):
    create_config()

try:
    # Calendar settings:
    conf.read(config_file, 'utf-8')
    SHOW_KEYBINDINGS          = conf.getboolean("Parameters", "show_keybindings", fallback=True)
    SHOW_DAY_NAMES            = conf.getboolean("Parameters", "show_day_names", fallback=True)
    MINIMAL_TODAY_INDICATOR   = conf.getboolean("Parameters", "minimal_today_indicator", fallback=True)
    MINIMAL_DAYS_INDICATOR    = conf.getboolean("Parameters", "minimal_days_indicator", fallback=True)
    MINIMAL_WEEKEND_INDICATOR = conf.getboolean("Parameters", "minimal_weekend_indicator", fallback=True)
    ASK_CONFIRMATIONS         = conf.getboolean("Parameters", "ask_confirmations", fallback=True)
    SHOW_WEATHER              = conf.getboolean("Parameters", "show_weather", fallback=False)
    SHOW_CURRENT_TIME         = conf.getboolean("Parameters", "show_current_time", fallback=False)
    DISPLAY_ICONS             = conf.getboolean("Parameters", "use_unicode_icons", fallback=True)
    DISPLAY_HOLIDAYS          = conf.getboolean("Parameters", "show_holidays", fallback=True)
    PRIVACY_MODE              = conf.getboolean("Parameters", "privacy_mode", fallback=False)
    CUT_TITLES                = conf.getboolean("Parameters", "cut_titles_by_cell_length", fallback=False)
    BIRTHDAYS_FROM_ABOOK      = conf.getboolean("Parameters", "birthdays_from_abook", fallback=True)
    START_WEEK_DAY            = int(conf.get("Parameters", "start_week_day", fallback=1))
    WEEKEND_DAYS              = conf.get("Parameters", "weekend_days", fallback="6,7")
    WEEKEND_DAYS              = [int(i) for i in WEEKEND_DAYS.split(",")]

    DEFAULT_VIEW     = conf.get("Parameters", "default_view", fallback="calendar")
    HOLIDAY_COUNTRY  = conf.get("Parameters", "holiday_country", fallback="UnitedStates")
    WEATHER_CITY     = conf.get("Parameters", "weather_city", fallback="")
    TODAY_ICON       = conf.get("Parameters", "today_icon", fallback="•") if DISPLAY_ICONS else "·"
    PRIVACY_ICON     = conf.get("Parameters", "privacy_icon", fallback="•") if DISPLAY_ICONS else "·"
    HIDDEN_ICON      = conf.get("Parameters", "hidden_icon", fallback="...")
    EVENT_ICON       = conf.get("Parameters", "event_icon", fallback="•")
    BIRTHDAY_ICON    = conf.get("Parameters", "birthday_icon", fallback="★")
    HOLIDAY_ICON     = conf.get("Parameters", "holiday_icon", fallback="☘️")

    # Journal settings:
    CALCURSE_TODO_FILE   = conf.get("Parameters", "calcurse_todo_file", fallback=calcurse_todo_file)
    CALCURSE_EVENTS_FILE = conf.get("Parameters", "calcurse_events_file", fallback=calcurse_events_file)
    TASKWARRIOR_FOLDER   = conf.get("Parameters", "taskwarrior_folder", fallback=taskwarrior_folder)
    TITLE                = conf.get("Parameters", "jounal_header", fallback="JOURNAL")
    SHOW_TITLE           = conf.getboolean("Parameters", "show_journal_header", fallback=True)
    SHOW_KEYBINDINGS     = conf.getboolean("Parameters", "show_keybindings", fallback=True)
    DONE_ICON            = conf.get("Parameters", "done_icon", fallback="✔") if DISPLAY_ICONS else "×"
    TODO_ICON            = conf.get("Parameters", "todo_icon", fallback="•") if DISPLAY_ICONS else "·"
    IMPORTANT_ICON       = conf.get("Parameters", "important_icon", fallback="‣") if DISPLAY_ICONS else "!"
    TIMER_ICON           = conf.get("Parameters", "timer_icon", fallback="⌚") if DISPLAY_ICONS else "!"
    REFRESH_INTERVAL     = int(conf.get("Parameters", "refresh_interval", fallback=1))

    # Calendar colors:
    COLOR_TODAY          = int(conf.get("Colors", "color_today", fallback=2))
    COLOR_EVENTS         = int(conf.get("Colors", "color_events", fallback=4))
    COLOR_DAYS           = int(conf.get("Colors", "color_days", fallback=7))
    COLOR_DAY_NAMES      = int(conf.get("Colors", "color_day_names", fallback=4))
    COLOR_WEEKENDS       = int(conf.get("Colors", "color_weekends", fallback=1))
    COLOR_WEEKEND_NAMES  = int(conf.get("Colors", "color_weekend_names", fallback=1))
    COLOR_HINTS          = int(conf.get("Colors", "color_hints", fallback=7))
    COLOR_PROMPTS        = int(conf.get("Colors", "color_prompts", fallback=7))
    COLOR_BIRTHDAYS      = int(conf.get("Colors", "color_birthdays", fallback=1))
    COLOR_HOLIDAYS       = int(conf.get("Colors", "color_holidays", fallback=2))
    COLOR_CONFIRMATIONS  = int(conf.get("Colors", "color_confirmations", fallback=1))
    COLOR_TIMER          = int(conf.get("Colors", "color_timer", fallback=2))
    COLOR_TIMER_PAUSED   = int(conf.get("Colors", "color_timer_paused", fallback=7))
    COLOR_TIME           = int(conf.get("Colors", "color_time", fallback=7))
    COLOR_WEATHER        = int(conf.get("Colors", "color_weather", fallback=2))
    COLOR_BACKGROUND     = int(conf.get("Colors", "color_background", fallback=-1))

    # Journal colors:
    COLOR_TODO           = int(conf.get("Colors", "color_todo", fallback=7))
    COLOR_DONE           = int(conf.get("Colors", "color_done", fallback=6))
    COLOR_TITLE          = int(conf.get("Colors", "color_title", fallback=1))
    COLOR_IMPORTANT      = int(conf.get("Colors", "color_important", fallback=1))
    COLOR_UNIMPORTANT    = int(conf.get("Colors", "color_unimportant", fallback=6))

    # Font styles:
    BOLD_TODAY               = conf.getboolean("Styles", "bold_today", fallback=False)
    BOLD_DAYS                = conf.getboolean("Styles", "bold_days", fallback=False)
    BOLD_DAY_NAMES           = conf.getboolean("Styles", "bold_day_names", fallback=False)
    BOLD_WEEKENDS            = conf.getboolean("Styles", "bold_weekends", fallback=False)
    BOLD_WEEKEND_NAMES       = conf.getboolean("Styles", "bold_weekend_names", fallback=False)
    BOLD_TITLE               = conf.getboolean("Styles", "bold_title", fallback=False)
    UNDERLINED_TODAY         = conf.getboolean("Styles", "underlined_today", fallback=False)
    UNDERLINED_DAYS          = conf.getboolean("Styles", "underlined_days", fallback=False)
    UNDERLINED_DAY_NAMES     = conf.getboolean("Styles", "underlined_day_names", fallback=False)
    UNDERLINED_WEEKENDS      = conf.getboolean("Styles", "underlined_weekends", fallback=False)
    UNDERLINED_WEEKEND_NAMES = conf.getboolean("Styles", "underlined_weekend_names", fallback=False)
    UNDERLINED_TITLE         = conf.getboolean("Styles", "underlined_title", fallback=False)

    # Dialogues:
    CALENDAR_HINT = conf.get("Dialogues", "calendar_hint", fallback=default_calendar_hint)
    TODO_HINT     = conf.get("Dialogues", "todo_hint", fallback=default_todo_hint)

    try:
        ICONS = {word: icon for (word, icon) in conf.items("Event icons")}
    except Exception:
        ICONS = {}

    data_folder = conf.get("Parameters", "folder_with_datafiles", fallback=config_folder)
except Exception:
    print("Looks like there is a problem in your config.ini file. Perhaps you edited it and entered a wrong line. Try removing your config.ini file and run the program again, it will create a fresh working config file.")
    exit()

# Read user arguments:
try:
    opts, args = getopt.getopt(sys.argv[1:],"pjchv",["folder=", "config="])
    for opt, arg in opts:
        if opt in ("--folder"):
            data_folder = arg
        elif opt == '-p':
            PRIVACY_MODE = True
        elif opt == '-j':
            DEFAULT_VIEW = 'journal'
        elif opt == '-c':
            DEFAULT_VIEW = 'calendar'
        elif opt in ("-h"):
            DEFAULT_VIEW = 'help'
        elif opt in ("-v"):
            DEFAULT_VIEW = 'version'
            print ("Calcure - version " + __version__)
except getopt.GetoptError:
    pass

# Assigning data files:
EVENTS_FILE = data_folder + "/events.csv"
TASKS_FILE = data_folder + "/tasks.csv"
if not os.path.exists(data_folder):
    os.makedirs(data_folder)


def load_holidays(year):
    '''Load list of holidays in this country around this year'''
    try:
        import holidays
        holidays = eval("holidays."+HOLIDAY_COUNTRY+"(years=[year-1, year, year+1])")
    except ModuleNotFoundError:
        holidays = None
    except SyntaxError:
        holidays = None
    except AttributeError:
        holidays = None
    return holidays


def import_events_from_calcurse():
    '''Importing events from calcurse apt file into our events file'''
    events = load_events()
    with open(CALCURSE_EVENTS_FILE, "r") as f:
        lines = f.readlines()
    for index, line in enumerate(lines):
        month = line[0:2]
        day = line[3:5]
        year = line[6:10]
        if line[11] == "[":
            name = line[15:-1]
        elif line[11] == "@":
            name = line[35:-1]
            name = name.replace('|',' ')
        event_id = 1 if not events['id'] else max(events['id'])+1
        new_event = str(event_id+index)+","+year+","+month+","+day+","+'"'+name+'"'+',1,n'
        with open(EVENTS_FILE, "a") as f:
            f.write(new_event+"\n")


def parse_birthdays_from_abook():
    '''Loading birthdays from abook contacts'''
    if BIRTHDAYS_FROM_ABOOK:
        abook_file = str(pathlib.Path.home())+"/.abook/addressbook"
        bd_names, bd_dates = [], []
        abook = configparser.ConfigParser()
        abook.read(abook_file)
        for each_contact in abook.sections():
            for (key, value) in abook.items(each_contact):
                if key == "birthday":
                    bd_names.append(abook[each_contact]["name"])
                    bd_month = int(abook[each_contact]["birthday"][-5:-3])
                    bd_day = int(abook[each_contact]["birthday"][-2:])
                    bd_dates.append(datetime.date(1, bd_month, bd_day))
    return bd_dates, bd_names


def calculate_recurring_events(year, month, day, fr):
    '''Calculate the date of recurring events so that they occur in the next month or year'''
    new_day   = day
    new_month = month
    new_year  = year
    skip_days = 0

    # Weekly and daily recurrence:
    if fr in ["w","d"]:
        for i in range(1000):
            if month + i > 12:
                year = year + 1
                month = month - 12
            if day > skip_days + calendar.monthrange(year, month + i)[1]:
                skip_days += calendar.monthrange(year, month + i)[1]
                skip_months = i + 1
            else:
                skip_months = i
                break
        new_day = day - skip_days
        new_month = month + skip_months
        new_year = year

    # Monthly recurrence:
    if fr == "m":
        if month > 12:
            new_year = year + (month-1)//12
            new_month = month - 12*(new_year-year)
    return datetime.date(new_year, new_month, new_day)


def load_events():
    '''Read from user's events file or create it if it does not exist'''
    try:
        with open(EVENTS_FILE) as f:
            pass
    except IOError:
        with open(EVENTS_FILE, "w+") as f:
            pass

    with open(EVENTS_FILE, "r") as f:
        lines = csv.reader(f, delimiter = ',')
        ids, dates, names, statuses = [], [], [], []
        try:
            for line in lines:
                repetitions = int(line[5])

                # For recurring events, each repetition becomes an event in the memory:
                for r in range(repetitions):
                    try:
                        ids.append(int(line[0]))
                        fr = line[6]
                        year  = int(line[1]) + r*(fr=='y')
                        month = int(line[2]) + r*(fr=='m')
                        day   = int(line[3]) + r*(fr=='d') + 7*r*(fr=='w')
                        event_date = calculate_recurring_events(year, month, day, fr)
                        dates.append(event_date)
                        names.append(line[4])

                        status = 'normal' if len(line) < 8 else line [7]
                        statuses.append(status)
                    except Exception:
                        pass
        except Exception:
            pass
        events = {'id': ids, 'dates': dates, 'names': names, 'statuses': statuses}
    return events


def add_event(stdscr, day, month, year, recurring):
    '''Ask user to input new event and add it the file'''
    y_max, x_max = stdscr.getmaxyx()

    if day == None:
        add_prompt = "Enter the date: "+str(year)+"/"+str(month)+"/"
        event_date = int(user_input(stdscr, add_prompt, 2))
    else:
        event_date = day

    # If user's date is the number and is in this month, ask the title:
    days_of_this_month = range(1, calendar.monthrange(year, month)[1]+1)
    if event_date in days_of_this_month:
        title_prompt = "Enter the title: "
        name = user_input(stdscr, title_prompt, x_max-len(title_prompt)-2)

        if recurring:
            rep_prompt = "How many times repeat the event: "
            repetitions = user_input(stdscr, rep_prompt, 3)
            freq_prompt = "Repeat the event every (d)ay, (w)eek, (m)onth or (y)ear?"
            prompt = freq_prompt + " "*abs(x_max - len(freq_prompt) - 1)
            stdscr.addstr(y_max-2, 0, prompt[:x_max-1], color_pair(8))
            frequency = stdscr.getkey()
        else:
            repetitions = 1
            frequency = "n"

        events = load_events()
        event_id = 1 if not events['id'] else max(events['id']) + 1
        new_event = (str(event_id)+","+str(year)+","+str(month)+","+
                str(event_date)+","+'"'+name+'"'+","+str(repetitions)+","+
                str(frequency))+",normal"
        if len(name) > 0 and int(repetitions) >= 0 and frequency in ["d","w","m","y","n"]:
            with open(EVENTS_FILE, "a") as f:
                f.write(new_event+"\n")


def delete_event(stdscr, ids_this_month, names_this_month):
    '''Delete chosen events'''
    y_max, x_max = stdscr.getmaxyx()
    prompt_string = "Number of event to delete: "
    try:
        # Ask which event to delete:
        num = user_input(stdscr, prompt_string, 4)
        if int(num) in range(1, len(ids_this_month)+1):

            # Ask confirmation:
            event_id = ids_this_month[int(num)-1]
            event_name = names_this_month[int(num)-1]
            prompt_string = "Really delete "+event_name+"? (y/n)"
            confirmed = ask_confirmation(stdscr, prompt_string)

            # Delete the event if it was confirmed:
            if confirmed:
                original_file = EVENTS_FILE
                dummy_file = EVENTS_FILE + '.bak'
                line_deleted = False
                with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
                    for line in read_obj:
                        if line.startswith(str(event_id)+',') == False:
                            write_obj.write(line)
                        else:
                            line_deleted = True
                if line_deleted:
                    os.remove(original_file)
                    os.rename(dummy_file, original_file)
                else:
                    os.remove(dummy_file)
    except:
        pass


def mark_event_as_important(stdscr, ids_this_month, names_this_month, month, year):
    '''Mark existing event as important'''
    y_max, x_max = stdscr.getmaxyx()
    prompt_string = "Mark as high priority event number: "
    num = (user_input(stdscr, prompt_string, 4))
    event_chosen = False

    # If provided number is correct, then change the status:
    try:
        if int(num) in range(1, len(ids_this_month)+1):
            recurring = True
            event_id = ids_this_month[int(num)-1]
            event_name = names_this_month[int(num)-1]

            # Here we work with a dummy file and replace the original in the last moment:
            original_file = EVENTS_FILE
            dummy_file = EVENTS_FILE + '.bak'
            line_deleted = False
            with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
                for line in read_obj:
                    if not line.startswith(str(event_id)+','):
                        write_obj.write(line)
                    else:
                        if line[:-1].endswith(",important"):
                            line = re.sub(',important', ',normal', line)
                        elif line[:-1].endswith(",unimportant"):
                            line = re.sub(',unimportant', ',important', line)
                        elif line[:-1].endswith(",normal"):
                            line = re.sub(',normal', ',important', line)
                        else:
                            line = line[:-1] + ',important\n'
                        write_obj.write(line)
                        line_edited = True
            if line_edited:
                os.remove(original_file)
                os.rename(dummy_file, original_file)
            else:
                os.remove(dummy_file)
    except:
        pass


def mark_event_as_unimportant(stdscr, ids_this_month, names_this_month, month, year):
    '''Mark existing event as unimportant'''
    y_max, x_max = stdscr.getmaxyx()
    prompt_string = "Mark as low priority event number: "
    num = (user_input(stdscr, prompt_string, 4))
    event_chosen = False

    # If provided number is correct, then change the status:
    try:
        if int(num) in range(1, len(ids_this_month)+1):
            recurring = True
            event_id = ids_this_month[int(num)-1]
            event_name = names_this_month[int(num)-1]

            # Here we work with a dummy file and replace the original in the last moment:
            original_file = EVENTS_FILE
            dummy_file = EVENTS_FILE + '.bak'
            line_deleted = False
            with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
                for line in read_obj:
                    if not line.startswith(str(event_id)+','):
                        write_obj.write(line)
                    else:
                        if line[:-1].endswith(",unimportant"):
                            line = re.sub(',unimportant', ',normal', line)
                        elif line[:-1].endswith(",important"):
                            line = re.sub(',important', ',unimportant', line)
                        elif line[:-1].endswith(",normal"):
                            line = re.sub(',normal', ',unimportant', line)
                        else:
                            line = line[:-1] + ',unimportant\n'
                        write_obj.write(line)
                        line_edited = True
            if line_edited:
                os.remove(original_file)
                os.rename(dummy_file, original_file)
            else:
                os.remove(dummy_file)
    except:
        pass


def edit_event(stdscr, ids_this_month, names_this_month, month, year):
    '''Edit chosen event via deleting it and creating a new one'''
    y_max, x_max = stdscr.getmaxyx()
    prompt_string = "Number of event to edit: "
    num = (user_input(stdscr, prompt_string, 4))
    event_chosen = False

    # If provided number is correct, then delete the event:
    try:
        if int(num) in range(1, len(ids_this_month)+1):
            recurring = True
            event_id = ids_this_month[int(num)-1]
            event_name = names_this_month[int(num)-1]
            prompt_string = "Really edit " + event_name + "? (y/n)"
            confirmed = ask_confirmation(stdscr, prompt_string)
            if confirmed:
                original_file = EVENTS_FILE
                dummy_file = EVENTS_FILE + '.bak'
                line_deleted = False
                with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
                    for line in read_obj:
                        if not line.startswith(str(event_id)+','):
                            write_obj.write(line)
                        else:
                            line_deleted = True
                if line_deleted:
                    os.remove(original_file)
                    os.rename(dummy_file, original_file)
                else:
                    os.remove(dummy_file)
                event_chosen = True
    except:
        pass

    if event_chosen:
        # First, ask the date within this month:
        add_prompt = "Enter new date: " + str(year) + "/" + str(month) + "/"
        event_date = user_input(stdscr, add_prompt, 2)

        # If user's date is the number and is in this month, ask the title:
        try:
            days_this_month = range(1, calendar.monthrange(year, month)[1]+1)
            if int(event_date) in days_this_month:
                title_prompt = "Enter new title: "
                name = user_input(stdscr, title_prompt, x_max-len(title_prompt)-2)

                rep_prompt = "How many times repeat the event: "
                repetitions = user_input(stdscr, rep_prompt, 3)
                freq_prompt = "Repeat the event every (d)ay, (w)eek, (m)onth or (y)ear?"
                prompt = freq_prompt + " "*abs(x_max - len(freq_prompt) - 1)
                stdscr.addstr(y_max-2, 0, prompt[:x_max-1], color_pair(8))
                frequency = stdscr.getkey()

                events = load_events()
                event_id = 1 if not events['id'] else max(events['id'])+1
                new_event = (str(event_id)+","+str(year)+","+str(month)+","+
                        event_date+","+'"'+name+'"'+","+str(repetitions)+","+str(frequency)+",normal")
                if len(name) > 0 and int(repetitions) >= 0 and frequency in ["d","w","m","y","n"]:
                    with open(EVENTS_FILE, "a") as f:
                        f.write(new_event+"\n")
        except:
            pass


def user_input(stdscr, prompt_string, answer_length):
    '''Ask user to input something and return this string'''
    y_max, x_max = stdscr.getmaxyx()
    echo()
    curs_set(True)
    display_string = str(prompt_string) + " "*abs((x_max-len(prompt_string))-1)
    stdscr.addstr(y_max - 2, 0, display_string[:x_max-1], color_pair(8))
    stdscr.refresh()
    user_input = stdscr.getstr(y_max - 2, len(prompt_string), answer_length).decode(encoding="utf-8")
    noecho()
    curs_set(False)
    return user_input


def user_input_for_tasks(stdscr, prompt_string, answer_length, task_number, subtask=False):
    '''Ask user to input task at the location where the task is displayed'''
    y_max, x_max = stdscr.getmaxyx()
    echo()
    curs_set(True)
    display_string = str(prompt_string) + " "*abs((x_max-len(prompt_string))-1)
    line_number = task_number - 1 + 2*SHOW_TITLE
    stdscr.addstr(line_number, 2*subtask, display_string[:x_max-1], color_pair(8))
    stdscr.refresh()
    user_input = stdscr.getstr(line_number, len(prompt_string)+2*subtask, answer_length).decode(encoding="utf-8")
    noecho()
    curs_set(False)
    return user_input


def display_line(stdscr, y, x, text, color, bold=False, underlined=False):
    '''Display the line of text respecting the slyling'''
    if bold and underlined:
        stdscr.addstr(y, x, text, color_pair(color) | A_BOLD | A_UNDERLINE)
    elif bold and not underlined:
        stdscr.addstr(y, x, text, color_pair(color) | A_BOLD)
    elif underlined and not bold:
        stdscr.addstr(y, x, text, color_pair(color) | A_UNDERLINE)
    else:
        stdscr.addstr(y, x, text, color_pair(color))


def display_day_names(stdscr, x_max):
    '''Display day name depending on the screen available and with right style'''
    num = 2 if x_max < 80 else 10
    x_cell = int(x_max//7)
    # Depending on which day is the start of the week, weekends are shifted:
    for i in range(7):
        shift = START_WEEK_DAY-1
        day_number = i + shift - 7*((i+shift) > 6)
        name = calendar.day_name[day_number][:num].upper()
        if day_number + 1 not in WEEKEND_DAYS:
            display_line(stdscr, 1, i*x_cell, name, 1, BOLD_DAY_NAMES, UNDERLINED_DAY_NAMES)
        else:
            display_line(stdscr, 1, i*x_cell, name, 6, BOLD_WEEKEND_NAMES, UNDERLINED_WEEKEND_NAMES)


def display_icon(name, screen, selection_mode=False):
    '''Check if event name contains a keyword and return corresponding icon'''
    if not selection_mode and DISPLAY_ICONS:
        icon = EVENT_ICON + " "
        for keyword in ICONS:
            if keyword in name.lower():
                icon = ICONS[keyword] + " "
    elif screen == "journal":
        icon = "·"
    else:
        icon = ""
    return icon


def ask_confirmation(stdscr, prompt_string):
    '''Ask user confirmation for an action'''
    y_max, x_max = stdscr.getmaxyx()
    confirmed = True
    if ASK_CONFIRMATIONS:
        halfdelay(255)
        prompt = prompt_string + " "*abs(x_max - len(prompt_string) - 1)
        stdscr.addstr(y_max-2, 0, prompt[:x_max-1], color_pair(9))
        key = stdscr.getkey()
        confirmed = True if key == "y" else False
    return confirmed


def initialize_colors(stdscr):
    '''Define all the color pairs'''
    start_color()
    use_default_colors()
    init_pair(1, COLOR_DAY_NAMES, COLOR_BACKGROUND)
    init_pair(6, COLOR_WEEKEND_NAMES, COLOR_BACKGROUND)
    init_pair(3, COLOR_HINTS, COLOR_BACKGROUND)
    init_pair(7, COLOR_BIRTHDAYS, COLOR_BACKGROUND)
    init_pair(8, COLOR_PROMPTS, COLOR_BACKGROUND)
    init_pair(9, COLOR_CONFIRMATIONS, COLOR_BACKGROUND)
    if MINIMAL_WEEKEND_INDICATOR:
        init_pair(2, COLOR_WEEKENDS, COLOR_BACKGROUND)
    else:
        init_pair(2, COLOR_BLACK, COLOR_WEEKENDS)
    if MINIMAL_TODAY_INDICATOR:
        init_pair(4, COLOR_TODAY, COLOR_BACKGROUND)
    else:
        init_pair(4, COLOR_BLACK, COLOR_TODAY)
    if MINIMAL_DAYS_INDICATOR:
        init_pair(5, COLOR_DAYS, COLOR_BACKGROUND)
    else:
        init_pair(5, COLOR_BLACK, COLOR_DAYS)
    init_pair(10, COLOR_TITLE, COLOR_BACKGROUND)
    init_pair(11, COLOR_TODO, COLOR_BACKGROUND)
    init_pair(12, COLOR_DONE, COLOR_BACKGROUND)
    init_pair(13, COLOR_IMPORTANT, COLOR_BACKGROUND)
    init_pair(14, COLOR_TIMER, COLOR_BACKGROUND)
    init_pair(15, COLOR_TIMER_PAUSED, COLOR_BACKGROUND)
    init_pair(16, COLOR_HOLIDAYS, COLOR_BACKGROUND)
    init_pair(17, COLOR_EVENTS, COLOR_BACKGROUND)
    init_pair(18, COLOR_TIME, COLOR_BACKGROUND)
    init_pair(19, COLOR_WEATHER, COLOR_BACKGROUND)
    init_pair(20, COLOR_UNIMPORTANT, COLOR_BACKGROUND)


class Weather():

    def __init__(self):
        self.loaded = False
        self.forcast = " "

    def display(self, stdscr, month_year_string):
        '''Load the weather at launch and display weather widget.'''
        _, x_max = stdscr.getmaxyx()

        # If weather is not yet loaded, show the loading icon and load weather:
        if not self.loaded:
            stdscr.addstr(0, x_max - 2, "·", color_pair(19))
            stdscr.refresh()
            try:
                max_load_time = 2
                request_url = f"wttr.in/{WEATHER_CITY}?format=3"
                self.forcast = str(subprocess.check_output(["curl", "-s", request_url],
                              timeout=max_load_time, encoding='utf-8'))[:-1]
                self.forcast = self.forcast.split(':')[1]
                self.loaded = True
            except Exception:
                pass

        # Display the weather if space allows:
        if len(self.forcast) < x_max - len(month_year_string):
            stdscr.addstr(0, x_max - len(self.forcast) - 0, self.forcast, color_pair(19))


def load_tasks():
    '''Reads from the user's appointments file'''
    # Create the file if it does not exist:
    try:
        with open(TASKS_FILE) as f:
            pass
    except IOError:
        with open(TASKS_FILE, "w+") as f:
            pass

    # Read the file:
    with open(TASKS_FILE,"r") as f:
        lines = csv.reader(f, delimiter = ',')
        tasks = []
        statuses = []
        timestamps = []

        for row in lines:
            tasks.append(row[0])
            statuses.append(row[1])
            if len(row) > 2:
                timestamps.append(row[2:])
            else:
                timestamps.append([])
    return tasks, statuses, timestamps


def add_task(stdscr, tasks):
    '''Ask the user to input new task and adds it to the file'''
    y_max, x_max = stdscr.getmaxyx()
    prompt_string = " " + TODO_ICON + " "
    new_task = user_input_for_tasks(stdscr, prompt_string, x_max - 1, len(tasks) + 1)
    if len(new_task) > 0:
        with open(TASKS_FILE, "a") as f:
            f.write(f'"{new_task}",todo\n')


def add_subtask(stdscr, tasks, statuses, timestamps):
    '''Ask the user to input a subtask for existing task and adds it to the file'''
    y_max, x_max = stdscr.getmaxyx()

    # Display task numbers and ask to which add a subtask:
    shift = 2 if SHOW_TITLE else 0
    for	i in range(len(tasks)):
        col = 1 if i+1 < 10 else 0
        stdscr.addstr(shift+i, col, str(i+1))
    prompt_string = "Add subtask for number: "
    number = user_input(stdscr, prompt_string, 4)

    # If the provided number corresponds to a task, then edit:
    if number_is_valid(number, tasks):
        number = int(number)
        level = '----'if (tasks[number-1][:2] == '--') else '--'
        prompt_string = "Enter the subtask: "
        new_task = user_input(stdscr, prompt_string, x_max - 1)
        if len(new_task) > 0:
            tasks.insert(number, level + new_task)
            statuses.insert(number, statuses[number-1])
            timestamps.insert(number, [])
            write_tasks_file(tasks, statuses, timestamps)


def toggle_subtask(stdscr, tasks, statuses, timestamps):
    '''Toggle between task and subtask state'''
    y_max, x_max = stdscr.getmaxyx()
    shift = 2 if SHOW_TITLE else 0
    for	i in range(len(tasks)):
        col = 1 if i + 1 < 10 else 0
        stdscr.addstr(shift+i, col, str(i+1))
    prompt_string = "Which (sub)task to toggle: "
    number = user_input(stdscr, prompt_string, 4)
    if number_is_valid(number, tasks):
        number = int(number)
        if tasks[number-1][:2] == '--':
            tasks[number-1] = tasks[number-1][2:]
        else:
            tasks[number-1] = '--' + tasks[number-1]
        write_tasks_file(tasks, statuses, timestamps)


def delete_all_tasks(stdscr):
    '''Delete all the tasks'''
    y_max, x_max = stdscr.getmaxyx()
    prompt_string = "Really delete all tasks? (y/n) "
    confirmed = ask_confirmation(stdscr, prompt_string)
    if confirmed:
        write_tasks_file([], [], [])


def calcurse_task_import(stdscr, tasks):
    '''Import todo events from calcurse database'''
    y_max, _ = stdscr.getmaxyx()
    prompt_string = "Import tasks from calcurse? (y/n) "
    confirmed = ask_confirmation(stdscr, prompt_string)
    if confirmed:
        with open(CALCURSE_TODO_FILE, 'r') as f:
            for task in f.readlines():
                if len(task) > 0:
                    if task[4:-1] not in tasks:
                        with open(TASKS_FILE,"a") as f:
                            if task[1] in ['1','2']:
                                f.write('"'+task[4:-1]+'"' + ",important\n")
                            elif task[1] in ['8','9','10']:
                                f.write('"'+task[4:-1]+'"' + ",unimportant\n")
                            else:
                                f.write('"'+task[4:-1]+'"' + ",todo\n")


def taskwarrior_task_import(stdscr, tasks):
    '''Import tasks from taskwarrior database'''
    y_max, _ = stdscr.getmaxyx()
    prompt_string = "Import tasks from taskwarrior? (y/n) "
    confirmed = ask_confirmation(stdscr, prompt_string)
    if confirmed:
        with open(taskwarrior_folder+"/pending.data", 'r') as f:
            for task in f.readlines():
                if len(task) > 0:
                    task = task.split('description:"',1)[1]
                    task = task.split('"',1)[0]
                    if task not in tasks:
                        with open(TASKS_FILE,"a") as f:
                            f.write('"'+task+'"' + ",todo\n")


def delete_task(stdscr, tasks, statuses, timestamps):
    '''Ask the user which task to delete and change the file'''
    y_max, x_max = stdscr.getmaxyx()
    shift = 2 if SHOW_TITLE else 0
    for	i in range(len(tasks)):
        col = 1 if i+1 < 10 else 0
        stdscr.addstr(shift+i, col, str(i+1))
    prompt_string = "Delete task number: "
    number = user_input(stdscr, prompt_string, 4)

    # If the provided number corresponds to a task, then delete:
    if number_is_valid(number, tasks):
        number = int(number)
        prompt_string = "Really delete this task? (y/n) "
        confirmed = ask_confirmation(stdscr, prompt_string)
        if confirmed:
            to_delete = [number-1]
            # Mark subtasks to be deleted as well:
            if tasks[number-1][:2] != '--':
                for i in range(number, len(tasks)):
                    if tasks[i][:2] == '--':
                        to_delete.append(i)
                    else:
                        break
            # Delete marked tasks:
            for index in reversed(to_delete):
                del tasks[index]
                del statuses[index]
                del timestamps[index]
            write_tasks_file(tasks, statuses, timestamps)


def edit_task(stdscr, tasks, statuses, timestamps):
    '''Ask the user which task to delete and change the file'''
    y_max, x_max = stdscr.getmaxyx()

    # Display task numbers and ask which to edit:
    shift = 2 if SHOW_TITLE else 0
    for	i in range(len(tasks)):
        col = 1 if i+1 < 10 else 0
        stdscr.addstr(shift+i, col, str(i+1))
    prompt_string = "Edit task number: "
    number = user_input(stdscr, prompt_string, 4)

    # If the provided number corresponds to a task, then edit:
    if number_is_valid(number, tasks):
        number = int(number)
        tab = "   " if tasks[number-1][:2] == "--"  else " "
        prompt_string = tab + TODO_ICON + " "
        new_task = user_input_for_tasks(stdscr, prompt_string, x_max - 1, number)
        if len(new_task) > 0:
            if tasks[number-1][:2] == "--":
                new_task = "--"+new_task
            tasks[number-1] = new_task
            write_tasks_file(tasks, statuses, timestamps)


def move_task(stdscr, tasks, statuses, timestamps):
    '''Ask the user which task to move and where'''
    y_max, x_max = stdscr.getmaxyx()

    # Display task numbers and ask which to edit:
    shift = 2 if SHOW_TITLE else 0
    for	i in range(len(tasks)):
        col = 1 if i+1 < 10 else 0
        stdscr.addstr(shift+i, col, str(i+1))
    prompt_string = "Move task number: "
    move_from = user_input(stdscr, prompt_string, 4)

    # If the provided number corresponds to a task, then ask where to move:
    if number_is_valid(move_from, tasks):
        move_from = int(move_from)
        prompt_string = "Move to the position number: "
        move_to = user_input(stdscr, prompt_string, 4)
        if number_is_valid(move_to, tasks):
            move_to = int(move_to)
            tasks.insert(move_to-1, tasks.pop(move_from-1))
            statuses.insert(move_to-1, statuses.pop(move_from-1))
            timestamps.insert(move_to-1, timestamps.pop(move_from-1))
            write_tasks_file(tasks, statuses, timestamps)


def number_is_valid(number, tasks):
    '''Check if input is integer and corresponds to a task'''
    try:
        number = int(number)
        if 0 < number <= len(tasks):
            return True
        else:
            return False
    except ValueError:
        return False


def mark_as_done(stdscr, tasks, statuses, timestamps):
    '''Ask user which task to mark as done and change the file'''
    y_max, x_max = stdscr.getmaxyx()

    # Display task numbers and ask which to edit:
    shift = 2 if SHOW_TITLE else 0
    for	i in range(len(tasks)):
        col = 1 if i+1 < 10 else 0
        stdscr.addstr(shift+i, col, str(i+1))
    prompt_string = "Mark as done task number: "
    number = user_input(stdscr, prompt_string, 4)

    # If the provided number corresponds to a task, then edit:
    if number_is_valid(number, tasks):
        number = int(number)
        statuses[number-1] = "done"

        # if there are subtasks, mark them as well:
        if tasks[number-1][:2] != '--':
            for i in range(number, len(tasks)):
                if tasks[i][:2] == '--':
                    statuses[i] = "done"
                else:
                    break
        write_tasks_file(tasks, statuses, timestamps)


def mark_as_important(stdscr, tasks, statuses, timestamps):
    '''Ask user which task to mark as done and changes the file'''
    y_max, x_max = stdscr.getmaxyx()

    # Display task numbers and ask which to edit:
    shift = 2 if SHOW_TITLE else 0
    for	i in range(len(tasks)):
        col = 1 if i+1 < 10 else 0
        stdscr.addstr(shift+i, col, str(i+1))
    prompt_string = "Mark as high priority task number: "
    number = user_input(stdscr, prompt_string, 4)

    # If the provided number corresponds to a task, then edit:
    if number_is_valid(number, tasks):
        number = int(number)
        if statuses[number-1] != "important":
            statuses[number-1] = "important"
        else:
            statuses[number-1] = "todo"

        # if there are subtasks, mark them as well:
        if tasks[number-1][:2] != '--':
            for i in range(number, len(tasks)):
                if tasks[i][:2] == '--':
                    if statuses[i] != "important":
                        statuses[i] = "important"
                    else:
                        statuses[i] = "todo"
                else:
                    break
        write_tasks_file(tasks, statuses, timestamps)


def mark_as_unimportant(stdscr, tasks, statuses, timestamps):
    '''Ask user which task to mark as unimportant and changes the file'''
    y_max, x_max = stdscr.getmaxyx()

    # Display task numbers and ask which to edit:
    shift = 2 if SHOW_TITLE else 0
    for	i in range(len(tasks)):
        col = 1 if i+1 < 10 else 0
        stdscr.addstr(shift+i, col, str(i+1))
    prompt_string = "Mark as low priority task number: "
    number = user_input(stdscr, prompt_string, 4)

    # If the provided number corresponds to a task, then edit:
    if number_is_valid(number, tasks):
        number = int(number)
        if statuses[number-1] != "unimportant":
            statuses[number-1] = "unimportant"
        else:
            statuses[number-1] = "todo"

        # if there are subtasks, mark them as well:
        if tasks[number-1][:2] != '--':
            for i in range(number, len(tasks)):
                if tasks[i][:2] == '--':
                    if statuses[i] != "unimportant":
                        statuses[i] = "unimportant"
                    else:
                        statuses[i] = "todo"
                else:
                    break
        write_tasks_file(tasks, statuses, timestamps)


def unmark_task(stdscr, tasks, statuses, timestamps):
    '''Ask user which task to unmark and rewrite the file'''
    # Display task numbers and ask which to edit:
    shift = 2 if SHOW_TITLE else 0
    for	i in range(len(tasks)):
        col = 1 if i+1 < 10 else 0
        stdscr.addstr(shift+i, col, str(i+1))
    prompt_string = "Unmark task number: "
    number = user_input(stdscr, prompt_string, 4)

    # If the provided number corresponds to a task, then edit:
    if number_is_valid(number, tasks):
        number = int(number)
        statuses[number-1] = "todo"

        # if there are subtasks, unmark them as well:
        if tasks[number-1][:2] != '--':
            for i in range(number, len(tasks)):
                if tasks[i][:2] == '--':
                    statuses[i] = "todo"
                else:
                    break
        write_tasks_file(tasks, statuses, timestamps)


def vim_style_exit(stdscr, state, key):
    '''Handle vim style key combinations like "ZZ" and "ZQ" for exit'''
    if key == "Z":
        try:
            key = stdscr.getkey()
            if key in ["Z", "Q"]:
                prompt_string = "Really exit? (y/n)"
                confirmed = ask_confirmation(stdscr, prompt_string)
                if confirmed:
                    state = 'exit'
        except KeyboardInterrupt:
            screen.state = 'exit'
        except Exception:
            pass
    return state


def reset_timer(stdscr, tasks, statuses, timestamps):
    '''Ask user which task to timer to reset and rewrite the file'''
    # Display task numbers and ask which to edit:
    shift = 2 if SHOW_TITLE else 0
    for	i in range(len(tasks)):
        col = 1 if i+1 < 10 else 0
        stdscr.addstr(shift+i, col, str(i+1))
    prompt_string = "Remove timer for task number: "
    number = user_input(stdscr, prompt_string, 4)

    # If the provided number corresponds to a task, then remove timestamps:
    if number_is_valid(number, tasks):
        number = int(number)
        prompt_string = "Really remove the timer? (y/n) "
        confirmed = ask_confirmation(stdscr, prompt_string)
        if confirmed:
            timestamps[number-1] = []
            write_tasks_file(tasks, statuses, timestamps)


def write_tasks_file(tasks, statuses, timestamps):
    '''Rewrite the database file with changed tasks, statuses, and timers'''
    original_file = TASKS_FILE
    dummy_file = TASKS_FILE + '.bak'
    with open(dummy_file, "w") as f:
        for task, status, timestamp in zip(tasks, statuses, timestamps):
            f.write(f'"{task}",{status}')
            for stamp in timestamp:
                f.write(f',{str(stamp)}')
            f.write("\n")
    os.remove(original_file)
    os.rename(dummy_file, original_file)


def add_timestamp(stdscr, tasks, statuses, timestamps):
    '''Ask user for which task to add timer and change the file'''
    # Display task numbers and ask which to edit:
    shift = 2 if SHOW_TITLE else 0
    for	i in range(len(tasks)):
        col = 1 if i+1 < 10 else 0
        stdscr.addstr(shift+i, col, str(i+1))
    prompt_string = "Add/Pause timer for task number: "
    number = user_input(stdscr, prompt_string, 4)

    # If the provided number corresponds to a task, then add timestamp:
    if number_is_valid(number, tasks):
        number = int(number)
        timestamps[number-1].append(int(time.time()))
        write_tasks_file(tasks, statuses, timestamps)


def calculate_passed_time(times, curently_counting):
    '''Calculate how much time passed in the unpaused intervals'''
    time_passed = 0

    # Calculate passed time, assuming that even timestamps are pauses:
    for index, _ in enumerate(times):
        if index > 0 and index%2 == 1:
            time_passed += float(times[index]) - float(times[index-1])

    # Add time passed during the current run:
    if curently_counting:
        time_passed += time.time() - float(times[-1])

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
    if curently_counting == False and DISPLAY_ICONS:
        time_string = "⏯︎ " + time_string
    elif curently_counting == True and DISPLAY_ICONS:
        time_string = "⏵ " + time_string
    return time_string


def display_time(stdscr, month_year_string):
    '''Show the widget with current time if space allows'''
    _, x_max   = stdscr.getmaxyx()
    if SHOW_CURRENT_TIME and (x_max > 2*len(month_year_string) + 6):
        time_string = time.strftime("%H:%M", time.localtime())
        stdscr.addstr(0, x_max//2-2, time_string, color_pair(18))


def reset_to_today(screen):
    '''Reset the day, month, and year to the current date'''
    today = datetime.date.today()
    screen.month = today.month
    screen.year  = today.year
    screen.day   = int(today.day)
    return screen


def fill_background(stdscr):
    '''Fill the background with background color'''
    y_max, x_max = stdscr.getmaxyx()
    for index in range(y_max-1):
        stdscr.addstr(index, 0, " "*x_max, color_pair(1))


def check_color(status):
    '''Provide color according to the status of importance'''
    if status == 'important':
        color = 13
    elif status == 'unimportant':
        color = 20
    else:
        color = 17
    return color


def draw_daily_screen(stdscr, screen, weather):
    '''This is the daily view that shows event of the day'''
    bd_dates, bd_names = parse_birthdays_from_abook()
    today          = datetime.date.today()
    holidays       = load_holidays(screen.year)

    stdscr.clear()
    halfdelay(255)
    noecho()
    curs_set(False)
    fill_background(stdscr)
    events = load_events()
    dates = calendar.Calendar(firstweekday=START_WEEK_DAY-1).monthdayscalendar(screen.year, screen.month)
    month_year_string = str(calendar.month_name[screen.month].upper()) + " " + str(screen.year)

    # Display month, year, and days of the week with appropriate color:
    if datetime.date(screen.year, screen.month, screen.day) == today:
        color = 4
        icon = " " + TODAY_ICON
    else:
        color = 5
        icon = ""
    date_string = (str(calendar.month_name[screen.month].upper()) + " " + str(screen.day) +
                        ", " + str(screen.year) + icon)
    stdscr.addstr(0, 0, date_string[:screen.x_max], color_pair(color))

    # Display events of this day:
    ids_this_month = []
    names_this_month = []
    event_number = 0
    num_of_event_this_day = 0
    for event_id, event_date, event_name, event_status in zip(events['id'],
            events['dates'], events['names'], events['statuses']):

        # Check if this event happens on this day, and screen space is okay:
        if datetime.date(screen.year, screen.month, screen.day) == event_date:
            if num_of_event_this_day < screen.y_max - 3:
                icon = display_icon(event_name, "calendar", screen.selection_mode)

                # Check if this is a recurring event:
                if event_id in ids_this_month:
                    event_number = ids_this_month.index(event_id) + 1
                else:
                    event_number += 1
                    ids_this_month.append(event_id)
                    names_this_month.append(event_name)

                # Display the event:
                number = (str(event_number)+"·")*(screen.selection_mode)
                if screen.privacy: event_name = PRIVACY_ICON*len(event_name)
                disp = icon + number + event_name
                disp = disp[:screen.x_max - 1]
                color = check_color(event_status)
                try:
                    stdscr.addstr(2+num_of_event_this_day,
                                    1, disp, color_pair(color))
                except:
                    pass

                num_of_event_this_day += 1

            # If there is no more screen space, show "..." icon:
            else:
                hidden = HIDDEN_ICON + " "*(screen.x_max - 3)
                try:
                    stdscr.addstr(3+num_of_event_this_day-2, 1, hidden, color_pair(1))
                except:
                    pass

    # Display birthdays:
    if BIRTHDAYS_FROM_ABOOK:
        for index, bd_date in enumerate(bd_dates):
            try:
                if bd_date == datetime.date(1, screen.month, screen.day):
                    if screen.privacy:
                        event_name = PRIVACY_ICON*len(event_name)
                    bd_name = PRIVACY_ICON*len(bd_names[index]) if screen.privacy else bd_names[index]
                    disp = (BIRTHDAY_ICON+" ")*DISPLAY_ICONS+bd_name
                    disp = disp[:screen.x_max - 1]
                    try:
                        stdscr.addstr(2 + num_of_event_this_day, 1, disp, color_pair(7))
                    except Exception:
                        pass
                    num_of_event_this_day += 1
            except ValueError:
                pass

    # Display holidays:
    if DISPLAY_HOLIDAYS and not holidays is None:
        for holyday_date, occasion in holidays.items():
            try:
                if holyday_date == datetime.date(screen.year, screen.month, screen.day):
                    occasion = PRIVACY_ICON*len(occasion) if privacy else occasion
                    disp = (HOLIDAY_ICON+" ")*DISPLAY_ICONS+occasion
                    disp = disp[:screen.x_max - 1]
                    try:
                        stdscr.addstr(2 + num_of_event_this_day, 1, disp, color_pair(16))
                    except Exception:
                        pass
                    num_of_event_this_day += 1
            except ValueError:
                pass

    # Display current time, hints, and weather:
    display_time(stdscr, date_string)
    if SHOW_KEYBINDINGS:
        stdscr.addstr(y_max - 1, 0, CALENDAR_HINT[:screen.x_max-2], color_pair(3))
    if SHOW_WEATHER:
        weather.display(stdscr, month_year_string)

    return ids_this_month, names_this_month


def control_daily_screen(stdscr, screen, key, ids_this_month, names_this_month):
    '''Handle user input on the daily screen'''

    # If we need to choose one of the events, change the mode:
    screen.refresh_mode = False
    if screen.selection_mode:
        if key in ["d", "x"]:
            delete_event(stdscr, ids_this_month, names_this_month)
        elif key in ["e", "c"]:
            edit_event(stdscr, ids_this_month, names_this_month, screen.month, screen.year)
        elif key in ["i", "h"]:
            mark_event_as_important(stdscr, ids_this_month, names_this_month, screen.month, screen.year)
        elif key in ["l"]:
            mark_event_as_unimportant(stdscr, ids_this_month, names_this_month, screen.month, screen.year)
        screen.selection_mode = False
        screen.refresh_mode = True

    # Otherwise, check for regular hotkeys:
    if not screen.refresh_mode:
        try:
            key = stdscr.getkey()

            # Handle screen resize:
            if key == "KEY_RESIZE":
                screen.y_max, screen.x_max = stdscr.getmaxyx()
                stdscr.clear()
                stdscr.refresh()

            # Handle rest of the keybindings:
            screen.state = vim_style_exit(stdscr, screen.state, key)

            if key in ["n", "j", "KEY_UP", "KEY_RIGHT"]:
                screen.next_day()
            if key in ["p", "k", "KEY_DOWN", "KEY_LEFT"]:
                screen.previous_day()
            if key in ["a"]: add_event(stdscr, screen.day, screen.month, screen.year, recurring = False)
            if key in ["A"]: add_event(stdscr, screen.day, screen.month, screen.year, recurring = True)
            if key in ["q", "KEY_BACKSPACE", "\b", "\x7f"]:
                screen.state = 'monthly_screen'

            # General keys for calendar screen:
            if key in ["d", "x"]: screen.selection_mode = True
            if key in ["e", "c"]: screen.selection_mode = True
            if key in ["i", "h"]: screen.selection_mode = True
            if key in ["l"]:      screen.selection_mode = True
            if key == "?":
                screen.state = 'help_screen'
            if key == "*": screen.privacy = not screen.privacy
            if key == "C": import_events_from_calcurse()
            if key in ["KEY_HOME", "G"]:
                screen = reset_to_today(screen)
            if key in ["KEY_TAB", " "]:
                screen.state = 'journal_screen'

        # Handle keyboard interruption with ctr+c:
        except KeyboardInterrupt:
            prompt_string = "Really exit? (y/n)"
            confirmed = ask_confirmation(stdscr, prompt_string)
            if confirmed:
                screen.state = 'exit'

        # This except is necessary to prevent many various crashes:
        except Exception:
            pass
    return screen, key


def draw_monthly_screen(stdscr, screen, weather):
    '''Draw the screen with monthly view'''
    halfdelay(255)
    stdscr.clear()
    noecho()
    curs_set(False)
    fill_background(stdscr)
    y_cell = (screen.y_max-2)//6
    x_cell = screen.x_max//7
    today  = datetime.date.today()

    # Load data:
    bd_dates, bd_names = parse_birthdays_from_abook()
    events = load_events()
    holidays = load_holidays(screen.year)

    # Displaying the month, year, and days of the week:
    month_year_string = str(calendar.month_name[screen.month].upper()) + " " + str(screen.year)
    display_line(stdscr, 0, 0, month_year_string, 5, BOLD_TITLE, UNDERLINED_TITLE)
    if SHOW_DAY_NAMES:
        display_day_names(stdscr, screen.x_max)

    # Displaying the dates and events:
    day_number = 0
    ids_this_month = []
    names_this_month = []
    event_number = 0
    dates = calendar.Calendar(firstweekday=START_WEEK_DAY-1).monthdayscalendar(screen.year, screen.month)
    for w in range(len(dates)):
        for d in range(7):
            day = dates[w][d]
            if day > 0:

                # Display dates of the month with proper styles:
                shift = START_WEEK_DAY-1
                day_number = d+shift - 7*((d+shift) > 6)
                # Today:
                if datetime.date(screen.year, screen.month, day) == today:
                    display_line(stdscr, 2+w*y_cell, d*x_cell, str(day)+TODAY_ICON, 4, BOLD_TODAY, UNDERLINED_TODAY)
                # Week days:
                elif day_number+1 not in WEEKEND_DAYS:
                    display_line(stdscr, 2+w*y_cell, d*x_cell, str(day), 5, BOLD_DAYS, UNDERLINED_DAYS)
                # Weekends:
                else:
                    display_line(stdscr, 2+w*y_cell, d*x_cell, str(day), 2, BOLD_WEEKENDS, UNDERLINED_WEEKENDS)

                # Display events of this month:
                num_of_event_this_day = 0
                for event_id, event_date, event_name, event_status in zip(events['id'],
                        events['dates'], events['names'], events['statuses']):

                    # Check if this event happens in this day and screen space is okay:
                    if datetime.date(screen.year, screen.month, day) == event_date:
                        if num_of_event_this_day < y_cell - 1:
                            icon = display_icon(event_name, "calendar", screen.selection_mode)

                            # Check if this is a recurring event:
                            if event_id in ids_this_month:
                                event_number = ids_this_month.index(event_id) + 1
                            else:
                                event_number += 1
                                ids_this_month.append(event_id)
                                names_this_month.append(event_name)

                            # Display the event:
                            number = (str(event_number)+"·")*(screen.selection_mode)
                            if screen.privacy:
                                event_name = PRIVACY_ICON*len(event_name)
                            disp = icon + number + event_name*(x_cell > 5)
                            disp = disp[:x_cell] if CUT_TITLES else disp[:screen.x_max-d*x_cell]
                            disp = disp + " "*abs(screen.x_max - x_cell*d - len(disp))
                            color = check_color(event_status)
                            try:
                                stdscr.addstr(3+num_of_event_this_day+w*y_cell,
                                                d*x_cell, disp, color_pair(color))
                            except:
                                pass

                            num_of_event_this_day += 1

                        # If there is no more space, show "..." icon:
                        else:
                            hidden = HIDDEN_ICON + " "*(x_cell - 3)
                            try:
                                stdscr.addstr(3+num_of_event_this_day+w*y_cell-1,
                                                d*x_cell, hidden, color_pair(1))
                            except Exception:
                                pass

                # Display birthdays:
                if BIRTHDAYS_FROM_ABOOK:
                    for index, bd_date in enumerate(bd_dates):
                        try:
                            if bd_date == datetime.date(1, screen.month, day):
                                bd_name = PRIVACY_ICON*len(bd_names[index]) if screen.privacy else bd_names[index]
                                disp = (BIRTHDAY_ICON+" ")*DISPLAY_ICONS+bd_name*(x_cell > 5)
                                disp = disp[:x_cell] if CUT_TITLES else disp[:screen.x_max-d*x_cell]
                                try:
                                    stdscr.addstr(3+num_of_event_this_day+w*y_cell,
                                                    d*x_cell, disp, color_pair(7))
                                except Exception:
                                    pass
                                num_of_event_this_day += 1
                        except ValueError:
                            pass

                # Display holidays:
                if DISPLAY_HOLIDAYS and not holidays is None:
                    for holyday_date, occasion in holidays.items():
                        try:
                            if holyday_date == datetime.date(screen.year, screen.month, day):
                                occasion = PRIVACY_ICON*len(occasion) if privacy else occasion
                                disp = (HOLIDAY_ICON+" ")*DISPLAY_ICONS+occasion*(x_cell > 5)
                                disp = disp[:x_cell] if CUT_TITLES else disp[:screen.x_max-d*x_cell]
                                try:
                                    stdscr.addstr(3+num_of_event_this_day+w*y_cell,
                                                    d*x_cell, disp, color_pair(16))
                                except Exception:
                                    pass
                                num_of_event_this_day += 1
                        except ValueError:
                            pass
            day_number += 1

    # Display current time, hints, and weather:
    display_time(stdscr, month_year_string)
    if SHOW_KEYBINDINGS:
        stdscr.addstr(screen.y_max - 1, 0, CALENDAR_HINT[:x_max-2], color_pair(3))
    if SHOW_WEATHER:
        weather.display(stdscr, month_year_string)
    return ids_this_month, names_this_month


def control_monthly_screen(stdscr, screen, key, ids_this_month, names_this_month):
    '''Process user input on the monthly screen'''
    # If we need to choose one of the events, change the mode:
    screen.refresh_mode = False
    if screen.selection_mode:
        if key in ["d", "x"]:
            delete_event(stdscr, ids_this_month, names_this_month)
        elif key in ["e", "c"]:
            edit_event(stdscr, ids_this_month, names_this_month, screen.month, screen.year)
        elif key in ["i", "h"]:
            mark_event_as_important(stdscr, ids_this_month, names_this_month, screen.month, screen.year)
        elif key in ["l"]:
            mark_event_as_unimportant(stdscr, ids_this_month, names_this_month, screen.month, screen.year)
        screen.selection_mode = False
        screen.refresh_mode = True

    # Otherwise, check for regular hotkeys:
    if not screen.refresh_mode:
        try:
            key = stdscr.getkey()

            # Handle vim-style exit on "ZZ" and "ZQ":
            screen.state = vim_style_exit(stdscr, screen.state, key)

            # Handle "g" as go to selected day:
            day = 1
            if key == "g":
                try:
                    add_prompt = "Go to date: "+str(screen.year)+"/"+str(screen.month)+"/"
                    event_date = int(user_input(stdscr, add_prompt, 2))
                    days_of_this_month = range(1, calendar.monthrange(screen.year, screen.month)[1]+1)
                    if event_date in days_of_this_month:
                        screen.day = event_date
                        screen.state   = 'daily_screen'
                except KeyboardInterrupt:
                    screen.state = 'exit'
                except Exception:
                    pass

            # Handle screen resize:
            if key == "KEY_RESIZE":
                screen.y_max, screen.x_max = stdscr.getmaxyx()
                stdscr.clear()
                stdscr.refresh()

            # Key specific to monthly screen:
            if key in ["n", "j", "KEY_UP", "KEY_RIGHT"]:
                screen.next_month()
            if key in ["p", "k", "KEY_DOWN", "KEY_LEFT"]:
                screen.previous_month()
            if key in ["a"]: add_event(stdscr, None, screen.month, screen.year, recurring = False)
            if key in ["A"]: add_event(stdscr, None, screen.month, screen.year, recurring = True)
            if key == "q":
                screen.state = 'exit'

            # General keys for calendar screen:
            if key in ["d", "x"]: screen.selection_mode = True
            if key in ["e", "c"]: screen.selection_mode = True
            if key in ["i", "h"]: screen.selection_mode = True
            if key in ["l"]:      screen.selection_mode = True
            if key == "?":
                screen.state = 'help_screen'
            if key == "*": screen.privacy = not screen.privacy
            if key == "C": import_events_from_calcurse()
            if key in ["KEY_HOME", "G"]:
                screen = reset_to_today(screen)
            if key in ["KEY_TAB", " "]:
                screen.state = 'journal_screen'

        # Handle keyboard interruption with ctr+c:
        except KeyboardInterrupt:
            prompt_string = "Really exit? (y/n)"
            confirmed = ask_confirmation(stdscr, prompt_string)
            if confirmed:
                screen.state = 'exit'

        # This except is necessary to prevent many various crashes:
        except Exception:
            pass

    return screen, key


def draw_journal_screen(stdscr, tasks, statuses, timestamps, screen):
    '''Draw the journal screen'''
    if screen.refresh_now:
        stdscr.clear()
        screen.refresh_now = False
    noecho()
    halfdelay(255)
    curs_set(False)
    fill_background(stdscr)

    # Check if any of the timers is counting, and increase the update time:
    for times in timestamps:
        curently_counting = False if not times else (len(times)%2 == 1)
        if curently_counting:
            halfdelay(REFRESH_INTERVAL*10)
            break

    try:
        # Display the header:
        if SHOW_TITLE:
            display_line(stdscr, 0, 1, TITLE[:screen.x_max-3], 10, BOLD_TITLE, UNDERLINED_TITLE)
        shift = 2 if SHOW_TITLE else 0

        # Display the tasks:
        for index, task in enumerate(tasks):
            task = task[:screen.x_max-3]

            # Check the tabbing for subtasks:
            tab = 1
            if task[:4] == '----':
                tab += 4
                task = task[4:]
            elif task[:2] == '--':
                tab += 2
                task = task[2:]

            # Display the task name depending on its type:
            if screen.privacy:
                task = PRIVACY_ICON*len(task)
            if statuses[index] == "done":
                stdscr.addstr(index+shift, tab, DONE_ICON, color_pair(12))
                stdscr.addstr(index+shift, tab+2, task, color_pair(12))
            elif statuses[index] == "important":
                stdscr.addstr(index+shift, tab, IMPORTANT_ICON, color_pair(13))
                stdscr.addstr(index+shift, tab+2, task, color_pair(13))
            elif statuses[index] == "unimportant":
                icon = display_icon(task, "journal")
                stdscr.addstr(index+shift, tab, icon, color_pair(20))
                stdscr.addstr(index+shift, tab+2, task, color_pair(20))
            else:
                icon = display_icon(task, "journal")
                stdscr.addstr(index+shift, tab, icon, color_pair(11))
                stdscr.addstr(index+shift, tab+2, task, color_pair(11))

            # Display the timer, depending on avalible space:
            times = timestamps[index]
            timer_started = True if times else False
            curently_counting = False if not times else (len(times)%2 == 1)
            timer_color = color_pair(14) if curently_counting else color_pair(15)
            timer_string = calculate_passed_time(times, curently_counting)
            if timer_started and (len(timer_string+task)+tab+4 < x_max):
                stdscr.addstr(index+shift, tab+4+len(task), timer_string, timer_color)
            elif timer_started and (len(task)+tab+6 < screen.x_max) and DISPLAY_ICONS:
                stdscr.addstr(index+shift, tab+4+len(task), TIMER_ICON, timer_color)

        # Show keybinding:
        if SHOW_KEYBINDINGS:
            stdscr.addstr(y_max - 1, 0, TODO_HINT[:x_max-2], color_pair(3))
    except Exception:
        pass
    stdscr.refresh()


def control_journal_screen(stdscr, tasks, statuses, timestamps, screen):
    '''Process user input on the journal screen'''
    try:

        # Wait for user to press a key:
        key = stdscr.getkey()
        screen.refresh_now = True

        # Handle screen resize:
        if key == "KEY_RESIZE":
            screen.y_max, screen.x_max = stdscr.getmaxyx()
            stdscr.clear()
            stdscr.refresh()

        # Handle keybindings:
        screen.state = vim_style_exit(stdscr, screen.state, key)

        if key == "a": add_task(stdscr, tasks)
        if key == "A": add_subtask(stdscr, tasks, statuses, timestamps)
        if key == "v": mark_as_done(stdscr, tasks, statuses, timestamps)
        if key == "h": mark_as_important(stdscr, tasks, statuses, timestamps)
        if key == "l": mark_as_unimportant(stdscr, tasks, statuses, timestamps)
        if key == "u": unmark_task(stdscr, tasks, statuses, timestamps)
        if key == "V": write_tasks_file(tasks, ['done']*len(tasks), timestamps)
        if key == "H": write_tasks_file(tasks, ['important']*len(tasks), timestamps)
        if key == "U": write_tasks_file(tasks, ['todo']*len(tasks), timestamps)
        if key == "L": write_tasks_file(tasks, ['unimportant']*len(tasks), timestamps)
        if key == "D": delete_all_tasks(stdscr)
        if key == "t": add_timestamp(stdscr, tasks, statuses, timestamps)
        if key == "T": reset_timer(stdscr, tasks, statuses, timestamps)
        if key == "s": toggle_subtask(stdscr, tasks, statuses, timestamps)
        if key == "m": move_task(stdscr, tasks, statuses, timestamps)
        if key == "*": screen.privacy = not screen.privacy
        if key == "C": calcurse_task_import(stdscr, tasks)
        if key == "W": taskwarrior_task_import(stdscr, tasks)
        if key in ["d", "x"]: delete_task(stdscr, tasks, statuses, timestamps)
        if key in ["e", "c"]: edit_task(stdscr, tasks, statuses, timestamps)
        if key == " ":
            screen.state = 'monthly_screen'
        if key == "?":
            screen.state = 'help_screen'
        if key == "q":
            prompt_string = "Really exit? (y/n) "
            confirmed = ask_confirmation(stdscr, prompt_string)
            if confirmed:
                screen.state = 'exit'

    # Handle keybard interruption with ctr+c:
    except KeyboardInterrupt:
        prompt_string = "Really exit? (y/n) "
        confirmed = ask_confirmation(stdscr, prompt_string)
        if confirmed:
            screen.state = 'exit'

    # This except is necessary to prevent many various crashes:
    except Exception:
        pass

    return screen


def draw_help_screen(stdscr, screen):
    '''Draw the help screen'''
    stdscr.clear()
    noecho()
    curs_set(False)
    fill_background(stdscr)

    keys_general, keys_calendar, keys_todo = help_screen_info()

    # Depending on the available screen size, adopt the layout:
    if screen.x_max < 102:
        global_shift_x = 0
        shift_x = 0
        shift_y = 6 + len(keys_general) + len(keys_calendar)
    else:
        global_shift_x = (screen.x_max - 102)//2
        shift_x = 45
        shift_y = 2

    if screen.y_max > 20 and screen.x_max >= 102:
        global_shift_y = (screen.y_max - 20)//2
    else:
        global_shift_y = 0

    # Print out the dictionaries:
    try:
        # Left column:
        title = "CALCURE " + __version__
        display_line(stdscr, global_shift_y, global_shift_x + 1, title[:screen.x_max-3], 6, BOLD_TITLE, UNDERLINED_TITLE)

        display_line(stdscr, global_shift_y + 2, global_shift_x + 8,
                "GENERAL KEYBINDINGS"[:screen.x_max-3], 4, BOLD_TITLE, UNDERLINED_TITLE)
        for index, key in enumerate(keys_general):
            line = str(key+" "+keys_general[key])[:screen.x_max-3]
            display_line(stdscr, global_shift_y + index + 3, global_shift_x, line, 5)

        display_line(stdscr, global_shift_y + 4+len(keys_general), global_shift_x + 8,
                "CALENDAR KEYBINDINGS"[:screen.x_max-3], 4, BOLD_TITLE, UNDERLINED_TITLE)
        for index, key in enumerate(keys_calendar):
            line = str(key+" "+keys_calendar[key])[:screen.x_max-3]
            display_line(stdscr, global_shift_y + index + 5 + len(keys_general), global_shift_x, line, 5)

        # Right column:
        d_x = global_shift_x + shift_x
        d_y = global_shift_y + shift_y
        display_line(stdscr, d_y, d_x + 8, "JOURNAL KEYBINDINGS"[:screen.x_max-3], 4, BOLD_TITLE, UNDERLINED_TITLE)
        for index, key in enumerate(keys_todo):
            line = str(key + " " + keys_todo[key])[:screen.x_max-3]
            display_line(stdscr, d_y + index + 1, d_x, line, 5)

        # Additional info:
        d_x = global_shift_x + shift_x + 8
        d_y = global_shift_y + len(keys_todo) + shift_y
        display_line(stdscr, d_y + 2, d_x, "Vim keys (j, k, ZZ, ZQ) work as well!", 6)
        display_line(stdscr, d_y + 4, d_x, "For more information, visit:", 5)
        display_line(stdscr, d_y + 5, d_x, "https://github.com/anufrievroman/calcure", 4)
    except Exception:
        pass
    stdscr.refresh()


def control_help_screen(stdscr, screen):
    '''Process user input on the help screen'''
    # Getting user's input:
    try:
        key = stdscr.getkey()

        # Handle vim-style exit on "ZZ" and "ZQ":
        screen.state = vim_style_exit(stdscr, screen.state, key)

        # Handle screen resize:
        if key == "KEY_RESIZE":
            screen.y_max, screen.x_max = stdscr.getmaxyx()
            stdscr.clear()
            stdscr.refresh()

        # Handle keys to exit the help screen:
        if key in [" ", "?", "q", "KEY_BACKSPACE", "\b", "\x7f"]:
            screen.state = 'monthly_screen'

    except KeyboardInterrupt:
        prompt_string = "Really exit? (y/n) "
        confirmed = ask_confirmation(stdscr, prompt_string)
        if confirmed:
            screen.state = 'exit'
    except Exception:
        pass
    return screen


class Screen():

    def __init__(self, state, year, month, day, privacy, y_max, x_max):
        self.state = state
        self.year = year
        self.month = month
        self.day = day
        self.privacy = privacy
        self.y_max = y_max
        self.x_max = x_max
        self.selection_mode = False
        self.refresh_mode = False
        self.refresh_now = True

    def next_month(self):
        '''Switches to the next month'''
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year += 1

    def previous_month(self):
        '''Switches to the previous month'''
        if self.month > 1:
            self.month -= 1
        else:
            self.month = 12
            self.year -= 1

    def next_day(self):
        '''Switch the daily veiw to the next day'''
        days_in_this_month = calendar.monthrange(self.year, self.month)[1]
        if self.day < days_in_this_month:
            self.day += 1
        else:
            self.day = 1
            if self.month < 12:
                self.month += 1
            else:
                self.month = 1
                self.year += 1

    def previous_day(self):
        '''Switch the daity view to the previous day'''
        if self.day > 1:
            self.day -= 1
        else:
            if self.month > 1:
                self.month -= 1
            else:
                self.month = 12
                self.year -= 1
            self.day = calendar.monthrange(self.year, self.month)[1]


def main(stdscr):
    '''Main function that runs and switches screens'''
    day     = datetime.date.today().day
    month   = datetime.date.today().month
    year    = datetime.date.today().year
    weather = Weather()

    # Decide how to start the program:
    if DEFAULT_VIEW == 'help':
        state = 'help_screen'
    elif DEFAULT_VIEW == 'version':
        state = 'exit'
    elif DEFAULT_VIEW == 'journal':
        state = 'journal_screen'
    else:
        state = 'monthly_screen'

    # Starting the curses screen:
    stdscr = initscr()
    initialize_colors(stdscr)
    y_max, x_max = stdscr.getmaxyx()

    screen = Screen(state, year, month, day, PRIVACY_MODE, y_max, x_max)

    # Running different screens depending on the state:
    while state != 'exit':
        if screen.state == 'monthly_screen':
            key = None
            while screen.state == 'monthly_screen':
                ids_this_month, names_this_month = draw_monthly_screen(stdscr, screen, weather)
                screen, key = control_monthly_screen(stdscr, screen, key, ids_this_month, names_this_month)

        elif screen.state == 'daily_screen':
            key = None
            while screen.state == 'daily_screen':
                ids_this_month, names_this_month = draw_daily_screen(stdscr, screen, weather)
                screen, key = control_daily_screen(stdscr, screen, key, ids_this_month, names_this_month)

        elif screen.state == 'journal_screen':
            while screen.state == 'journal_screen':
                tasks, statuses, timestamps = load_tasks()
                draw_journal_screen(stdscr, tasks, statuses, timestamps, screen)
                screen = control_journal_screen(stdscr, tasks, statuses, timestamps, screen)

        elif screen.state == 'help_screen':
            while screen.state == 'help_screen':
                draw_help_screen(stdscr, screen)
                screen = control_help_screen(stdscr, screen)

        else:
            break

    # Cleaning up before quitting:
    echo()
    curs_set(True)
    endwin()


def cli() -> None:
    try:
        wrapper(main)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    cli()
