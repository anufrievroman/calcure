import curses
from data import Frequency, Color


def display_question(stdscr, y, x, question, color):
    """Display the line of text respecting the slyling and available space"""
    y_max, x_max = stdscr.getmaxyx()
    if y >= y_max or x >= x_max: return
    question = question[:(x_max - x - 1)]
    stdscr.addstr(y, x, question, curses.color_pair(color.value))


def clear_line(stdscr, y, x = 0):
    """Clear a line from any text"""
    _, x_max = stdscr.getmaxyx()
    stdscr.addstr(y, x, " "*(x_max - x - 2), curses.color_pair(Color.DAYS.value))


def input_string(stdscr, y, x, question, answer_length):
    """Ask user to input something and return it as a string"""
    _, x_max = stdscr.getmaxyx()
    curses.echo()
    curses.curs_set(True)
    display_question(stdscr, y, x, question, Color.PROMPTS)
    stdscr.refresh()
    answer = stdscr.getstr(y, len(question) + x, answer_length).decode(encoding="utf-8")
    curses.noecho()
    curses.curs_set(False)
    return answer


def input_integer(stdscr, y, x, prompt_string):
    """Ask user for an integer number and check if it is an integer"""
    number = input_string(stdscr, y, x, prompt_string, 3)
    try:
        number = int(number) - 1
    except ValueError:
        return None
    return number


def input_day(stdscr, y, x, prompt_string):
    """Ask user for an integer number and check if it is an integer"""
    number = input_string(stdscr, y, x, prompt_string, 2)
    try:
        number = int(number)
    except ValueError:
        return None
    return number


def input_frequency(stdscr, y, x, question):
    """Ask user for the frequency of event repetitions"""
    freq = input_string(stdscr, y, x, question, 2)
    if freq == 'd':
        return Frequency.DAILY
    elif freq == 'w':
        return Frequency.WEEKLY
    elif freq == 'm':
        return Frequency.MONTHLY
    elif freq == 'y':
        return Frequency.YEARLY
    elif freq == 'n':
        return Frequency.ONCE
    else:
        return None


def ask_confirmation(stdscr, question, confirmations_enabled):
    """Ask user confirmation for an action"""
    if not confirmations_enabled: return True
    y_max, x_max = stdscr.getmaxyx()
    curses.halfdelay(255)
    display_question(stdscr, y_max-2, 0, question, Color.CONFIRMATIONS)
    key = stdscr.getkey()
    confirmed = True if key == "y" else False
    return confirmed


def vim_style_exit(stdscr, screen):
    """Handle vim style key combinations like "ZZ" and "ZQ" for exit"""
    if screen.key == "Z":
        try:
            screen.key = stdscr.getkey()
            return True if screen.key in ["Z", "Q"] else False
        except KeyboardInterrupt:
            return True
    else:
        return False
