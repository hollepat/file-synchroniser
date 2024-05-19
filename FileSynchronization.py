import os
import time
import argparse
import hashlib
import logging

logger = logging.getLogger(__name__)


class FileSynchronization:
    def __init__(self, source: str, replica: str, interval: int = 5):
        self.source = source
        self.replica = replica
        if interval is None:
            self.sync_interval = 5
        else:
            self.sync_interval = interval

        # periodical synchronization
        while True:
            self._synchronize()
            time.sleep(self.sync_interval)

    def _synchronize(self):
        logger.info(f"Synchronizing files from {self.source} to {self.replica}")
        if self.are_different(self.source, self.replica):
            # TODO: write recursive synchronization logic here
            logger.info("Folders are different! Syncing files...")
            self._sync_files()

    def _sync_files(self):
        """read, update, delete files from source to replica"""
        pass

    def are_different(self, folder1_path, folder2_path, algorithm='md5') -> bool:
        """Check if two folders are different by comparing their checksums.

        :param folder1_path: path to the first folder
        :param folder2_path: path to the second folder
        :param algorithm: hashing algorithm to use (default: 'md5')
        :return: True if the folders are different, False otherwise
        """
        folder1_structure = self.get_folder_structure(folder1_path, algorithm)
        folder2_structure = self.get_folder_structure(folder2_path, algorithm)
        return not self.compare_folders(folder1_structure, folder2_structure)

    def get_folder_structure(self, folder_path, algorithm='md5'):
        folder_structure = {}
        for root, dirs, files in os.walk(folder_path):
            logger.debug(f"Processing {root}, {dirs}, {files}")
            relative_path = os.path.relpath(root, folder_path)
            folder_structure[relative_path] = {'files': {}, 'dirs': dirs}
            for filename in files:
                file_path = os.path.join(root, filename)
                folder_structure[relative_path]['files'][filename] = self.calculate_checksum(file_path, algorithm)
        return folder_structure

    @staticmethod
    def compare_folders(folder1_structure, folder2_structure) -> bool:
        """Compare the structure of two folders.

        :param folder1_structure: structure of the first folder
        :param folder2_structure: structure of the second folder
        :return: True if the folders are the same, False otherwise
        """
        # Compare the keys (relative paths)
        if folder1_structure.keys() != folder2_structure.keys():
            return False

        for path in folder1_structure:
            # Compare the directories at each path
            if set(folder1_structure[path]['dirs']) != set(folder2_structure[path]['dirs']):
                return False

            # Compare the files at each path
            if folder1_structure[path]['files'] != folder2_structure[path]['files']:
                return False

        return True

    @staticmethod
    def calculate_checksum(file_path, algorithm='md5'):
        hash_func = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    def has_folder_changed(self, initial_checksums, folder_path, algorithm='md5') -> bool:
        # check if the source and replica folders are different
        current_checksums = self.get_folder_checksums(folder_path, algorithm)
        return initial_checksums != current_checksums

    def get_folder_checksums(self, folder_path, algorithm='md5'):
        folder_checksums = {}
        for root, _, files in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                folder_checksums[file_path] = self.calculate_checksum(file_path, algorithm)
        return folder_checksums


def setup_logger(log_file_path, log_level=logging.DEBUG):
    if log_file_path is None:
        log_file_path = './sync.log'

    # Create a custom logger
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_file_path)

    # Set level for handlers
    console_handler.setLevel(log_level)
    file_handler.setLevel(log_level)

    # Create formatters and add it to handlers
    console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


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
    logger = setup_logger(args.log_file)
    fs = FileSynchronization(args.source, args.replica, args.interval)
