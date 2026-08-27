"""Keybindings loaded from keybindings.ini or falling back to defaults.

To customise, create ~/.config/calcure/keybindings.ini with a [Keybindings]
section and set any of the keys listed below, e.g.:

    [Keybindings]
    key_done   = D
    key_delete = BackSpace
"""

import configparser
from pathlib import Path

_keybindings_file = Path.home() / ".config" / "calcure" / "keybindings.ini"

# Default keybindings:

# Navigation
KEY_NEXT              = "n"
KEY_PREV              = "p"
KEY_TODAY             = "R"
KEY_GOTO              = "g"
KEY_GOTO_DAY          = "G"

# View switching
KEY_VIEW_DAILY        = "v"
KEY_VIEW_WEEKLY       = "w"
KEY_VIEW_WEEK_NUMBERS = "W"

# Events and tasks — shared actions
KEY_ADD               = "a"
KEY_ADD_EXTRA         = "A"   # recurring event (calendar) / add subtask (journal)
KEY_IMPORTANT         = "i"   # h is a permanent alias
KEY_LOW               = "l"
KEY_UNMARK            = "u"
KEY_DONE              = "d"   # v is a permanent alias in the journal
KEY_DELETE            = "x"
KEY_EDIT              = "e"   # r is a permanent alias
KEY_MOVE              = "m"
KEY_MOVE_IN_MONTH     = "M"
KEY_PRIVACY_ITEM      = "."

# Journal-only task actions
KEY_TIMER             = "t"
KEY_TIMER_RESET       = "T"
KEY_TIMERS_TOGGLE     = "P"
KEY_SUBTASK_STATE     = "s"
KEY_DEADLINE          = "f"
KEY_DEADLINE_REMOVE   = "F"
KEY_DONE_ALL          = "D"   # V is a permanent alias
KEY_UNMARK_ALL        = "U"
KEY_LOW_ALL           = "L"
KEY_IMPORTANT_ALL     = "I"   # H is a permanent alias
KEY_DELETE_ALL        = "X"
KEY_HIDE_DONE         = "-"

# Global
KEY_PRIVACY           = "*"
KEY_IMPORT            = "C"
KEY_RELOAD            = "Q"
KEY_QUIT              = "q"
KEY_HELP              = "?"
KEY_SWITCH            = " "
KEY_SPLIT             = "/"

# Load overrides from keybindings.ini if it exists:

if _keybindings_file.exists():
    _conf = configparser.ConfigParser()
    _conf.read(_keybindings_file)
    if _conf.has_section("Keybindings"):
        _b = _conf["Keybindings"]
        KEY_NEXT              = _b.get("key_next",              KEY_NEXT)
        KEY_PREV              = _b.get("key_prev",              KEY_PREV)
        KEY_TODAY             = _b.get("key_today",             KEY_TODAY)
        KEY_GOTO              = _b.get("key_goto",              KEY_GOTO)
        KEY_GOTO_DAY          = _b.get("key_goto_day",          KEY_GOTO_DAY)
        KEY_VIEW_DAILY        = _b.get("key_view_daily",        KEY_VIEW_DAILY)
        KEY_VIEW_WEEKLY       = _b.get("key_view_weekly",       KEY_VIEW_WEEKLY)
        KEY_VIEW_WEEK_NUMBERS = _b.get("key_view_week_numbers", KEY_VIEW_WEEK_NUMBERS)
        KEY_ADD               = _b.get("key_add",               KEY_ADD)
        KEY_ADD_EXTRA         = _b.get("key_add_extra",         KEY_ADD_EXTRA)
        KEY_IMPORTANT         = _b.get("key_important",         KEY_IMPORTANT)
        KEY_LOW               = _b.get("key_low",               KEY_LOW)
        KEY_UNMARK            = _b.get("key_unmark",            KEY_UNMARK)
        KEY_DONE              = _b.get("key_done",              KEY_DONE)
        KEY_DELETE            = _b.get("key_delete",            KEY_DELETE)
        KEY_EDIT              = _b.get("key_edit",              KEY_EDIT)
        KEY_MOVE              = _b.get("key_move",              KEY_MOVE)
        KEY_MOVE_IN_MONTH     = _b.get("key_move_in_month",     KEY_MOVE_IN_MONTH)
        KEY_PRIVACY_ITEM      = _b.get("key_privacy_item",      KEY_PRIVACY_ITEM)
        KEY_TIMER             = _b.get("key_timer",             KEY_TIMER)
        KEY_TIMER_RESET       = _b.get("key_timer_reset",       KEY_TIMER_RESET)
        KEY_TIMERS_TOGGLE     = _b.get("key_timers_toggle",     KEY_TIMERS_TOGGLE)
        KEY_SUBTASK_STATE     = _b.get("key_subtask_state",     KEY_SUBTASK_STATE)
        KEY_DEADLINE          = _b.get("key_deadline",          KEY_DEADLINE)
        KEY_DEADLINE_REMOVE   = _b.get("key_deadline_remove",   KEY_DEADLINE_REMOVE)
        KEY_DONE_ALL          = _b.get("key_done_all",          KEY_DONE_ALL)
        KEY_UNMARK_ALL        = _b.get("key_unmark_all",        KEY_UNMARK_ALL)
        KEY_LOW_ALL           = _b.get("key_low_all",           KEY_LOW_ALL)
        KEY_IMPORTANT_ALL     = _b.get("key_important_all",     KEY_IMPORTANT_ALL)
        KEY_DELETE_ALL        = _b.get("key_delete_all",        KEY_DELETE_ALL)
        KEY_HIDE_DONE         = _b.get("key_hide_done",         KEY_HIDE_DONE)
        KEY_PRIVACY           = _b.get("key_privacy",           KEY_PRIVACY)
        KEY_IMPORT            = _b.get("key_import",            KEY_IMPORT)
        KEY_RELOAD            = _b.get("key_reload",            KEY_RELOAD)
        KEY_QUIT              = _b.get("key_quit",              KEY_QUIT)
        KEY_HELP              = _b.get("key_help",              KEY_HELP)
        KEY_SWITCH            = _b.get("key_switch",            KEY_SWITCH)
        KEY_SPLIT             = _b.get("key_split",             KEY_SPLIT)

        # Allow writing "Space" in the ini file for the space character:
        if KEY_SWITCH.lower() == "space":
            KEY_SWITCH = " "

