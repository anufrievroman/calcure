# Calcure

Modern TUI calendar and task manager with customizable interface. Manages your events and tasks, displays birthdays from your [abook](https://abook.sourceforge.io/), and can import events and tasks from [calcurse](https://github.com/lfos/calcurse) and [taskwarrior](https://github.com/GothenburgBitFactory/taskwarrior). See [wiki](https://github.com/anufrievroman/calcure/wiki) for more information.

![screenshot](screen.jpg)

## Features

- Vim keys
- Operation with fewest key presses possible
- Todo list with subtasks and timers ⌚
- Birthdays of your abook contacts
- Import of events and tasks from calcurse and taskwarrior
- Icons according to the name ✈ ⛷ ⛱
- Privat events and tasks •••••
- Plain text database in your folder for cloud sync
- Customizable colors, icons, and other features
- Resize and mobile friendly
- Week can start on any day
- Current weather ⛅
- Support for Persian calendar


## Installation

### Linux and Mac OS

`pip install calcure`


### Arch Linux, Manjaro etc

The package `calcure` is available in AUR. 

`yay -S calcure`

Also, you need to install `holidays` and `jdatetime` libraries:

`pip install holidays jdatetime`


### Windows

1. Install `Windows Terminal` app from the app store
2. Install `python 3.x` also from the app store (if you just type `python` in the Windows Terminal app it will offer you to install)
3. Install the program and libraries libraries by typing in the Windows Terminal `pip install windows-curses calcure`
4. Now you can finally run it by typing in the Windows Terminal `python -m calcure`


## Dependencies

- python 3
- `holidays` and `jdatetime` python libraries. Install by `pip install holidays jdatetime`.

## Usage

Run `calcure` in your terminal. You may need to restart your terminal after install.

### User arguments

Calcure can be started in special mods using the following user arguments:

`-j` · Start on the journal page

`-i` · Start using Persian calendar

`-h` · Start on the help page

`-p` · Start in the privacy mode (text is obfuscated as •••••)

`-v` · Print the version and exit

`--folder=FOLDERNAME` - Use datafiles (events and tasks) stored in a specific folder. For example, if you want to have separate databases for work and for personal things, you can start as:
`calcure --folder=$HOME/.calcure/work` or `calcure --folder=$HOME/.calcure/personal`
The same effect can also be achieved with the `--config` argument, as explained below.

`--config=CONFIGFILE.ini` - Use specific config file instead of the default one. For example, if you want to separate not only datafiles, like in the previous example, but other settings too, you can run the program with alternative config as:

`calcure --config=$HOME/.config/calcure/config2.ini`

If the specified config file does not exist, it will be created with default settings.

## Key bindings

Besides key bindings listed below, various vim-style key binding (`ZZ`, `ZQ` etc) and dedicated buttons (`home` etc) are supported as well.

### General

`space` · Switch between calendar and tasks

`/` · Toggle split screen

`*` · Toggle privacy mode

`?` · Show keybindings

`q` · quit


### Calendar view

`n`,`l`,`↓`  · Next month

`p`,`k`,`↑` · Previous month

`a` · Add an event

`A` · Add a recurring event

`h` · Mark/unmark an event as high priority

`l` · Mark/unmark an event as low priority

`d` · Delete an event

`e` · Edit an event

`m` · Move an event

`.` · Toggle privacy of an event

`g` · Go to selected day

`C` · Import events from Calcurse

`G` - return to current month


### Tasks view

`a` · Add a task

`A` · Add a subtask

`v` · Mark a task as done

`V` · Mark all tasks as done

`u` · Unmark a task

`U` · Unmark all tasks

`h` · Mark/unmark a task as important

`H` · Mark/unmark all tasks as important

`l` · Mark/unmark a task as low priority

`L` · Mark/unmark all tasks as low priority

`.` · Toggle privacy of a task

`d` · Delete a task and all its subtasks

`D` · Delete all tasks

`t` · Start / pause timer for a task

`T` · Remove a timer

`m` · Move a task

`s` · Toggle between task and subtask

`e` · Edit a task

`C` · Import tasks from Calcurse

`W` · Import tasks from Taskwarrior


## Configuration

On the first run, program will create a configuration file at `.config/calcure/config.ini`

You can edit parameters and colors in the `config.ini` file. Example of the [config.ini file is here](https://github.com/anufrievroman/calcure/wiki/Default-config.ini). Explanations of all options are [available in the wiki](https://github.com/anufrievroman/calcure/wiki/Settings).


## Troubleshooting

- If your terminal shows empty squares instead of icons, probably it does not support unicode. In this case, in config set: `use_unicode_icons = No`.
- Weather widget slows down launch of the program and requires internet. If that is a problem, switch weather off in config: `show_weather = No`.
- If weather is incorrect, set your city in config `weather_city = Tokyo`. By default, this setting is empty and program tries to detect your city automatically from your ip.
- If after install the program does not run by just running `calcure`, try to restart your terminal, it may need to recheck the binaries.

## Contribution, translations, donations

If you wish to contribute to the code base or translations, feel free to open issues or propose PRs. Particularly, you are welcome to contribute on the topics of file encryption and syncing with popular calendar services. For big changes, please open an issue to discuss first. 

If you'd like to support the development, consider [donations](https://www.buymeacoffee.com/angryprofessor).
For more information about contribution, see [wiki pages](https://github.com/anufrievroman/calcure/wiki/Contribution).
