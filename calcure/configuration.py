"""This module creates and loads user config file"""

import os
import pathlib
import configparser
import sys
import getopt

from calcure.translation_en import ERR_FILE1, ERR_FILE2
from calcure.data import AppState


class Config:
    """User configuration loaded from the config.ini file"""
    def __init__(self):
        self.taskwarrior_folder    = str(pathlib.Path.home()) + "/.task"
        self.calcurse_todo_file    = str(pathlib.Path.home()) + "/.local/share/calcurse/todo"
        self.calcurse_events_file  = str(pathlib.Path.home()) + "/.local/share/calcurse/apts"
        self.config_folder         = str(pathlib.Path.home()) + "/.config/calcure"
        self.config_file           = self.config_folder + "/config.ini"

    def create_config_file(self):
        """Create config.ini file if it does not exist"""
        if os.path.exists(self.config_file):
            return

        if not os.path.exists(self.config_folder):
            os.makedirs(self.config_folder)

        conf = configparser.ConfigParser()
        conf["Parameters"] = {
                "folder_with_datafiles":     str(self.config_folder),
                "calcurse_todo_file":        str(self.calcurse_todo_file),
                "calcurse_events_file":      str(self.calcurse_events_file),
                "taskwarrior_folder":        str(self.taskwarrior_folder),
                "default_view":              "calendar",
                "birthdays_from_abook":      "Yes",
                "show_keybindings":          "Yes",
                "privacy_mode":              "No",
                "show_weather":              "No",
                "weather_city":              "",
                "minimal_today_indicator":   "Yes",
                "minimal_days_indicator":    "Yes",
                "minimal_weekend_indicator": "Yes",
                "show_calendar_boarders":    "No",
                "cut_titles_by_cell_length": "No",
                "ask_confirmations":         "Yes",
                "use_unicode_icons":         "Yes",
                "show_current_time":         "No",
                "show_holidays":             "Yes",
                "show_nothing_planned":      "Yes",
                "holiday_country":           "UnitedStates",
                "use_persian_calendar":      "No",
                "start_week_day":            "1",
                "weekend_days":              "6,7",
                "refresh_interval":          "1",
                "split_screen":              "Yes",
                "right_pane_percentage":     "25",
                "journal_header":            "JOURNAL",
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
                "separator_icon":            "│",
                }

        conf["Colors"] = {
                "color_today":           "2",
                "color_events":          "7",
                "color_days":            "4",
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
                "color_weather":         "2",
                "color_active_pane":     "2",
                "color_separator":       "7",
                "color_calendar_border": "7",
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
                "rehearsal":   "♪",
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

        with open(self.config_file, 'w', encoding="utf-8") as f:
            conf.write(f)

    def read_config_file(self):
        """Read user config.ini file"""
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
            self.SHOW_WEATHER              = conf.getboolean("Parameters", "show_weather", fallback=False)
            self.SHOW_CURRENT_TIME         = conf.getboolean("Parameters", "show_current_time", fallback=False)
            self.DISPLAY_ICONS             = conf.getboolean("Parameters", "use_unicode_icons", fallback=True)
            self.DISPLAY_HOLIDAYS          = conf.getboolean("Parameters", "show_holidays", fallback=True)
            self.PRIVACY_MODE              = conf.getboolean("Parameters", "privacy_mode", fallback=False)
            self.CUT_TITLES                = conf.getboolean("Parameters", "cut_titles_by_cell_length", fallback=False)
            self.BIRTHDAYS_FROM_ABOOK      = conf.getboolean("Parameters", "birthdays_from_abook", fallback=True)
            self.SPLIT_SCREEN              = conf.getboolean("Parameters", "split_screen", fallback=True)
            self.SHOW_NOTHING_PLANNED      = conf.getboolean("Parameters", "show_nothing_planned", fallback=True)
            self.SHOW_CALENDAR_BOARDERS    = conf.getboolean("Parameters", "show_calendar_boarders", fallback=False)
            self.USE_PERSIAN_CALENDAR      = conf.getboolean("Parameters", "use_persian_calendar", fallback=False)
            self.START_WEEK_DAY            = int(conf.get("Parameters", "start_week_day", fallback=1))
            self.WEEKEND_DAYS              = conf.get("Parameters", "weekend_days", fallback="6,7")
            self.WEEKEND_DAYS              = [int(i) for i in self.WEEKEND_DAYS.split(",")]

            self.HOLIDAY_COUNTRY  = conf.get("Parameters", "holiday_country", fallback="UnitedStates")
            self.WEATHER_CITY     = conf.get("Parameters", "weather_city", fallback="")
            self.TODAY_ICON       = conf.get("Parameters", "today_icon", fallback="•") if self.DISPLAY_ICONS else "·"
            self.PRIVACY_ICON     = conf.get("Parameters", "privacy_icon", fallback="•") if self.DISPLAY_ICONS else "·"
            self.HIDDEN_ICON      = conf.get("Parameters", "hidden_icon", fallback="...")
            self.EVENT_ICON       = conf.get("Parameters", "event_icon", fallback="•") if self.DISPLAY_ICONS else ""
            self.BIRTHDAY_ICON    = conf.get("Parameters", "birthday_icon", fallback="★")
            self.HOLIDAY_ICON     = conf.get("Parameters", "holiday_icon", fallback="☘️")
            self.SEPARATOR_ICON   = conf.get("Parameters", "separator_icon", fallback="│")

            # Journal settings:
            self.CALCURSE_TODO_FILE    = conf.get("Parameters", "calcurse_todo_file", fallback=self.calcurse_todo_file)
            self.CALCURSE_EVENTS_FILE  = conf.get("Parameters", "calcurse_events_file", fallback=self.calcurse_events_file)
            self.TASKWARRIOR_FOLDER    = conf.get("Parameters", "taskwarrior_folder", fallback=self.taskwarrior_folder)
            self.JOURNAL_HEADER        = conf.get("Parameters", "journal_header", fallback="JOURNAL")
            self.SHOW_KEYBINDINGS      = conf.getboolean("Parameters", "show_keybindings", fallback=True)
            self.DONE_ICON             = conf.get("Parameters", "done_icon", fallback="✔") if self.DISPLAY_ICONS else "×"
            self.TODO_ICON             = conf.get("Parameters", "todo_icon", fallback="•") if self.DISPLAY_ICONS else "·"
            self.IMPORTANT_ICON        = conf.get("Parameters", "important_icon", fallback="‣") if self.DISPLAY_ICONS else "!"
            self.TIMER_ICON            = conf.get("Parameters", "timer_icon", fallback="⌚") if self.DISPLAY_ICONS else "!"
            self.REFRESH_INTERVAL      = int(conf.get("Parameters", "refresh_interval", fallback=1))
            self.RIGHT_PANE_PERCENTAGE = int(conf.get("Parameters", "right_pane_percentage", fallback=25))

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
            self.COLOR_CONFIRMATIONS   = int(conf.get("Colors", "color_confirmations", fallback=1))
            self.COLOR_TIMER           = int(conf.get("Colors", "color_timer", fallback=2))
            self.COLOR_TIMER_PAUSED    = int(conf.get("Colors", "color_timer_paused", fallback=7))
            self.COLOR_TIME            = int(conf.get("Colors", "color_time", fallback=7))
            self.COLOR_WEATHER         = int(conf.get("Colors", "color_weather", fallback=2))
            self.COLOR_BACKGROUND      = int(conf.get("Colors", "color_background", fallback=-1))
            self.COLOR_CALENDAR_HEADER = int(conf.get("Colors", "color_calendar_header", fallback=4))
            self.COLOR_ACTIVE_PANE     = int(conf.get("Colors", "color_active_pane", fallback=2))
            self.COLOR_SEPARATOR       = int(conf.get("Colors", "color_separator", fallback=7))
            self.COLOR_CALENDAR_BOARDER= int(conf.get("Colors", "color_calendar_border", fallback=7))

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

            try:
                self.ICONS = {word: icon for (word, icon) in conf.items("Event icons")}
            except configparser.NoSectionError:
                self.ICONS = {}

            self.data_folder = conf.get("Parameters", "folder_with_datafiles", fallback=self.config_folder)
            self.EVENTS_FILE = self.data_folder + "/events.csv"
            self.TASKS_FILE = self.data_folder + "/tasks.csv"

        except Exception:
            print(ERR_FILE1)
            print(ERR_FILE2)
            exit()

    def read_config_file_from_user_arguments(self):
        """Read user config.ini location from user arguments"""
        try:
            opts, _ = getopt.getopt(sys.argv[1:], "pjchv", ["folder=", "config="])
            for opt, arg in opts:
                if opt in "--config":
                    self.config_file = arg
                    if not os.path.exists(self.config_file):
                        self.create_config_file()
        except getopt.GetoptError:
            pass

    def read_parameters_from_user_arguments(self):
        """Read user arguments that were provided at the run"""
        try:
            opts, _ = getopt.getopt(sys.argv[1:],"pjhvi",["folder=", "config="])
            for opt, arg in opts:
                if opt in '--folder':
                    self.data_folder = arg
                    if not os.path.exists(self.data_folder):
                        os.makedirs(self.data_folder)
                    self.EVENTS_FILE = self.data_folder + "/events.csv"
                    self.TASKS_FILE = self.data_folder + "/tasks.csv"
                elif opt == '-p':
                    self.PRIVACY_MODE = True
                elif opt == '-j':
                    self.DEFAULT_VIEW = AppState.JOURNAL
                elif opt in ('-h'):
                    self.DEFAULT_VIEW = AppState.HELP
                elif opt in ('-v'):
                    self.DEFAULT_VIEW = AppState.EXIT
                    print ('Calcure - version 2.0')
                elif opt in ('-i'):
                    self.USE_PERSIAN_CALENDAR = True
        except getopt.GetoptError:
            pass


# Read config file:
cf = Config()
cf.create_config_file()
cf.read_config_file_from_user_arguments()
cf.read_config_file()
cf.read_parameters_from_user_arguments()
