"""This is a test for implement async loading of weather. Not really working yet"""

import asyncio
import curses

async def load_weather():
    # your weather loading code here
    await asyncio.sleep(3)  # simulate some work
    return "New weather"


async def draw_interface(stdscr):
    # your curses interface drawing code here
    weather = ""
    weather = await load_weather()
    while True:
        stdscr.addstr(0, 0, weather)
        stdscr.refresh()
        key = stdscr.getkey()
        stdscr.refresh()


def main():
    stdscr = curses.initscr()
    # curses.cbreak()
    stdscr.keypad(True)
    stdscr.clear()

    loop = asyncio.get_event_loop()
    loop.create_task(draw_interface(stdscr))
    loop.run_forever()

    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

if __name__ == '__main__':
    main()
