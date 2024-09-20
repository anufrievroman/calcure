"""This module creates and loads user config file"""

import configparser
import sys
import getopt
import logging
import datetime
from pathlib import Path

from calcure.data import AppState


class Config:
    """User configuration loaded from the config.ini file"""
    def __init__(self):
        self.home_path = Path.home()
        self.calcurse_todo_file = self.home_path / ".local" / "share" / "calcurse" / "todo"
        self.calcurse_events_file = self.home_path / ".local" / "share" / "calcurse" / "apts"
        self.config_folder = self.home_path / ".config" / "calcure"
        self.config_file = self.config_folder / "config.ini"
        self.is_first_run= True

        # Create config folder:
        self.config_folder.mkdir(exist_ok=True)

        # Read config file:
        self.create_config_file()
        self.read_config_file_from_user_arguments()
        self.read_config_file()
        self.read_parameters_from_user_arguments()


    def shorten_path(self, path):
        """Replace home part of paths with tilde"""
        if str(path).startswith(str(self.home_path)):
            return str(path).replace(str(self.home_path), "~", 1)
        else:
            return str(path)


    def create_config_file(self):
        """Create config.ini file if it does not exist"""

        if self.config_file.exists():
            self.is_first_run = False
            return

        conf = configparser.ConfigParser()
        conf["Parameters"] = {
                "folder_with_datafiles":     self.shorten_path(self.config_folder),
                "calcurse_todo_file":        self.shorten_path(self.calcurse_todo_file),
                "calcurse_events_file":      self.shorten_path(self.calcurse_events_file),
                "language":                  "en",
                "default_view":              "calendar",
                "default_calendar_view":     "monthly",
                "birthdays_from_abook":      "Yes",
                "show_keybindings":          "Yes",
                "privacy_mode":              "No",
                "show_weather":              "No",
                "weather_city":              "",
                "weather_metric_units":      "Yes",
                "minimal_today_indicator":   "Yes",
                "minimal_days_indicator":    "Yes",
                "minimal_weekend_indicator": "Yes",
                "show_calendar_borders":     "No",
                "cut_titles_by_cell_length": "No",
                "ask_confirmations":         "Yes",
                "ask_confirmation_to_quit":  "Yes",
                "use_unicode_icons":         "Yes",
                "show_current_time":         "No",
                "show_holidays":             "Yes",
                "show_nothing_planned":      "Yes",
                "one_timer_at_a_time":       "No",
                "holiday_country":           "UnitedStates",
                "use_persian_calendar":      "No",
                "start_week_day":            "1",
                "weekend_days":              "6,7",
                "refresh_interval":          "1",
                "data_reload_interval":      "0",
                "split_screen":              "Yes",
                "right_pane_percentage":     "25",
                "journal_header":            "JOURNAL",
                "event_icon":                "•",
                "privacy_icon":              "•",
                "today_icon":                "•",
                "birthday_icon":             "★",
                "holiday_icon":              "⛱",
                "hidden_icon":               "...",
                "done_icon":                 "✔",
                "todo_icon":                 "•",
                "important_icon":            "‣",
                "separator_icon":            "│",
                "deadline_icon":             "⚑",
                }

        conf["Colors"] = {
                "color_today":           "2",
                "color_events":          "4",
                "color_days":            "7",
                "color_day_names":       "4",
                "color_weekends":        "1",
                "color_weekend_names":   "1",
                "color_hints":           "7",
                "color_prompts":         "7",
                "color_confirmations":   "1",
                "color_birthdays":       "1",
                "color_holidays":        "2",
                "color_todo":            "7",
                "color_done":            "6",
                "color_title":           "4",
                "color_calendar_header": "4",
                "color_important":       "1",
                "color_unimportant":     "6",
                "color_timer":           "2",
                "color_timer_paused":    "7",
                "color_time":            "7",
                "color_deadlines":       "3",
                "color_weather":         "2",
                "color_active_pane":     "2",
                "color_separator":       "7",
                "color_calendar_border": "7",
                "color_ics_calendars":   "2,3,1,7,4,5,2,3,1,7",
                "color_background":      "-1",
                }

        conf["Styles"] = {
                "bold_today":               "No",
                "bold_days":                "No",
                "bold_day_names":           "No",
                "bold_weekends":            "No",
                "bold_weekend_names":       "No",
                "bold_title":               "No",
                "bold_active_pane":         "No",
                "underlined_today":         "No",
                "underlined_days":          "No",
                "underlined_day_names":     "No",
                "underlined_weekends":      "No",
                "underlined_weekend_names": "No",
                "underlined_title":         "No",
                "underlined_active_pane":   "No",
                "strikethrough_done":       "No",
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
                "talk":        "🎙️",
                "dating":      "♥",
                "concert":     "♪",
                "dance":       "♪",
                "music":       "♪",
                "rehearsal":   "♪",
                "call":        "🕻",
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
                "sport":       "⛷",
                "gym":         "🏋",
                "training":    "⛷",
                "email":       "✉",
                "letter":      "✉",
                }

        with open(self.config_file, 'w', encoding="utf-8") as f:
            conf.write(f)


    def read_config_file(self):
        """Read user config.ini file and assign values to all the global variables"""
        try:
            conf = configparser.ConfigParser()
            conf.read(self.config_file, 'utf-8')

            # Reading default view:
            default_view = conf.get("Parameters", "default_view", fallback="calendar")
            if default_view == 'journal':
                self.DEFAULT_VIEW = AppState.JOURNAL
            else:
                self.DEFAULT_VIEW = AppState.CALENDAR

            # Calendar settings:
            self.SHOW_KEYBINDINGS          = conf.getboolean("Parameters", "show_keybindings", fallback=True)
            self.MINIMAL_TODAY_INDICATOR   = conf.getboolean("Parameters", "minimal_today_indicator", fallback=True)
            self.MINIMAL_DAYS_INDICATOR    = conf.getboolean("Parameters", "minimal_days_indicator", fallback=True)
            self.MINIMAL_WEEKEND_INDICATOR = conf.getboolean("Parameters", "minimal_weekend_indicator", fallback=True)
            self.ASK_CONFIRMATIONS         = conf.getboolean("Parameters", "ask_confirmations", fallback=True)
            self.ASK_CONFIRMATION_TO_QUIT  = conf.getboolean("Parameters", "ask_confirmation_to_quit", fallback=True)
            self.SHOW_WEATHER              = conf.getboolean("Parameters", "show_weather", fallback=False)
            self.SHOW_CURRENT_TIME         = conf.getboolean("Parameters", "show_current_time", fallback=False)
            self.DISPLAY_ICONS             = conf.getboolean("Parameters", "use_unicode_icons", fallback=True)
            self.DISPLAY_HOLIDAYS          = conf.getboolean("Parameters", "show_holidays", fallback=True)
            self.PRIVACY_MODE              = conf.getboolean("Parameters", "privacy_mode", fallback=False)
            self.CUT_TITLES                = conf.getboolean("Parameters", "cut_titles_by_cell_length", fallback=False)
            self.BIRTHDAYS_FROM_ABOOK      = conf.getboolean("Parameters", "birthdays_from_abook", fallback=True)
            self.SPLIT_SCREEN              = conf.getboolean("Parameters", "split_screen", fallback=True)
            self.SHOW_NOTHING_PLANNED      = conf.getboolean("Parameters", "show_nothing_planned", fallback=True)
            self.SHOW_CALENDAR_BORDERS     = conf.getboolean("Parameters", "show_calendar_borders", fallback=False)
            self.USE_PERSIAN_CALENDAR      = conf.getboolean("Parameters", "use_persian_calendar", fallback=False)
            self.LANG                      = conf.get("Parameters", "language", fallback="en")
            self.START_WEEK_DAY            = int(conf.get("Parameters", "start_week_day", fallback=1))
            self.WEEKEND_DAYS              = conf.get("Parameters", "weekend_days", fallback="6,7")
            self.WEEKEND_DAYS              = [int(i) for i in self.WEEKEND_DAYS.split(",")]
            self.HOLIDAY_COUNTRY           = conf.get("Parameters", "holiday_country", fallback="UnitedStates")
            self.WEATHER_CITY              = conf.get("Parameters", "weather_city", fallback="")
            self.WEATHER_METRIC_UNITS      = conf.getboolean("Parameters", "weather_metric_units", fallback=True)
            self.DEFAULT_CALENDAR_VIEW     = conf.get("Parameters", "default_calendar_view", fallback="monthly")

            # Journal settings:
            self.CALCURSE_TODO_FILE = conf.get("Parameters", "calcurse_todo_file", fallback=self.calcurse_todo_file)
            self.CALCURSE_TODO_FILE = Path(self.CALCURSE_TODO_FILE).expanduser()

            self.CALCURSE_EVENTS_FILE = conf.get("Parameters", "calcurse_events_file", fallback=self.calcurse_events_file)
            self.CALCURSE_EVENTS_FILE = Path(self.CALCURSE_EVENTS_FILE).expanduser()

            self.JOURNAL_HEADER        = conf.get("Parameters", "journal_header", fallback="JOURNAL")
            self.SHOW_KEYBINDINGS      = conf.getboolean("Parameters", "show_keybindings", fallback=True)
            self.DONE_ICON             = conf.get("Parameters", "done_icon", fallback="✔") if self.DISPLAY_ICONS else "×"
            self.TODO_ICON             = conf.get("Parameters", "todo_icon", fallback="•") if self.DISPLAY_ICONS else "·"
            self.IMPORTANT_ICON        = conf.get("Parameters", "important_icon", fallback="‣") if self.DISPLAY_ICONS else "!"
            self.REFRESH_INTERVAL      = int(conf.get("Parameters", "refresh_interval", fallback=1))
            self.DATA_RELOAD_INTERVAL  = int(conf.get("Parameters", "data_reload_interval", fallback=0))
            self.RIGHT_PANE_PERCENTAGE = int(conf.get("Parameters", "right_pane_percentage", fallback=25))
            self.ONE_TIMER_AT_A_TIME   = conf.getboolean("Parameters", "one_timer_at_a_time", fallback=False)

            # ICS files:
            self.ICS_EVENT_FILES = conf.get("Parameters", "ics_event_files", fallback=None, raw=True)
            if self.ICS_EVENT_FILES is not None:
                self.ICS_EVENT_FILES = [str(i) for i in self.ICS_EVENT_FILES.split(",")]

            self.ICS_TASK_FILES = conf.get("Parameters", "ics_task_files", fallback=None, raw=True)
            if self.ICS_TASK_FILES is not None:
                self.ICS_TASK_FILES = [str(i) for i in self.ICS_TASK_FILES.split(",")]

            # Calendar colors:
            self.COLOR_TODAY           = int(conf.get("Colors", "color_today", fallback=2))
            self.COLOR_EVENTS          = int(conf.get("Colors", "color_events", fallback=4))
            self.COLOR_DAYS            = int(conf.get("Colors", "color_days", fallback=7))
            self.COLOR_DAY_NAMES       = int(conf.get("Colors", "color_day_names", fallback=4))
            self.COLOR_WEEKENDS        = int(conf.get("Colors", "color_weekends", fallback=1))
            self.COLOR_WEEKEND_NAMES   = int(conf.get("Colors", "color_weekend_names", fallback=1))
            self.COLOR_HINTS           = int(conf.get("Colors", "color_hints", fallback=7))
            self.COLOR_PROMPTS         = int(conf.get("Colors", "color_prompts", fallback=7))
            self.COLOR_BIRTHDAYS       = int(conf.get("Colors", "color_birthdays", fallback=1))
            self.COLOR_HOLIDAYS        = int(conf.get("Colors", "color_holidays", fallback=2))
            self.COLOR_DEADLINES       = int(conf.get("Colors", "color_deadlines", fallback=3))
            self.COLOR_CONFIRMATIONS   = int(conf.get("Colors", "color_confirmations", fallback=1))
            self.COLOR_TIMER           = int(conf.get("Colors", "color_timer", fallback=2))
            self.COLOR_TIMER_PAUSED    = int(conf.get("Colors", "color_timer_paused", fallback=7))
            self.COLOR_TIME            = int(conf.get("Colors", "color_time", fallback=7))
            self.COLOR_WEATHER         = int(conf.get("Colors", "color_weather", fallback=2))
            self.COLOR_BACKGROUND      = int(conf.get("Colors", "color_background", fallback=-1))
            self.COLOR_CALENDAR_HEADER = int(conf.get("Colors", "color_calendar_header", fallback=4))
            self.COLOR_ACTIVE_PANE     = int(conf.get("Colors", "color_active_pane", fallback=2))
            self.COLOR_SEPARATOR       = int(conf.get("Colors", "color_separator", fallback=7))
            self.COLOR_CALENDAR_BORDER = int(conf.get("Colors", "color_calendar_border", fallback=7))
            self.COLOR_ICS_CALENDARS   = conf.get("Colors", "color_ics_calendars", fallback="2,3,1,7")
            self.COLOR_ICS_CALENDARS   = [int(number) for number in self.COLOR_ICS_CALENDARS.split(",")]

            # Journal colors:
            self.COLOR_TODO           = int(conf.get("Colors", "color_todo", fallback=7))
            self.COLOR_DONE           = int(conf.get("Colors", "color_done", fallback=6))
            self.COLOR_TITLE          = int(conf.get("Colors", "color_title", fallback=1))
            self.COLOR_IMPORTANT      = int(conf.get("Colors", "color_important", fallback=1))
            self.COLOR_UNIMPORTANT    = int(conf.get("Colors", "color_unimportant", fallback=6))

            # Font styles:
            self.BOLD_TODAY               = conf.getboolean("Styles", "bold_today", fallback=False)
            self.BOLD_DAYS                = conf.getboolean("Styles", "bold_days", fallback=False)
            self.BOLD_DAY_NAMES           = conf.getboolean("Styles", "bold_day_names", fallback=False)
            self.BOLD_WEEKENDS            = conf.getboolean("Styles", "bold_weekends", fallback=False)
            self.BOLD_WEEKEND_NAMES       = conf.getboolean("Styles", "bold_weekend_names", fallback=False)
            self.BOLD_TITLE               = conf.getboolean("Styles", "bold_title", fallback=False)
            self.BOLD_ACTIVE_PANE         = conf.getboolean("Styles", "bold_active_pane", fallback=False)
            self.UNDERLINED_TODAY         = conf.getboolean("Styles", "underlined_today", fallback=False)
            self.UNDERLINED_DAYS          = conf.getboolean("Styles", "underlined_days", fallback=False)
            self.UNDERLINED_DAY_NAMES     = conf.getboolean("Styles", "underlined_day_names", fallback=False)
            self.UNDERLINED_WEEKENDS      = conf.getboolean("Styles", "underlined_weekends", fallback=False)
            self.UNDERLINED_WEEKEND_NAMES = conf.getboolean("Styles", "underlined_weekend_names", fallback=False)
            self.UNDERLINED_TITLE         = conf.getboolean("Styles", "underlined_title", fallback=False)
            self.UNDERLINED_ACTIVE_PANE   = conf.getboolean("Styles", "underlined_active_pane", fallback=False)
            self.STRIKETHROUGH_DONE       = conf.getboolean("Styles", "strikethrough_done", fallback=False)

            # Icons:
            self.TODAY_ICON       = conf.get("Parameters", "today_icon", fallback="•") if self.DISPLAY_ICONS else "·"
            self.PRIVACY_ICON     = conf.get("Parameters", "privacy_icon", fallback="•") if self.DISPLAY_ICONS else "·"
            self.HIDDEN_ICON      = conf.get("Parameters", "hidden_icon", fallback="...")
            self.EVENT_ICON       = conf.get("Parameters", "event_icon", fallback="•") if self.DISPLAY_ICONS else "·"
            self.BIRTHDAY_ICON    = conf.get("Parameters", "birthday_icon", fallback="★") if self.DISPLAY_ICONS else "·"
            self.HOLIDAY_ICON     = conf.get("Parameters", "holiday_icon", fallback="☘️") if self.DISPLAY_ICONS else "·"
            self.SEPARATOR_ICON   = conf.get("Parameters", "separator_icon", fallback="│")
            self.DEADLINE_ICON    = conf.get("Parameters", "deadline_icon", fallback="⚑") if self.DISPLAY_ICONS else "·"
            try:
                self.ICONS = {word: icon for (word, icon) in conf.items("Event icons")}
            except configparser.NoSectionError:
                self.ICONS = {}

            self.data_folder = conf.get("Parameters", "folder_with_datafiles", fallback=self.config_folder)
            self.data_folder = Path(self.data_folder).expanduser()
            self.EVENTS_FILE = self.data_folder / "events.csv"
            self.TASKS_FILE = self.data_folder / "tasks.csv"

        except Exception:
            ERR_FILE1 = "Looks like there is a problem in your config.ini file. Perhaps you edited it and entered a wrong line. "
            ERR_FILE2 = "Try removing your config.ini file and run the program again, it will create a fresh working config file."
            logging.error(ERR_FILE1 + ERR_FILE2)
            exit()


    def read_config_file_from_user_arguments(self):
        """Read user config.ini location from user arguments"""
        try:
            opts, _ = getopt.getopt(sys.argv[1:], "pjchv", ["folder=", "config="])
            for opt, arg in opts:
                if opt in "--config":
                    self.config_file = Path(arg).expanduser()
                    if not self.config_file.exists():
                        self.create_config_file()
        except getopt.GetoptError:
            pass


    def read_parameters_from_user_arguments(self):
        """Read user arguments that were provided at the run. This values take priority over config.ini"""
        try:
            opts, _ = getopt.getopt(sys.argv[1:],"pjhvid",["folder=", "config=", "task=", "event="])
            for opt, arg in opts:
                if opt in '--folder':
                    self.data_folder = Path(arg).expanduser()
                    self.data_folder.mkdir(exist_ok=True)
                    self.EVENTS_FILE = self.data_folder / "events.csv"
                    self.TASKS_FILE = self.data_folder / "tasks.csv"
                elif opt == '-p':
                    self.PRIVACY_MODE = True
                elif opt == '-j':
                    self.DEFAULT_VIEW = AppState.JOURNAL
                elif opt == '-d':
                    self.DEFAULT_VIEW = AppState.JOURNAL
                elif opt in ('-h'):
                    self.DEFAULT_VIEW = AppState.HELP
                elif opt in ('-v'):
                    self.DEFAULT_VIEW = AppState.EXIT
                    print ('Calcure - version 3.1')
                elif opt in ('-i'):
                    self.USE_PERSIAN_CALENDAR = True
        except getopt.GetoptError as e_message:
            logging.error("Invalid user arguments. %s", e_message)
            pass

