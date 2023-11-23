import os
from time import time
import random
import argparse
from datetime import datetime
from models import Note


class MediaStreamService:

    """A singleton class that manages a media stream service.

    This class provides methods for getting folders, getting files in a folder,
    and tagging resources.
    """

    _instance = None

    folders = []
    contents = {}
    refresh_time = 30
    current_time = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MediaStreamService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.get_args()
        self._get_folders()
        for folder in self.folders:
            self._get_file_list_by_time(folder)
        self.current_time = time()

    def get_args(self):
        # Parse command-line arguments
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument(
            "folder_path", help="Folder path to be mounted as static repo"
        )
        parser.add_argument("--update", help="Update front", type=bool, default=False)
        self.args = parser.parse_args()
        return self.args

    def get_folders(self):
        """Gets a list of all folders in the media stream service.

        Returns:
            A list of all folders in the media stream service.
        """
        if self.elapsed_time > self.refresh_time:
            folders = self.folders
            self.current_time = time()
        else:
            folders = self._get_folders()
        return {"folders": folders}

    def get_files_in_folder(self, folder_id):
        """Gets a list of all files in a folder in the media stream service.

        Args:
            folder_id: The ID of the folder to get files from.

        Returns:
            A list of all files in the specified folder.
        """
        if self.elapsed_time > self.refresh_time:
            contents = self._get_file_list_by_time(
                os.path.join(self.args.folder_path, folder_id),
            )
            self.current_time = time()
        else:
            contents = self.contents[folder_id]
        return {"files": contents}

    @property
    def time_seed(self):
        current_time = datetime.now()
        return current_time.year + current_time.day + current_time.month

    @property
    def elapsed_time(self):
        return time() - self.current_time

    def _get_file_list_by_time(self, folder_id):
        contents = [
            a
            for a in os.listdir(os.path.join(self.args.folder_path, folder_id))
            if os.path.isfile(os.path.join(self.args.folder_path, folder_id, a))
        ]
        random.seed(self.time_seed)
        random.shuffle(contents)
        if folder_id in self.contents:
            self.contents.update({folder_id, contents})
        else:
            self.contents[folder_id] = contents
        return contents

    def _get_folders(self):
        folders = [
            a
            for a in os.listdir(self.args.folder_path)
            if os.path.isdir(os.path.join(self.args.folder_path, a))
        ]
        if not self.folders:
            self.folders = folders
        return folders

    async def tag_resource(self, note):
        """Adds a tag to a resource in the media stream service.

        Args:
            resource_id: The ID of the resource to tag.
            tag_name: The name of the tag to add.
        """
        try:
            with open("tags.txt", "a") as file:
                file.write(f"{note.model_dump_json()}\n")
            return {"succeded": True}
        except Exception as e:
            return {"succeded": False}
