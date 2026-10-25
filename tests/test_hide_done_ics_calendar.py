"""Regression tests for hiding completed iCalendar tasks in calendar deadlines."""
import datetime
import unittest
from types import SimpleNamespace

from icalendar import Todo

from calcure.loaders import TaskLoaderICS


class HideDoneICSTasksInCalendarTests(unittest.TestCase):
    def loader_with_tasks(self, hide_done):
        config = SimpleNamespace(
            HIDE_DONE_TASKS=hide_done,
            ICS_TASK_FILES=None,
            USE_PERSIAN_CALENDAR=False,
        )
        loader = TaskLoaderICS(config)
        due = datetime.date(2030, 1, 2)
        for summary, status in (
            ("synthetic completed task", "COMPLETED"),
            ("synthetic active task", "NEEDS-ACTION"),
        ):
            todo = Todo()
            todo.add("summary", summary)
            todo.add("status", status)
            todo.add("due", due)
            loader.parse_task(todo, calendar_number=0)
        return loader.user_ics_tasks

    def calendar_deadlines(self, tasks):
        screen = SimpleNamespace(year=2030, month=1, day=2)
        return [task.name for task in tasks.filter_events_that_day(screen).items]

    def test_hidden_completed_ics_tasks_are_omitted_from_calendar_deadlines(self):
        tasks = self.loader_with_tasks(hide_done=True)

        self.assertEqual(
            ["synthetic active task"],
            self.calendar_deadlines(tasks),
        )

    def test_completed_ics_tasks_remain_when_hiding_is_disabled(self):
        tasks = self.loader_with_tasks(hide_done=False)

        self.assertEqual(
            ["synthetic completed task", "synthetic active task"],
            self.calendar_deadlines(tasks),
        )


if __name__ == "__main__":
    unittest.main()
