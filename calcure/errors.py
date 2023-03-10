"""Module that controls logging and error output"""

import logging
import io

from calcure.configuration import cf


class Error():
    """Error messages displayed to the user"""

    def __init__(self):
        self.buffer = io.StringIO()
        self.file = f"{cf.config_folder}/info.log"

    def get_error_text(self):
        """Returns string with the text of the error"""
        return self.buffer.getvalue()

    def clear_buffer(self):
        """Clear the buffer containing errors"""
        self.buffer = io.StringIO()

    @property
    def has_occured(self):
        """Has any errors occured?"""
        return self.get_error_text() != ""


# Initialise error:
error = Error()

# Start logging:
logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)s] %(message)s",
                    encoding='utf-8',
                    handlers=[logging.FileHandler(error.file, 'w'),
                              logging.StreamHandler(),
                              logging.StreamHandler(error.buffer),
                              ])
