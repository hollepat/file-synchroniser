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
            self._synchronize()
            time.sleep(self.interval)

    def _synchronize(self):
        if self.source_checksum_changed() or self.replica_checksum_changed():  # Check if the source folder has changed (ONE WAY SYNC!)
            logging.info("Syncing files...")
            updated_files = self._get_updated_files(self.source)
            self.handler.update(updated_files)
            self.handler.delete_files_folders_replica()
        else:
            logging.info("No action needed.")

    def _get_updated_files(self, source: Path):
        files_to_copy = []

        for root, dirs, files in os.walk(source):

            for filename in files:
                if self.has_modification_time_changed(Path(root, filename)):
                    files_to_copy.append(Path(root, filename))

            for directory in dirs:
                if self.has_modification_time_changed(Path(root, directory)):
                    files_to_copy.append(Path(root, directory))
        return files_to_copy

    def has_modification_time_changed(self, item: Path):
        try:
            time = os.path.getmtime(item)
            if item in self.modified_files:
                if time > self.modified_files[item]:
                    self.modified_files[item] = time
                    return True
                else:
                    return False
            else:
                self.modified_files[item] = time
                return True
        except Exception as e:
            logging.error(f"Error occurred while checking modification time for {item}: {e}")
            return False

    def get_folder_checksum(self, folder_path: Path) -> Dict[Path, str]:
        checksums = {}
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = Path(root, file)
                checksums[file_path] = self.calculate_checksum(file_path)
        return checksums

    @staticmethod
    def calculate_checksum(file_path, algorithm='md5'):
        hash_func = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    def source_checksum_changed(self):
        current_checksum = self.get_folder_checksum(self.source)
        if current_checksum != self.last_source_checksum:
            self.last_source_checksum = current_checksum
            return True
        return False

    def replica_checksum_changed(self):
        current_checksum = self.get_folder_checksum(self.replica)
        if current_checksum != self.last_replica_checksum:
            self.last_replica_checksum = current_checksum
            return True
        return False
