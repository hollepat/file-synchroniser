import json
import logging.config
import logging.handlers
import pathlib
import logging
import datetime

LOG_FORMAT = '%(asctime)s | %(levelname)8s | %(filename)s:%(lineno)d | %(message)s'


class CustomLogFormatter(logging.Formatter):
    black = '\x1b[30m'
    white = '\x1b[37m'
    magenta = '\x1b[35m',
    cyan = '\x1b[36m',
    green = '\x1b[92m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    background_red = '\x1b[41m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        self.fmt = fmt
        super().__init__()
        self.FORMATS = {
            logging.DEBUG: self.blue + self.fmt + self.reset,
            logging.INFO: self.green + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.black + self.background_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logger(name, log_to_file=False, level=logging.DEBUG):
    logger = logging.getLogger(name)

    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(CustomLogFormatter(LOG_FORMAT))
    logger.addHandler(stdout_handler)

    # remove standard logger
    logger.propagate = False

    if log_to_file:
        today = datetime.datetime.now()
        file_handler = logging.FileHandler('run_{}.log'.format(today.strftime('%Y_%m_%d-%H_%M')))
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(file_handler)

    logger.setLevel(level)
    return logger



def setup_logging(log_file: str) -> None:
    config_file = pathlib.Path("Logger/config.json")
    if config_file.exists():
        with open(config_file, "rt") as file:
            config = json.load(file)
        logging.config.dictConfig(config)
        if "handlers" in config and "file" in config["handlers"]:
            config["handlers"]["file"]["filename"] = log_file
            logging.config.dictConfig(config)
    else:
        print("Config file not found. Using basic configuration.")
        logging.basicConfig(level=logging.INFO)