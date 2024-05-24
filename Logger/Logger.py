import json
import logging.config
import logging.handlers
from pathlib import Path
import logging


def setup_logging(log_file: Path) -> None:
    """Set up logging.

    :param log_file: Absolute path to log file
    """
    config_file = Path("Logger/config.json")
    if config_file.exists():
        with open(config_file, "rt") as file:
            config = json.load(file)
        logging.config.dictConfig(config)
        if "handlers" in config and "file" in config["handlers"]:
            if not log_file.exists():
                log_file.parent.mkdir(parents=True, exist_ok=True)
                log_file.touch(exist_ok=True)
            config["handlers"]["file"]["filename"] = log_file
            logging.config.dictConfig(config)
            print(f"Syncing to {log_file}")
    else:
        print("Config file not found. Using basic configuration.")
        logging.basicConfig(level=logging.INFO)
