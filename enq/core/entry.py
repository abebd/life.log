import logging
import textwrap
import sys
import tempfile
import json

from datetime import datetime
from pathlib import Path

from enq.core.types import StorageType, resolve_type_from_string
from enq.cli.editor import Editor
from enq.cli.interface import ui, State

logger = logging.getLogger(__name__)

def extract_title_from_content(content: str) -> tuple[str, str]:
    title = ""
    remaining_lines = []
    found_content = False

    if not content.strip():
        return title, ""

    for line in content.splitlines():
        is_whitespace = not line.strip()

        if not found_content:
            if is_whitespace:
                continue

        found_content = True
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            continue

        remaining_lines.append(line)

    return title, "\n".join(remaining_lines).strip()


class EntryHandler:
    def __init__(self, config):
        self.config = config
        self.type = resolve_type_from_string(type=self.config.settings["storage_mode"])

        if self.type == StorageType.FILE:
            self.diary_dir_path = Path(self.config.paths["diary_folder"]).expanduser()

        if self.type == StorageType.DATABASE:
            pass

        self.entry_timestamp = datetime.now()
        self._entries = None

    @property
    def entries(self):
        # TODO lazy fix, everytime entries is used we fetch from the folder
        #      maybe performance issue
        self._entries = self._get_entries()
        return self._entries

    def list_entries(self):
        for entry in self.entries:
            #print(entry["name"])
            ui.print(entry["name"])
    
    def add_entry(self, message, title):
        if self.type == StorageType.FILE:
            file_path = self._get_entry_file_path()
            logger.debug("Using file " + str(file_path))
            self._prepare_storage(file_path)

            try:
                with open(file_path, "a") as f:
                    # Write Header
                    f.write(self._get_header_time_str())

                    # Write title if it was sent
                    if not title == "":
                        f.write(f"\n\n### {title}\n\n")

                    # Write message
                    # TODO replace textwrap as it doesnt deal with
                    #      linebreaks in the text well
                    message = textwrap.fill(message, width=69, replace_whitespace=False, break_long_words=False)
                    f.write(f"{message}\n\n\n")

                logger.debug("Wrote entry to file")

            except OSError:
                logger.error("Unable to write to file: " + str(self.diary_dir_path))

        if self.type == StorageType.DATABASE:
            # TODO
            pass

    def get_entry_from_editor(self):
        editor = Editor(self.config.settings["editor"])

        if self.type == StorageType.FILE:
            with tempfile.NamedTemporaryFile(
                mode="w+", suffix=".md", delete=False
            ) as tf:
                temp_path = Path(tf.name)

                tf.write("# Put title here, or remove me...\n\n")

            try:
                editor.open(temp_path)

                content = temp_path.read_text(encoding="utf-8")

                title, message = extract_title_from_content(content)

                logger.debug(f"User wrote: {json.dumps({"title": title, "message": message})}")

                if message != "":
                    self.add_entry(title=title, message=message)

            finally:
                if temp_path.exists():
                    temp_path.unlink()


    def open_entry_in_editor(self, entry_name):
        editor = Editor(self.config.settings["editor"])

        if entry_name == "today":
            entry_name = self.entry_timestamp.strftime(f"%Y-%m-%d.{self.config.settings["extension"]}")

        file_path = self.diary_dir_path / entry_name

        if self.type == StorageType.FILE:
            editor.open(file_path)

    def _prepare_storage(self, file_path):
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if not file_path.exists():
            file_path.touch()

            with open(file_path, "a") as f:
                f.write(f"# {file_path.stem}\n\n")

        logger.debug(str(self.diary_dir_path) + " does not exist, creating it")

    def _get_entry_file_path(self):
        file_name = self.entry_timestamp.strftime(
            f"%Y-%m-%d.{self.config.settings['extension']}"
        )
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
        diary_folder = Path(self.config.paths["diary_folder"]).expanduser()

        logger.debug(f"Looking for entries in {str(diary_folder)}")

        sorted_files = sorted(
            diary_folder.glob(f"*.{self.config.settings['extension']}")
        )

        return [{"name": f.name, "path": str(f.absolute())} for f in sorted_files]

    def _get_entries_from_database(self) -> list:
        return []  # TODO

    def _get_header_time_str(self):
        return self.entry_timestamp.strftime("## %H:%M:%S")

"""
No longer used. Most of this code has already been refactored.

    def read_entry(self, entry_name: str) -> bool:
        entry_found = False
        extension = f"{self.config.settings['extension']}"

        if entry_name == "today":
            entry_name = self.entry_timestamp.strftime(f"%Y-%m-%d.{extension}")

        if self.type == StorageType.FILE:
            # If extension was not sent from user
            # Might need an --override-extension parameter
            if not entry_name[-len(extension) :] == extension:
                entry_name = f"{entry_name}.{extension}"
                logger.debug(
                    f"Appended {extension} to {entry_name} ({entry_name}.{extension})"
                )

            logger.debug(f"Found {str(len(self.entries))} file((s)")

            for entry in self.entries:
                logger.debug(f"On entry: {entry}")
                if (
                    entry_name == entry["name"]
                    or f"{entry_name}.{extension}" == entry["name"]
                ):
                    entry_found = True

                    self._read_entry_from_file(entry_name)

        if self.type == StorageType.DATABASE:
            # TODO
            pass

        if not entry_found:
            print(f"Could not find entry {entry_name}")

    def _read_entry_from_file(self, entry_name: str) -> bool:
        #TODO should take an Entry object instead of an entry name
        #     then we have some function to resolve an entry name
        file_path = self.diary_dir_path / entry_name

        if not file_path.is_file():
            alt_path = file_path.with_suffix(self.config.settings["extension"])
            if not alt_path.is_file():
                return False

            file_path = alt_path

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    ui.print(line.rstrip())

                return True

        except OSError as e:
            #TODO: make logger always log errors
            raise OSError(
                f"Could not read from file: {e}", file=sys.stderr
            )



"""


class Entry:
    def __init__(self):
        # TODO
        pass

