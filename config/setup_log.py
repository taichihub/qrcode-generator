import logging
import yaml
from config.setting import PROGRAM_SETTINGS

def load_log_messages():
    with open(PROGRAM_SETTINGS["LOG_FILE_PATH"], PROGRAM_SETTINGS["FILE_MODE"], encoding=PROGRAM_SETTINGS["ENCODING"]) as f:
        return yaml.safe_load(f)

def setup_logging():
    logging.basicConfig(level=logging.INFO, format=PROGRAM_SETTINGS["LOGGING_FORMAT"])
    return logging.getLogger(__name__)

LOG_MESSAGES = load_log_messages()
logger = setup_logging()
