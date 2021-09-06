# calcure

Minimalist TUI calendar and task manager with customizable interface. You can manage your events and tasks, view birthdays from your [abook](https://abook.sourceforge.io/), and import events and tasks from [calcurse](https://github.com/lfos/calcurse).

![screenshot](screenshot.jpeg)

## Features

- Vim keys
- Operation with a fewest key presses possible
- Todo list with tasks and subtasks
- Birthdays from your abook contacts
- Import events and tasks from calcurse
- Auto pictograms according to the name ✈ ⛷ ⛱
- Privacy mode ••••• to obfuscate events and tasks
- Simple plain text database in a desired location for cloud sync
- Colors, icons, and other features are fully customizable
- Resize friendly. Can shrink to a small window
- Start week on any day


## Installation

### On Arch-based distributions

The package `calcure` is avalible in AUR. Simply install it with `yay -S calcure` or with another AUR helper.

### On other distributions

Just copy the **calcure** file into a directory with your binaries and make it executable:

```
git clone https://github.com/anufrievroman/calcure
cp calcure/calcure $HOME/.local/bin
chmod =rwx $HOME/.local/bin/calcure
```

## Usage

Run by typing `calcure` in a linux terminal.

## Dependencies

It only requires python 3. You should have it by deafult, but if you don't, install `python` package from your standard repository.

## Key bindings

### General

`space` · Switch between calendar and tasks

`*` · Toggle privacy mode

`?` · Show keybindings

`q` · quit


### Calendar view

`n`,`j`,`l`,`↓`  · Next month

`p`,`h`,`k`,`↑` · Previous month

`a` · Add event

`A` · Add reccuring event

`d` · Delete event

`e` · Edit event

`C` · Imort events from calcurse

`home`,`gg`,`G` - return to current month


### Tasks view

`a` · Add task

`A` · Add subtask

`i` · Mark task as important

`I` · Mark all as important

`d` · Delete task and all subtasks

`D` · Delete all tasks

`s` · Toggle subtask

`e` · Edit task

`C` · Imort tasks from calcurse


## Configuration

On the first run, it will create a configuration file at `.config/calcure/config.ini`

You can edit parameters and colors in the `config.ini` file. Here is an example config:

```
[Parameters]
folder_with_datafiles = /home/user/.config/calcure
calcurse_todo_file = /home/user/.local/share/calcurse/todo
calcurse_events_file = /home/user/.local/share/calcurse/apts
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
ask_confirmations = No
use_unicode_icons = Yes
start_week_day = 1
event_icon = •
privacy_icon = •
today_icon = •
birthday_icon = ★
hidden_icon = ...
done_icon = ✔
todo_icon = •
important_icon = ‣
show_header = Yes
header = TODO LIST:

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
gig = ♪
disco = ♪
music = ♪
rehersal = ♪
call = ☎
phone = ☎
deadline = ⚑
over = ⚑
finish = ⚑
end = ⚑
appointment = ✔
task  = ✔
doctor = ⛑
dentist = ⛑
medical = ⛑
hospital = ⛑
party = ☘
museum = ⛬
meet = ⛬
talk = ⛬
conference = ⛬
hearing = ⛬
sport = ⛷
gym = ⛷
training = ⛷

```
When configuring colors, the numbers mean: 1 - red, 2 - green, 3 - yellow, 4 - blue, 5 - magenta, 6 - cyan, 7 - white

