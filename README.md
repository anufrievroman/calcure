# Calcure


Modern TUI calendar and task manager with customizable interface. Manages your events and tasks, displays birthdays from your [abook](https://abook.sourceforge.io/), and can import events and tasks from [calcurse](https://github.com/lfos/calcurse) and [taskwarrior](https://github.com/GothenburgBitFactory/taskwarrior). See [wiki](https://anufrievroman.gitbook.io/calcure/) for more information.

![screenshot](screenshot.png)

## Features

- Vim keys
- View tasks and events from .ics file synced with clouds
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

`pip install calcure`

### Windows

1. Install `Windows Terminal` app from the app store
2. Install `python 3.x` also from the app store (if you just type `python` in the Windows Terminal app it will offer you to install)
3. Install the program and libraries libraries by typing in the Windows Terminal `pip install windows-curses calcure`
4. Now you can finally run it by typing in the Windows Terminal `python -m calcure`

### Upgrade to the most recent version

`pip install --upgrade calcure`

## Dependencies

- python 3
- `holidays`, `jdatetime`, and 'ics' python libraries. Install by `pip install holidays jdatetime ics`.

## Usage

Run `calcure` in your terminal. You may need to restart your terminal after the install.

### Syncing with cloud calendars

Calcure can display in read-only mode events and tasks from Nextcloud, Google, and other calendars. See this [wiki page](https://anufrievroman.gitbook.io/calcure/syncing-with-clouds) for examples.

### User arguments

Calcure supports automations and can be started in special mods using various user arguments. Please refer [to this wiki page](https://anufrievroman.gitbook.io/calcure/user-arguments) for the list of options.

### Key bindings

[List of all key bindings](https://anufrievroman.gitbook.io/calcure/key-bindings) can be accessed in the wiki and via `?` key in the program.

### Settings

On the first run, program will create a configuration file at `~/.config/calcure/config.ini`.
You can edit parameters, colors, and icons in the `config.ini` file.
See [wiki](https://anufrievroman.gitbook.io/calcure/) for the [example of config.ini file](https://anufrievroman.gitbook.io/calcure/default-config) and [explanations of all settings](https://anufrievroman.gitbook.io/calcure/settings).

## Troubleshooting

- If your terminal shows empty squares instead of icons, probably it does not support unicode. In this case, in config set: `use_unicode_icons = No`.
- Weather widget slows down launch of the program and requires internet. If that is a problem, switch weather off in config: `show_weather = No`.
- If weather is incorrect, set your city in config `weather_city = Tokyo`. By default, this setting is empty and program tries to detect your city automatically from your ip.
- If after install the program does not run by just running `calcure`, try to restart your terminal, it may need to recheck the binaries.


## Contribution, translations, donations

For full information about contribution, see [wiki pages](https://anufrievroman.gitbook.io/calcure/contribution).

If you wish to contribute to the development or translations, feel free to open issues or propose PRs. Particularly, you are welcome to contribute to translations (create a copy of `en.py` in translations folder in your language), packaging for repositories, and syncing with popular calendar services. For big changes, please open an issue to discuss first. 

If you'd like to support the development, consider [donations](https://www.buymeacoffee.com/angryprofessor).

