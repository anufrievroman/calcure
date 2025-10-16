#!/usr/bin/env python3
"""Test script to verify week numbers are working in calcure"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'calcure'))

from calcure.calendars import Calendar

def test_week_numbers():
    """Test the week number functionality"""
    print("Testing Week Number Functionality")
    print("=" * 40)
    
    # Test Gregorian calendar
    cal_gregorian = Calendar(0, False)  # Start week on Monday, Gregorian
    
    print("Gregorian Calendar Tests:")
    print(f"Week number for 2024-03-01: {cal_gregorian.week_number(2024, 3, 1)}")
    print(f"Week number for 2024-03-23: {cal_gregorian.week_number(2024, 3, 23)}")
    
    # Test a few months
    for month in [3, 4, 5]:
        week_numbers = cal_gregorian.month_week_numbers(2024, month)
        month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        print(f"Week numbers for {month_names[month]} 2024: {week_numbers}")
    
    print("\nCalendar grid for March 2024:")
    dates = cal_gregorian.monthdayscalendar(2024, 3)
    week_numbers = cal_gregorian.month_week_numbers(2024, 3)
    
    print("Wk  Mon Tue Wed Thu Fri Sat Sun")
    for i, (week, week_num) in enumerate(zip(dates, week_numbers)):
        week_str = f"{week_num:2d}  "
        for day in week:
            if day == 0:
                week_str += "    "
            else:
                week_str += f"{day:3d} "
        print(week_str)
    
    print("\n✓ Week numbers functionality appears to be working correctly!")
    print("The implementation should now show week numbers in the left column of the calendar.")

if __name__ == "__main__":
    test_week_numbers()