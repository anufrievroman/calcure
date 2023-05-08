"""Module that controls logging and error output"""

import logging
import io

from calcure.configuration import cf


class Error():
    """Error messages displayed to the user.
    Different errors have different purposes:
    ERROR type is reserved for loading errors;
    WARNING type is reserved for incorrect user input;"""

    def __init__(self):
        self.buffer = io.StringIO()
        self.file = f"{cf.config_folder}/info.log"

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


# Initialise error:
error = Error()

# Start logging:
logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)s] %(message)s",
                    # encoding='utf-8',
                    handlers=[logging.FileHandler(error.file, 'w'),
                              logging.StreamHandler(),
                              logging.StreamHandler(error.buffer),
                              ])