# Aggregate key lists for @block_until_valid_input decorators.
# Fixed keys are navigation/special keys that are never user-configurable:

_FIXED_NAV = ["j", "k", "KEY_UP", "KEY_DOWN", "KEY_LEFT", "KEY_RIGHT", "KEY_HOME", "KEY_BTAB"]
_FIXED_ACT = ["h", "r", "c"]   # permanent aliases: h=important, r=edit, c=noop

CALENDAR_KEYS = list(dict.fromkeys([
    KEY_NEXT, KEY_PREV, KEY_TODAY, KEY_GOTO, KEY_GOTO_DAY,
    KEY_VIEW_DAILY, KEY_VIEW_WEEKLY, KEY_VIEW_WEEK_NUMBERS,
    KEY_ADD, KEY_ADD_EXTRA,
    KEY_IMPORTANT, KEY_LOW, KEY_UNMARK, KEY_DONE, KEY_DELETE, KEY_EDIT,
    KEY_MOVE, KEY_MOVE_IN_MONTH, KEY_PRIVACY_ITEM,
    KEY_IMPORT, KEY_RELOAD, KEY_QUIT, KEY_HELP, KEY_SWITCH, KEY_SPLIT, KEY_PRIVACY,
] + _FIXED_NAV + _FIXED_ACT))

WEEKLY_KEYS = list(dict.fromkeys(CALENDAR_KEYS + ["V"]))

JOURNAL_KEYS = list(dict.fromkeys([
    KEY_ADD, KEY_ADD_EXTRA,
    KEY_IMPORTANT, KEY_LOW, KEY_UNMARK, KEY_DONE, KEY_DELETE, KEY_EDIT,
    KEY_MOVE, KEY_PRIVACY_ITEM,
    KEY_TIMER, KEY_TIMER_RESET, KEY_TIMERS_TOGGLE, KEY_SUBTASK_STATE,
    KEY_DEADLINE, KEY_DEADLINE_REMOVE,
    KEY_DONE_ALL, KEY_UNMARK_ALL, KEY_LOW_ALL, KEY_IMPORTANT_ALL, KEY_DELETE_ALL,
    KEY_HIDE_DONE, KEY_IMPORT,
    KEY_PRIVACY, KEY_RELOAD, KEY_QUIT, KEY_HELP, KEY_SWITCH, KEY_SPLIT,
    "h", "v", "V", "H", "r", "c", "KEY_BTAB",
]))

HELP_KEYS = list(dict.fromkeys([KEY_SWITCH, KEY_HELP, KEY_QUIT, "^[", "\x7f"]))
