import argparse
import logging
import Logger.Logger as Logger
from synchronizer.FolderSynchronization import FolderSynchronization
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description='File Synchronization')

    # positional arguments
    parser.add_argument(dest='source', type=str, help='Absolute path to source directory.')
    parser.add_argument(dest='replica', type=str, help='Absolute path replica directory.')

    # optional arguments
    parser.add_argument('-i', dest='interval', type=int, help='Synchronization interval in seconds.', default=2)
    parser.add_argument('-lf', dest='log_file', type=str, help='Absolute path to log file.', default='logs/sync.log')
    return parser.parse_args()


def main():
    args = parse_args()
    Logger.setup_logging(Path(args.log_file))
    fs = FolderSynchronization(args.source, args.replica, args.interval)
    try:
        fs.run()
    except KeyboardInterrupt:
        logging.info("Exiting the program")


if __name__ == '__main__':
    main()
