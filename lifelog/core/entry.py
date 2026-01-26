import logging
import tempfile
import json

from datetime import datetime
from pathlib import Path

from lifelog.cli.editor import Editor
from lifelog.cli.menu import prompt_selection

logger = logging.getLogger(__name__)

class EntryHandler:
    def __init__(self, config, storage):
        self.config = config
        self.storage = storage
        # self.entries = entries

    @property
    def entries(self):
        pass

    def create_entry_from_string(self, body):
        entry = Entry(
            timestamp=datetime.now(),
            body=body,
            storage_type=self.storage.type,
        )

        logger.debug(
            f"Created entry: {json.dumps({'body': entry.body, 'timestamp': str(entry.timestamp)})}"
        )

        self.storage.add_entry(entry)

    def create_entry_from_editor(self):
        editor = Editor(self.config.settings["editor"])

        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=self.config.storage["file_extension"], delete=False
        ) as tf:
            temp_path = Path(tf.name)

        try:
            editor.open(temp_path)

            entry = Entry(
                timestamp=datetime.now(),
                body=temp_path.read_text(encoding="utf-8"),
                storage_type=self.storage.type,
            )

            logger.debug(
                f"User wrote: {json.dumps({'body': entry.body, 'timestamp': str(entry.timestamp)})}"
            )

            if entry.body != "":
                self.storage.add_entry(entry)

        finally:
            if temp_path.exists():
                temp_path.unlink()

    def open_entry_in_editor(self, entry):
        editor = Editor(self.config.settings["editor"])

        if entry is None:
            logger.warning("Failed to find entry to open in editor")

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tf:
            temp_path = Path(tf.name)

            tf.write(entry.body)

        try:
            editor.open(temp_path)

            new_entry = Entry(
                timestamp=datetime.now(),
                body=temp_path.read_text(encoding="utf-8"),
                storage_type=self.storage.type,
            )

            if new_entry != entry:
                logger.debug(
                    f"User updated entry: {json.dumps({'body': new_entry.body, 'timestamp': str(new_entry.timestamp)})}"
                )

                self.storage.update_entry(entry, new_entry)

        finally:
            if temp_path.exists():
                temp_path.unlink()

    def select_and_open_entry(self):
        # Keys currently is just the filename, and this is fine as a
        # key if we're just fetching entries from one folder.
        # If we start fetching entries from multiple folders,
        # we might need to provide the full path instead.

        entries = self.storage.get_entries()

        selected_entry = prompt_selection(
            entries,
            title="Select entry to view: ",
        )

        logging.debug(f"Chose entry: {selected_entry}")

        self.open_entry_in_editor(selected_entry)


class Entry:
    def __init__(self, body, timestamp, storage_type=None, uid=None):
        self.timestamp = timestamp
        self.body = body
        self.storage_type = storage_type
        self.uid = uid

    @property
    def date(self):
        return self.timestamp.date()

    @property
    def time(self):
        return self.timestamp.time()

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = str(value)

    @property
    def storage_type(self):
        return self._storage_type

    @storage_type.setter
    def storage_type(self, value):
        self._storage_type = value.lower()

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        self._uid = value

    def __str__(self):
        return f"{self.timestamp}"  # Add like 10 words or something from body

    def __eq__(self, other):
        if not isinstance(other, Entry):
            return False

        return self.body == other.body
