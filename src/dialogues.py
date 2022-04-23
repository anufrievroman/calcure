import curses

def display_question(stdscr, y, x, question, color):
    '''Display the line of text respecting the slyling and available space'''
    y_max, x_max = stdscr.getmaxyx()
    if y >= y_max or x >= x_max: return
    question = question[:(x_max - x - 1)]
    stdscr.addstr(y, x, question, curses.color_pair(color))


def clear_line(stdscr, y):
    '''Clear a line from any text'''
    _, x_max = stdscr.getmaxyx()
    stdscr.addstr(y, 0, " "*(x_max - 2), curses.color_pair(21))


def input_string(stdscr, y, x, question, answer_length):
    '''Ask user to input something and return it as a string'''
    _, x_max = stdscr.getmaxyx()
    curses.echo()
    curses.curs_set(True)
    display_question(stdscr, y, x, question, 8)
    stdscr.refresh()
    answer = stdscr.getstr(y, len(question) + x, answer_length).decode(encoding="utf-8")
    curses.noecho()
    curses.curs_set(False)
    return answer


def input_integer(stdscr, y, x, prompt_string):
    '''Ask user for an integer number and check if it is an integer'''
    number = input_string(stdscr, y, x, prompt_string, 3)
    try:
        number = int(number) - 1
    except ValueError:
        return None
    return number


def input_day(stdscr, y, x, prompt_string):
    '''Ask user for an integer number and check if it is an integer'''
    number = input_string(stdscr, y, x, prompt_string, 2)
    try:
        number = int(number)
    except ValueError:
        return None
    return number


def ask_confirmation(stdscr, question, confirmations_enabled):
    '''Ask user confirmation for an action'''
    if not confirmations_enabled: return True
    y_max, x_max = stdscr.getmaxyx()
    curses.halfdelay(255)
    display_question(stdscr, y_max-2, 0, question, 9)
    key = stdscr.getkey()
    confirmed = True if key == "y" else False
    return confirmed
