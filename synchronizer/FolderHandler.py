from pathlib import Path
import logging
import shutil
import os
import hashlib


class FolderHandler:

    def __init__(self, source: Path, replica: Path):
        self.source = source
        self.replica = replica

    def update(self):
        for root, dirs, files in os.walk(self.source):

            for filename in files:
                try:
                    replica_file_version = self.replica / Path(root).relative_to(self.source) / filename
                    source_file_version = Path(root, filename)
                    if not replica_file_version.exists():
                        # file not exists in replica
                        shutil.copy2(str(source_file_version), str(replica_file_version))
                        logging.info(f"Created file {replica_file_version}")
                    elif replica_file_version.exists() and self.calculate_checksum(
                            replica_file_version) != self.calculate_checksum(source_file_version):
                        # file exists but has changed
                        shutil.copy2(str(source_file_version), str(replica_file_version))
                        logging.info(f"Copying file {source_file_version} to {replica_file_version}")
                    else:
                        pass
                except Exception as e:
                    logging.error(f"An error occurred while updating file {Path(root, filename)}: {e}")

            for directory in dirs:
                try:
                    replica_folder_version = self.replica / Path(root).relative_to(self.source) / directory
                    if not replica_folder_version.exists():
                        replica_folder_version.mkdir()
                        logging.info(f"Created folder {replica_folder_version}")
                except Exception as e:
                    logging.error(f"An error occurred while updating folder {Path(root, directory)}: {e}")

    def delete_files_folders_replica(self):
        """Delete the file in the replica folder."""
        for root, dirs, files in os.walk(self.replica):
            for filename in files:
                try:
                    file_source = self.source / Path(root).relative_to(self.replica) / filename
                    if not file_source.exists():
                        os.remove(Path(root, filename))
                        logging.info(f"Deleted file {Path(root, filename)}")
                except Exception as e:
                    logging.error(f"An error occurred while deleting {Path(root, filename)}: {e}")

            for directory in dirs:
                try:
                    directory_source = self.source / Path(root).relative_to(self.replica) / directory
                    if not directory_source.exists():
                        shutil.rmtree(Path(root, directory))
                        logging.info(f"Deleted folder {Path(root, directory)}")
                except Exception as e:
                    logging.error(f"An error occurred while deleting {Path(root, directory)}: {e}")

    @staticmethod
    def calculate_checksum(file_path: Path, algorithm='md5') -> str:
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
