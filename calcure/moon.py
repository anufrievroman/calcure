"""Module that controls display of the moon phases"""

from datetime import datetime
from astral import moon

def get_moon_phase(year, month, day):
    """Return the icon and the description of the moon phase for given day"""
    phase = moon.phase(datetime(year, month, day))
    if  0 <= phase <= 1:
        return " 🌑"
    elif 7 <= phase <= 8:
        return " 🌓"
    elif 14 <= phase <= 15:
        return " 🌕"
    elif 21 <= phase <= 22:
        return " 🌗"
    else:
        return ""


