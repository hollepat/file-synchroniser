import os
import time
import hashlib
import logging
from pathlib import Path
from typing import Dict

from synchronizer.FolderHandler import FolderHandler


class FolderSynchronization:
    def __init__(self, source: str, replica: str, interval: int = 5):
        self.source: Path = Path(source)
        self.replica: Path = Path(replica)
        self.interval = interval
        self.modified_files: Dict[Path, float] = {}
        self.handler = FolderHandler(self.source, self.replica)
        self.last_replica_checksum = {}
        self.last_source_checksum = {}

    def run(self):
        logging.info(f"Synchronizing files from {self.source} to {self.replica} every {self.interval} seconds.")
        while True:
            try:
                self._synchronize()
            except Exception as e:
                logging.error(f"An error occurred during synchronization: {e}")
            time.sleep(self.interval)

    def _synchronize(self):
        if self.source_checksum_changed():  # Check if the source folder has changed (ONE WAY SYNC!)
            logging.info("Syncing files...")
            self.handler.update()
            self.handler.delete_files_folders_replica()
        else:
            logging.info("No action needed.")

    def get_folder_checksum(self, folder_path: Path) -> Dict[Path, str]:
        checksums = {}
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = Path(root, file)
                try:
                    checksums[file_path] = self.calculate_checksum(file_path)
                except Exception as e:
                    logging.error(f"An error occurred while accessing {file_path}! - {e}")
            for directory in dirs:
                directory_path = Path(root, directory)
                try:
                    checksums[directory_path] = self.calculate_folder_checksum(directory_path)
                except Exception as e:
                    logging.error(f"An error occurred while accessing {directory_path}! - {e}")
        return checksums

    def calculate_folder_checksum(self, folder_path: Path) -> str:
        """Compute SHA-256 hash of all files in a folder."""
        h = hashlib.sha256()
        for root, dirs, files in os.walk(folder_path):
            for name in sorted(files):  # Sort to ensure consistent order
                file_path = Path(root, name)
                try:
                    h.update(self.calculate_checksum(file_path).encode())
                except Exception as e:
                    logging.error(f"An error occurred while accessing {file_path}! - {e}")
                    raise
        return h.hexdigest()

    @staticmethod
    def calculate_checksum(file_path: Path, algorithm: str = 'md5') -> str:
        hash_func = hashlib.new(algorithm)
        try:
            with open(file_path, 'rb') as f:
                while chunk := f.read(4096):
                    hash_func.update(chunk)
        except FileNotFoundError as e:
            logging.error(f"File not found: {file_path} - {e}")
            raise
        except PermissionError as e:
            logging.error(f"Permission denied: {file_path} - {e}")
            raise
        except OSError as e:
            logging.error(f"OS error for file {file_path}: {e}")
            raise
        return hash_func.hexdigest()

    def source_checksum_changed(self):
        current_checksum = self.get_folder_checksum(self.source)
        if current_checksum != self.last_source_checksum:
            self.last_source_checksum = current_checksum
            return True
        return False
