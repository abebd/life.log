import logging
import textwrap
import sys

from datetime import datetime
from pathlib import Path

from mypy_diary.core.config import Config
from mypy_diary.types import StorageType, resolve_type_from_string 

logger = logging.getLogger(__name__)

class MessageHandler:
    #TODO remove me
    def __init__(self):
        pass


class EntryHandler:
    
    def __init__(self, config):

        self.config = config
        self.type = resolve_type_from_string(
            type = self.config.settings["storage_mode"]    
        )

        if self.type == StorageType.FILE:

            self.diary_dir_path= Path(
                self.config.paths["diary_folder"]
            ).expanduser()

        if self.type == StorageType.DATABASE:
            pass

        self.entry_timestamp = datetime.now()
        self.entries = self._get_entries() #TODO might become slow in future


    def list_entries(self):

        for entry in self.entries:
            print(entry["name"])


    def read_entry(self, entry_name):
    
        entry_found = False

        if self.type == StorageType.FILE:
            
            extension = f".{self.config.settings['extension']}" 

            # If extension was not sent from user
            # Might need an --override-extension parameter
            if not entry_name[-len(extension):] == extension:
                
                entry_name = f"{entry_name}{extension}"
                logger.debug(f"Appended {extension} to {entry_name} ({entry_name}{extension})")

            for entry in self.entries:
                if entry_name == entry["name"] \
                or f"{entry_name}.entry" == entry["name"]:

                    entry_found = True

                    try:

                        with open(self.diary_dir_path / entry_name, "r", encoding="utf-8") as f:
                            
                            for line in f:

                                sys.stdout.write(line)

                            sys.stdout.flush()

                    except OSError as e:

                        print(f"Could not read file: {e}", file=sys.stderr)
                        

        if self.type == StorageType.DATABASE:
            #TODO
            pass


        if not entry_found:
            print(f"Could not find file {entry_name}")


    def add_entry(self, message, title=''):

        if self.type == StorageType.FILE:

            #self._setup_file_storage()
            file_path = self._get_file_path()

            logger.debug(
                "Using file " + 
                str(file_path)
            )

            file_path.parent.mkdir(parents=True, exist_ok=True)

            file_path.touch(exist_ok=True)

            try:
                with open(file_path, "a") as f:

                    # Write Header
                    f.write(self.entry_timestamp.strftime("@%H:%M:%S"))

                    # Write title if it was sent
                    if not title == '':

                        f.write(f"\n{title}\n\n")

                    # Write message
                    message = textwrap.fill(message, width=69)
                    f.write(f"\n\n{message}\n\n\n")

            except OSError as e:
                logger.error(
                    "Unable to write to file: " + 
                    str(self.diary_dir_path)
                )

        if self.type == StorageType.DATABASE:
            #TODO
            pass


    def _setup_file_storage(self):

        if not self.diary_dir_path.exists():

            logger.debug(str(
                self.diary_dir_path) + " does not exist, creating it"
            )
            self.diary_dir_path.mkdir(parents=True)


    def _get_file_path(self):

        file_name = self.entry_timestamp.strftime("%Y-%m-%d.entry")
        return self.diary_dir_path / file_name


    def _get_entries(self) -> list:
 
        match self.type:
            
            case StorageType.FILE:
                return self._get_entries_from_file()

            case StorageType.DATABASE:
                return self._get_entries_from_database()
                
            case _:
                return []


    def _get_entries_from_file(self) -> list:
        
        diary_folder = Path(
            self.config.paths["diary_folder"]
        ).expanduser()

        sorted_files = sorted(
            diary_folder.glob("*.entry")
        )

        return [
            {
                "name": f.name, 
                "path": str(f.absolute())
            }
            for f in sorted_files
        ]
        

    def _get_entries_from_database(self) -> list:
        
        return [] # TODO


