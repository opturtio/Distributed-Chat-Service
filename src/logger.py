import logging
from logging.handlers import RotatingFileHandler

# Configure the logger
LOG_FILE = "P2PChat.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# File handler with rotation
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
))

# Attach the handler to the root logger
root_logger = logging.getLogger()
root_logger.addHandler(file_handler)

# Shortcut to access the logger
logger = logging.getLogger("P2PChat")