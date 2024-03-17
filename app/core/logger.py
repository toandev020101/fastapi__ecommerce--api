import os
import sys
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

# Create a logs folder in the user directory if it doesn't already exist
log_dir = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


# Function to create path for new log file
def get_log_file_path():
    today = datetime.now()
    year_month = today.strftime("%Y/%m")
    log_file_name = f"{today.strftime('%Y-%m-%d')}_api.log"
    log_file_path = os.path.join(log_dir, year_month, log_file_name)

    # Create folders for year and month if they don't already exist
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    return os.path.join(log_dir, year_month, log_file_name)


# get logger
logger = logging.getLogger('logger')

# create formatter
formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")  # Add a closing parenthesis here

# create handlers
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = TimedRotatingFileHandler(get_log_file_path(), when="midnight", interval=1, backupCount=7,
                                        encoding='utf-8')

# set formatters
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# add handlers to the logger
logger.handlers = [stream_handler, file_handler]

# set log-level
logger.setLevel(logging.INFO)  # Change INFO to logging.INFO
