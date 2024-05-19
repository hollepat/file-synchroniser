import os
import argparse


class FileSynchronization:
    def __init__(self, source, replica):
        self.source = source
        self.replica = replica

        # periodical synchronization
        self._synchronize()

    def _synchronize(self):
        print(f"Synchronizing files from {self.source} to {self.replica}")


def parse_args():
    parser = argparse.ArgumentParser(description='File Synchronization')

    # positional arguments
    parser.add_argument(dest='source', type=str, help='source directory')
    parser.add_argument(dest='replica', type=str, help='replica directory')

    # optional arguments
    parser.add_argument('-i', dest='interval', type=int, help='synchronization interval in seconds')
    parser.add_argument('-lf', dest='log_file', type=str, help='log file path')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    fs = FileSynchronization(args.source, args.replica)
