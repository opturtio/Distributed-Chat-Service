import logging
from logging.handlers import RotatingFileHandler

# Configure the log file
LOG_FILE = "P2PChat.log"

# Create the root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)  # Set the logging level

# Remove all existing handlers (including the default StreamHandler) so no console logging occures
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# Create a file handler with rotation
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
))

# Add the file handler to the root logger
root_logger.addHandler(file_handler)

# Shortcut to access the logger
logger = logging.getLogger("P2PChat")
