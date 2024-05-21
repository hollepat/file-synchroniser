from pathlib import Path
import logging
from typing import List
import shutil
import os


class FolderHandler:

    def __init__(self, source: Path, replica: Path):
        self.source = source
        self.replica = replica

    def update(self, differences: List[Path]):
        """Update the replica folder based on the differences found."""
        for item in differences:
            if item.is_file():
                self._update_file(item)
            else:
                self._update_folder(item)

    def delete_files_folders_replica(self):
        """Delete the file in the replica folder."""
        for root, dirs, files in os.walk(self.replica):

            for filename in files:
                file_source = self.source / Path(root).relative_to(self.replica) / filename
                if not file_source.exists():
                    os.remove(Path(root, filename))
                    logging.info(f"Deleted file {Path(root, filename)}")

            for directory in dirs:
                directory_source = self.source / Path(root).relative_to(self.replica) / directory
                if not directory_source.exists():
                    shutil.rmtree(Path(root, directory))
                    logging.info(f"Deleted folder {Path(root, directory)}")
    def _update_file(self, file_source: Path):
        """Update the file in the replica folder."""
        file_replica = self.replica / file_source.relative_to(self.source)
        os.makedirs(file_replica.parent, exist_ok=True)
        if not file_replica.exists():
            shutil.copy2(str(file_source), str(file_replica))
            logging.info(f"Created file {file_replica}")
        else:
            shutil.copy2(str(file_source), str(file_replica))
            logging.info(f"Copying file {file_source} to {file_replica}")

    def _update_folder(self, folder_source: Path):
        """Update the folder in the replica folder."""
        folder_replica = self.replica / folder_source.relative_to(self.source)
        if not folder_replica.exists():
            shutil.copytree(str(folder_source), str(folder_replica))
            logging.info(f"Created folder {folder_replica}")
        else:
            shutil.rmtree(str(folder_replica))
            shutil.copytree(str(folder_source), str(folder_replica))
            logging.info(f"Copying folder {folder_source} to {folder_replica}")
