import io
import logging

string_buffer = io.StringIO()
logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)s] %(message)s",
                    encoding='utf-8',
                    handlers=[logging.FileHandler("info.log", 'w'),
                              logging.StreamHandler(),
                              logging.StreamHandler(string_buffer),
                              ])

logging.error("Invalid user arguments")

log_variable = string_buffer.getvalue()
print(log_variable)
