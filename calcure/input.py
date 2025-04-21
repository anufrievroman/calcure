import curses

def input_field(stdscr, prompt="Enter text: "):
    curses.curs_set(1)  # Show cursor
    stdscr.clear()
    stdscr.addstr(0, 0, prompt)
    stdscr.refresh()

    input_str = ""
    cursor_pos = 0
    start_x = len(prompt)  # Fixed starting position of input

    while True:
        stdscr.move(0, start_x + cursor_pos)  # Move cursor
        key = stdscr.getch()

        if key == 27:  # Escape key
            return None
        elif key in (curses.KEY_ENTER, 10, 13):  # Enter key
            return input_str
        elif key in (curses.KEY_BACKSPACE, 127):  # Backspace key
            if cursor_pos > 0:
                input_str = input_str[:cursor_pos-1] + input_str[cursor_pos:]
                cursor_pos -= 1
        elif key == curses.KEY_LEFT:  # Move cursor left
            if cursor_pos > 0:
                cursor_pos -= 1
        elif key == curses.KEY_RIGHT:  # Move cursor right
            if cursor_pos < len(input_str):
                cursor_pos += 1
        elif 32 <= key <= 126:  # Printable ASCII characters
            input_str = input_str[:cursor_pos] + chr(key) + input_str[cursor_pos:]
            cursor_pos += 1

        # Redraw input field
        stdscr.addstr(0, start_x, input_str + " ")  # Extra space clears deleted characters
        stdscr.refresh()

def main(stdscr):
    stdscr.clear()
    stdscr.addstr("Press Enter after typing, or Esc to exit.\n")
    stdscr.refresh()

    user_input = input_field(stdscr)

    stdscr.clear()
    if user_input is None:
        stdscr.addstr("Input cancelled.\n")
    else:
        stdscr.addstr(f"You entered: {user_input}\n")

    stdscr.addstr("Press any key to exit.")
    stdscr.getch()

curses.wrapper(main)

