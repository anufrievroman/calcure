"""Regression tests for marking truncated monthly event titles."""
import atexit
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Importing the app initializes configuration, so isolate its home and CLI args.
_test_home = tempfile.TemporaryDirectory(prefix="calcure-test-home-")
Path(_test_home.name, ".config").mkdir()
_original_argv = sys.argv
sys.argv = [_original_argv[0]]
try:
    with patch.dict(os.environ, {"HOME": _test_home.name, "USERPROFILE": _test_home.name}):
        with patch.object(Path, "home", return_value=Path(_test_home.name)):
            from calcure.__main__ import UserEventView, cf
finally:
    sys.argv = _original_argv


def _cleanup_test_home():
    import logging

    logging.shutdown()
    _test_home.cleanup()


atexit.register(_cleanup_test_home)

from calcure.data import CalState, Frequency, Status, UserEvent


class EventTitleTruncationTests(unittest.TestCase):
    def setUp(self):
        self.original_settings = {
            "CUT_TITLES": cf.CUT_TITLES,
            "DISPLAY_ICONS": cf.DISPLAY_ICONS,
            "EVENT_ICON": cf.EVENT_ICON,
            "SHOW_CALENDAR_BORDERS": cf.SHOW_CALENDAR_BORDERS,
            "STRIKETHROUGH_DONE": cf.STRIKETHROUGH_DONE,
        }
        cf.CUT_TITLES = True
        cf.DISPLAY_ICONS = False
        cf.EVENT_ICON = "*"
        cf.SHOW_CALENDAR_BORDERS = False
        cf.STRIKETHROUGH_DONE = False

    def tearDown(self):
        for setting, value in self.original_settings.items():
            setattr(cf, setting, value)

    def event_view(self, title):
        event = UserEvent(
            1, 2030, 1, 2, title, 1, Frequency.ONCE, Status.NORMAL, False
        )
        screen = type(
            "Screen",
            (),
            {"x_max": 70, "x": 0, "calendar_state": CalState.MONTHLY, "privacy": False},
        )()
        return UserEventView(None, 0, 0, event, screen)

    def test_truncated_title_ends_with_ellipsis(self):
        view = self.event_view("synthetic title longer than a day cell")

        view.fill_remaining_space()
        view.cut_info()

        self.assertTrue(view.info.rstrip().endswith("…"))
        self.assertEqual(9, len(view.info))

    def test_title_that_fits_is_not_marked_as_truncated(self):
        view = self.event_view("brief")

        view.fill_remaining_space()
        view.cut_info()

        self.assertFalse(view.info.rstrip().endswith("…"))
        self.assertEqual("* brief", view.info.rstrip())


if __name__ == "__main__":
    unittest.main()
