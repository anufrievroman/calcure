# Calcure


Modern TUI calendar and task manager with customizable interface. Manages your events and tasks, displays birthdays from your [abook](https://abook.sourceforge.io/), and can import events and tasks from [calcurse](https://github.com/lfos/calcurse) and [taskwarrior](https://github.com/GothenburgBitFactory/taskwarrior).

[See documentation](https://anufrievroman.gitbook.io/calcure/) for more information.

![screenshot](screenshot.png)

## Features

- Vim keys
- View tasks and events from .ics files synced with clouds
- Operation with fewest key presses possible
- Todo list with subtasks, deadlines, and timers
- Birthdays of your abook contacts
- Import of events and tasks from calcurse and taskwarrior
- Icons according to the name ✈ ⛷ ⛱
- Private events and tasks •••••
- Plain text database in your folder for cloud sync
- Customizable colors, icons, and other features
- Resize and mobile friendly
- Current weather ⛅
- Support for Persian calendar


## Installation

### Linux and Mac OS

There are several ways to install:

`pipx install calcure` - the up-to-date version from PyPi. You may need to install `pipx` first.

`yay -S calcure` - [AUR package](https://aur.archlinux.org/packages/calcure) is available. Upvote to support the project!

`calcure` is also available as NixOS package.

### Windows

1. Install `Windows Terminal` app from the app store
2. Install `python 3.x` also from the app store (if you just type `python` in the Windows Terminal app it will offer you to install)
3. Install the program and libraries by typing in the Windows Terminal `pip install windows-curses calcure`
4. Now you can finally run it by typing in the Windows Terminal `python -m calcure`

### Upgrade to the most recent version

`pipx upgrade calcure`

### Dependencies

- `python` 3.7 and higher (usually already installed)
- `holidays`, `jdatetime`, `icalendar`, and `taskw` python libraries (should be installed automatically with the calcure).
- `windows-curses` on Windows

## Usage

Run `calcure` in your terminal. You may need to restart your terminal after the install.

### Syncing with cloud calendars

[This page in documentation](https://anufrievroman.gitbook.io/calcure/syncing-with-clouds) shows examples how to sync and display in read-only mode events and tasks from Nextcloud, Google, and other calendars. 

### User arguments

[Various user arguments](https://anufrievroman.gitbook.io/calcure/user-arguments) can be added started in special mods add tasks and events etc.

### Key bindings

[List of all key bindings](https://anufrievroman.gitbook.io/calcure/key-bindings) can be accessed in the wiki and via `?` key in the program.

### Settings

[Example of config.ini file](https://anufrievroman.gitbook.io/calcure/default-config) and [explanations of all settings](https://anufrievroman.gitbook.io/calcure/settings) are available in the documentation.
On the first run, program will create a `config.ini` file where you can edit parameters, colors, and icons at `~/.config/calcure/config.ini`.

### Troubleshooting

[Typical problems and solutions](https://anufrievroman.gitbook.io/calcure/troubleshooting) are described in documentation. If you faced a new problem, don't hesitate to open an issue.


## Contribution

[Full information about contribution](https://anufrievroman.gitbook.io/calcure/contribution) is available in the documentation.

## Support

I am not a professional developer and work on open-source projects in my free time. If you'd like to support the development, consider donations via [buymeacoffee](https://www.buymeacoffee.com/angryprofessor) or cryptocurrencies:

- BTC `bc1qpkzmutdqfxkce34skt09vll97s5smpa0r2tyzj`
- ETH `0x6f1Ce9cA181458Fc153a5f7cBF88044736C3b00C`
- BNB `0x40f22c372758E35C905458cAF8BB17f51ac133d1`
- LTC `ltc1qtu33qyv2xlzxda5mmrmk943zpksq8q75tuh85p`
