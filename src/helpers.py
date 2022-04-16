import curses
import jdatetime
from config import cf


##################### CALENDAR OPERATIONS ##############################


def monthrange_gregorian(year, month):
    '''Return number of days (28-31) in this gregorian month and year'''

    def isleap(year):
        '''Return True for leap years, False for non-leap years'''
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    mdays = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return mdays[month] + (month == 2 and isleap(year))


def monthrange_persian(year, month):
    '''Return number of days (28-31) in this Jalali month and year'''

    def isleap(year):
        '''Return True for leap years, False for non-leap years'''
        return jdatetime.date(year, 1, 1).isleap()

    mdays = [0, 31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
    return mdays[month] + (month == 12 and isleap(year))


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
            if day > skip_days + monthrange_gregorian(year, month + i):
                skip_days += monthrange_gregorian(year, month + i)
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


##################### ON-SCREEN OPERATIONS ##############################


def display_line(stdscr, y, x, text, color, bold=False, underlined=False):
    '''Display the line of text respecting the slyling and available space'''

    # Make sure that we display inside the screen:
    y_max, x_max = stdscr.getmaxyx()
    if y >= y_max or x >= x_max: return

    # Cut the text if it does not fit the screen:
    text = text[:(x_max-1-x)]

    if bold and underlined:
        stdscr.addstr(y, x, text, curses.color_pair(color) | curses.A_BOLD | curses.A_UNDERLINE)
    elif bold and not underlined:
        stdscr.addstr(y, x, text, curses.color_pair(color) | curses.A_BOLD)
    elif underlined and not bold:
        stdscr.addstr(y, x, text, curses.color_pair(color) | curses.A_UNDERLINE)
    else:
        stdscr.addstr(y, x, text, curses.color_pair(color))


def fill_background(stdscr):
    '''Fill the screen background with background color'''
    y_max, x_max = stdscr.getmaxyx()
    for index in range(y_max-1):
        stdscr.addstr(index, 0, " "*x_max, curses.color_pair(1))


def initialize_colors(stdscr):
    '''Define all the color pairs'''
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, cf.COLOR_DAY_NAMES, cf.COLOR_BACKGROUND)
    curses.init_pair(2, cf.COLOR_WEEKENDS, cf.COLOR_BACKGROUND)
    curses.init_pair(3, cf.COLOR_HINTS, cf.COLOR_BACKGROUND)
    curses.init_pair(4, cf.COLOR_TODAY, cf.COLOR_BACKGROUND)
    curses.init_pair(5, cf.COLOR_DAYS, cf.COLOR_BACKGROUND)
    curses.init_pair(6, cf.COLOR_WEEKEND_NAMES, cf.COLOR_BACKGROUND)
    curses.init_pair(7, cf.COLOR_BIRTHDAYS, cf.COLOR_BACKGROUND)
    curses.init_pair(8, cf.COLOR_PROMPTS, cf.COLOR_BACKGROUND)
    curses.init_pair(9, cf.COLOR_CONFIRMATIONS, cf.COLOR_BACKGROUND)
    curses.init_pair(10, cf.COLOR_TITLE, cf.COLOR_BACKGROUND)
    curses.init_pair(11, cf.COLOR_TODO, cf.COLOR_BACKGROUND)
    curses.init_pair(12, cf.COLOR_DONE, cf.COLOR_BACKGROUND)
    curses.init_pair(13, cf.COLOR_IMPORTANT, cf.COLOR_BACKGROUND)
    curses.init_pair(14, cf.COLOR_TIMER, cf.COLOR_BACKGROUND)
    curses.init_pair(15, cf.COLOR_TIMER_PAUSED, cf.COLOR_BACKGROUND)
    curses.init_pair(16, cf.COLOR_HOLIDAYS, cf.COLOR_BACKGROUND)
    curses.init_pair(17, cf.COLOR_EVENTS, cf.COLOR_BACKGROUND)
    curses.init_pair(18, cf.COLOR_TIME, cf.COLOR_BACKGROUND)
    curses.init_pair(19, cf.COLOR_WEATHER, cf.COLOR_BACKGROUND)
    curses.init_pair(20, cf.COLOR_UNIMPORTANT, cf.COLOR_BACKGROUND)
    curses.init_pair(21, cf.COLOR_CALENDAR_HEADER, cf.COLOR_BACKGROUND)

    if not cf.MINIMAL_WEEKEND_INDICATOR:
        curses.init_pair(2, curses.COLOR_BLACK, cf.COLOR_WEEKENDS)
    if not cf.MINIMAL_TODAY_INDICATOR:
        curses.init_pair(4, curses.COLOR_BLACK, cf.COLOR_TODAY)
    if not cf.MINIMAL_DAYS_INDICATOR:
        curses.init_pair(5, curses.COLOR_BLACK, cf.COLOR_DAYS)
