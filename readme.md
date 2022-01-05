# Calcure

Minimalist TUI calendar and task manager with customizable interface. Manages your events and tasks, displays birthdays from your [abook](https://abook.sourceforge.io/), and can import events and tasks from [calcurse](https://github.com/lfos/calcurse).

![screenshot](screenshot.jpeg)

## Features

- Vim keys
- Operation with fewest key presses possible
- Todo list with subtasks and timers ⌚
- Birthdays of your abook contacts
- Import of events and tasks from calcurse
- Icons according to the name ✈ ⛷ ⛱
- Privacy mode ••••• to obfuscate events and tasks
- Plain text database in your folder for cloud sync
- Customizable colors, icons, and other features
- Resize and mobile friendly
- Week can start on any day
- Current weather ⛅


## Installation

### On Arch-based Linux distributions

The package `calcure` is available in AUR. Install it with `yay -S calcure` or with another AUR helper.

### On other Linux distributions

Just copy the `calcure` file into a directory with your binaries and make it executable. For example:

```
git clone https://github.com/anufrievroman/calcure
cp calcure/calcure $HOME/.local/bin
chmod =rwx $HOME/.local/bin/calcure
```

## Dependencies

It only requires python 3. On Linux and MacOS, you should have it by default, but if you don't, install `python` package from your standard repository.


## Usage

Run `calcure` in your terminal. 

### User arguments

`-c` - Start on the calendar page (default)

`-j` - Start on the journal page

`-h` - Start on the help page

`-p` - Start in the privacy mode (text is obfuscated as •••••)

`-v` - Print the version and exit

`--folder=FOLDERNAME` - Use datafiles (events and tasks) stored in a specific folder. For example, if you want to have separate databases for work and for personal things, you can start as `calcure --folder=$HOME/.calcure/work` or `calcure --folder=$HOME/.calcure/personal`. The same effect can basically be achived with the `--config` argument, as explained below.

`--config=CONFIGFILE.ini` - Use specific config file instead of the default one. For example, if you want to separate not only datafiles, like in the previous example, but other settings too, you can run program with alternative config as `calcure --config=$HOME/.config/calcure/config2.ini`. If the specified config file does not exist, it will be created with default settings.

## Keybindings

Besides keybindings listed below, various vim-style keybinding (`ZZ`, `ZQ` etc) and dedicated buttons (`home` etc) are supported as well.

### General

`space` · Switch between calendar and tasks

`*` · Toggle privacy mode

`?` · Show keybindings

`q` · quit


### Calendar view

`n`,`j`,`l`,`↓`  · Next month

`p`,`h`,`k`,`↑` · Previous month

`a` · Add an event

`A` · Add a recurring event

`i` · Mark/unmark an event as important

`d`,`x` · Delete an event

`e` · Edit an event

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

`i` · Mark a task as important

`I` · Mark all tasks as important

`d` · Delete a task and all its subtasks

`D` · Delete all tasks

`t` · Start / pause timer for a task

`T` · Remove a timer

`m` · Move a task

`s` · Toggle between task and subtask

`e` · Edit a task

`C` · Import tasks from Calcurse


## Configuration

On the first run, it will create a configuration file at `.config/calcure/config.ini`

You can edit parameters and colors in the `config.ini` file. Here is an example config (don't forget to change *username*):

```
[Parameters]
folder_with_datafiles = /home/username/.config/calcure
calcurse_todo_file = /home/username/.local/share/calcurse/todo
calcurse_events_file = /home/username/.local/share/calcurse/apts
default_view = calendar
birthdays_from_abook = Yes
show_keybindings = Yes
privacy_mode = No
show_weather = No
show_day_names = Yes
minimal_today_indicator = Yes
minimal_days_indicator = Yes
minimal_weekend_indicator = Yes
cut_titles_by_cell_length = No
ask_confirmations = Yes
use_unicode_icons = Yes
start_week_day = 1
refresh_interval = 1
event_icon = •
privacy_icon = •
today_icon = •
birthday_icon = ★
hidden_icon = ...
done_icon = ✔
todo_icon = •
important_icon = ‣
timer_icon = ⌚
show_header = Yes
header = TASKS:

[Colors]
color_today = 2
color_days = 7
color_day_names = 4
color_weekends = 1
color_weekend_names = 1
color_hints = 7
color_prompts = 7
color_confirmations = 1
color_birthdays = 1
color_todo = 7
color_done = 6
color_title = 4
color_important = 1
color_timer = 2
color_timer_paused = 7

[Dialogues]
calendar_hint = Space: Tasks · n/p: Change month · a: Add event · ?: Keybindings
todo_hint = Space: Calendar · a: Add · v: Done · i: Important · ?: Keybindings

[Event icons]
travel = ✈
plane = ✈
trip = ✈
voyage = ✈
flight = ✈
airport = ✈
vacation = ⛱
holyday = ⛱
day-off = ⛱
hair = ✂
barber = ✂
beauty = ✂
nails = ✂
game = ♟
match = ♟
play = ♟
interview = ♟
date = ♥
concert = ♪
dance = ♪
music = ♪
rehersal = ♪
call = ✆
phone = ✆
zoom = ✆
deadline = ⚑
over = ⚑
finish = ⚑
end = ⚑
doctor = ✚
dentist = ✚
medical = ✚
hospital = ✚
party = ☘
bar = ☘
museum = ⛬
meet = ⛬
talk = ⛬
conference = ⛬
hearing = ⛬
sport = ⛷
gym = ⛷
training = ⛷
email = ✉
letter = ✉

```
When configuring colors, the numbers indicate standart colors of your terminal and by usually mean: 

1 - red, 2 - green, 3 - yellow, 4 - blue, 5 - magenta, 6 - cyan, 7 - white


## Contribution and donations

If you wish to contribute, feel free to open issues or propose PRs. Particularly, you are welcome to contribute on the topics of file encryption, sycing with popular calendar services, and translations. If you'd like to support the development, consider [donations](https://www.buymeacoffee.com/angryprofessor).
