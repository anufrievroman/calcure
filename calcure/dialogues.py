""" Module that controls interactions with the user, like questions and confirmations"""

import curses
import logging

from calcure.data import Frequency
from calcure.colors import Color



def safe_run(func):
    """Decorator preventing crashes on keyboard interruption and no input"""

    def inner(stdscr, screen, *args, **kwargs):
        try:
            func(stdscr, screen, *args, **kwargs)

        # Handle keyboard interruption with ctrl+c:
        except KeyboardInterrupt:
            pass

        # Prevent crash if no input:
        except curses.error:
            pass
    return inner


def display_question(stdscr, y, x, question, color):
    """Display the line of text respecting the styling and available space"""
    y_max, x_max = stdscr.getmaxyx()
    if y >= y_max or x >= x_max:
        return
    question = question[:(x_max - x - 1)]
    stdscr.addstr(y, x, question, curses.color_pair(color.value))


def clear_line(stdscr, y, x=0):
    """Clear a line from any text"""
    _, x_max = stdscr.getmaxyx()
    stdscr.addstr(y, x, " " * (x_max - x - 1), curses.color_pair(Color.EMPTY.value))


def input_field(stdscr, y, x, field_length):
    """Input field that gets characters entered by user"""
    curses.curs_set(1)
    input_str = ""
    cursor_pos = 0

    while True:
        stdscr.move(y, x + cursor_pos)
        key = stdscr.get_wch()

        # Regular Unicode characters:
        if isinstance(key, str):
            if ord(key) == 27: # Esc
                return ""
            elif ord(key) in (10, 13): # Enter
                return input_str
            elif ord(key) == 127 and cursor_pos > 0: # Backspace
                input_str = input_str[:cursor_pos-1] + input_str[cursor_pos:]
                cursor_pos -= 1
            elif cursor_pos < field_length: # Other characters:
                input_str = input_str[:cursor_pos] + chr(ord(key)) + input_str[cursor_pos:]
                cursor_pos += 1
            else:
                pass

        # Various keys:
        else:
            if key == curses.KEY_ENTER:
                return input_str
            elif key == curses.KEY_BACKSPACE and cursor_pos > 0:
                input_str = input_str[:cursor_pos-1] + input_str[cursor_pos:]
                cursor_pos -= 1
            elif key == curses.KEY_LEFT and cursor_pos > 0:
                cursor_pos -= 1
            elif key == curses.KEY_RIGHT and cursor_pos < len(input_str):
                cursor_pos += 1
            else:
                pass


        # Redraw input field:
        stdscr.addstr(y, x, input_str + " ")
        stdscr.refresh()


def input_string(stdscr, y, x, question, answer_length):
    """Ask user to input something and return it as a string"""
    curses.echo()
    curses.curs_set(True)
    display_question(stdscr, y, x, question, Color.PROMPTS)
    stdscr.refresh()
    try:
        # answer = stdscr.getstr(y, len(question) + x, answer_length).decode(encoding="utf-8")
        answer = input_field(stdscr, y, len(question) + x, answer_length)
    except (UnicodeDecodeError, KeyboardInterrupt):
        answer = ""
        logging.warning("Incorrect characters in user input.")
    curses.noecho()
    curses.curs_set(False)
    return answer


def input_integer(stdscr, y, x, question):
    """Ask user for an integer number and check if it is an integer"""
    number = input_string(stdscr, y, x, question, 3)
    try:
        number = int(number) - 1
    except (ValueError, KeyboardInterrupt):
        logging.warning("Incorrect number input.")
        return None
    return number


def input_day(stdscr, y, x, prompt_string):
    """Ask user for an integer number and check if it is an integer"""
    number = input_string(stdscr, y, x, prompt_string, 2)
    try:
        number = int(number)
    except (ValueError, KeyboardInterrupt):
        logging.warning("Incorrect day input.")
        return None
    return number


def input_date(stdscr, y, x, prompt_string):
    """Ask user to input date in YYYY/MM/DD format and check if it was a valid entry"""
    date_unformatted = input_string(stdscr, y, x, prompt_string, 10)
    try:
        year = int(date_unformatted.split("/")[0])
        month = int(date_unformatted.split("/")[1])
        day = int(date_unformatted.split("/")[2])
        return year, month, day
    except (ValueError, IndexError, KeyboardInterrupt):
        logging.warning("Incorrect date input.")
        return None, None, None


def input_frequency(stdscr, y, x, question):
    """Ask user for the frequency of event repetitions"""
    freq = input_string(stdscr, y, x, question, 2)
    if freq == 'd':
        return Frequency.DAILY
    if freq == 'w':
        return Frequency.WEEKLY
    if freq == 'm':
        return Frequency.MONTHLY
    if freq == 'y':
        return Frequency.YEARLY
    if freq == 'n':
        return Frequency.ONCE
    return None


def ask_confirmation(stdscr, question, confirmations_enabled):
    """Ask user confirmation for an action"""
    if not confirmations_enabled:
        return True
    y_max, _ = stdscr.getmaxyx()
    curses.halfdelay(255)
    display_question(stdscr, y_max - 2, 0, question, Color.CONFIRMATIONS)
    key = stdscr.getkey()
    confirmed = (key == "y")
    return confirmed


def vim_style_exit(stdscr, screen):
    """Handle vim style key combinations like ZZ and ZQ for exit"""
    if screen.key == "Z":
        try:
            screen.key = stdscr.getkey()
            return (screen.key in ["Z", "Q"])
        except KeyboardInterrupt:
            return True
    else:
        return False
