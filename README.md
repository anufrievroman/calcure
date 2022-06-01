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
- Private events and tasks •••••
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

Calcure can be started in special mods using various user arguments. Please refer [to this wiki page](https://github.com/anufrievroman/calcure/wiki/User-arguments) for the list of options.

## Key bindings

List of all key bindings can be accessed [in the wiki](https://github.com/anufrievroman/calcure/wiki/Key-bindings) and via `?` key in the program.

## Settings

On the first run, program will create a configuration file at `.config/calcure/config.ini`.
You can edit parameters and colors in the `config.ini` file.
An example of the [config.ini file is here](https://github.com/anufrievroman/calcure/wiki/Default-config.ini).
Explanations of all settings are [in the wiki](https://github.com/anufrievroman/calcure/wiki/Settings).

## Troubleshooting

- If your terminal shows empty squares instead of icons, probably it does not support unicode. In this case, in config set: `use_unicode_icons = No`.
- Weather widget slows down launch of the program and requires internet. If that is a problem, switch weather off in config: `show_weather = No`.
- If weather is incorrect, set your city in config `weather_city = Tokyo`. By default, this setting is empty and program tries to detect your city automatically from your ip.
- If after install the program does not run by just running `calcure`, try to restart your terminal, it may need to recheck the binaries.

## Contribution, translations, donations

If you wish to contribute to the code base or translations, feel free to open issues or propose PRs. Particularly, you are welcome to contribute on the topics of file encryption and syncing with popular calendar services. For big changes, please open an issue to discuss first. 

If you'd like to support the development, consider [donations](https://www.buymeacoffee.com/angryprofessor).
For more information about contribution, see [wiki pages](https://github.com/anufrievroman/calcure/wiki/Contribution).
