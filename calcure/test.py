
import curses

def main(stdscr):
    curses.curs_set(1)
    stdscr.clear()
    stdscr.addstr("Enter characters (ESC to exit):\n")

    while True:
        ch = stdscr.get_wch()  # This reads a wide character (Unicode)

        if isinstance(ch, str):
            if ord(ch) == 27:  # ESC key
                break
            stdscr.addstr(f"Input: {ch} -> Unicode: {ord(ch)}\n")
        else:
            stdscr.addstr(f"Special key code: {ch}\n")

        stdscr.refresh()

curses.wrapper(main)
