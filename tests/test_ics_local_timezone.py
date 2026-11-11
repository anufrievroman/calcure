"""Regression test for ICS event times across a DST change."""
import os
import tempfile
import time
import unittest
from types import SimpleNamespace

from calcure.loaders import EventLoaderICS

ICS = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
DTSTART;TZID=Europe/Berlin:20261005T093000
DTEND;TZID=Europe/Berlin:20261005T100000
UID:summer@example.com
SUMMARY:Summer meeting
END:VEVENT
BEGIN:VEVENT
DTSTART;TZID=Europe/Berlin:20261207T093000
DTEND;TZID=Europe/Berlin:20261207T100000
UID:winter@example.com
SUMMARY:Winter meeting
END:VEVENT
END:VCALENDAR
"""


class ICSLocalTimezoneTests(unittest.TestCase):
    def setUp(self):
        self.old_tz = os.environ.get("TZ")
        os.environ["TZ"] = "Europe/Berlin"
        time.tzset()

    def tearDown(self):
        if self.old_tz is None:
            del os.environ["TZ"]
        else:
            os.environ["TZ"] = self.old_tz
        time.tzset()

    def test_events_keep_their_hour_on_both_sides_of_dst(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "events.ics")
            with open(path, "w") as f:
                f.write(ICS)
            config = SimpleNamespace(ICS_EVENT_FILES=[path], USE_PERSIAN_CALENDAR=False)
            events = EventLoaderICS(config).load().items

        self.assertEqual([(e.hour, e.minute) for e in events], [(9, 30), (9, 30)])


if __name__ == "__main__":
    unittest.main()
