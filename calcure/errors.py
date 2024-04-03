"""Module that controls logging and error output"""

import logging
import io


class Error():
    """Error messages displayed to the user.
    Different errors have different purposes:
    ERROR type is reserved for loading errors;
    WARNING type is reserved for incorrect user input;"""

    def __init__(self, file):
        self.buffer = io.StringIO()
        self.file = file

        # Start logging errors:
        logging.basicConfig(level=logging.INFO,
                            format="[%(levelname)s] %(message)s",
                            # encoding='utf-8',
                            handlers=[logging.FileHandler(self.file, 'w'),
                                      #logging.StreamHandler(),
                                      logging.StreamHandler(self.buffer),
                                      ])
    @property
    def has_occured(self):
        """Has any errors occured?"""
        return self.buffer.getvalue() != ""

    @property
    def number_of_errors(self):
        """Return the number of different errors in the buffer"""
        return self.buffer.getvalue().count("[")

    @property
    def text(self):
        """Return the string with the text of the error"""
        return self.buffer.getvalue().split("] ")[1]

    @property
    def type(self):
        """Return the string with type of the error"""
        return self.buffer.getvalue().split("] ")[0]

    def clear_buffer(self):
        """Clear the buffer containing errors"""
        self.buffer.seek(0)
        self.buffer.truncate(0)

