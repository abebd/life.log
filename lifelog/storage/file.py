from lifelog.storage.base import Storage


class FileStorage(Storage):
    def __init__(self, config):
        pass

    @property
    def type(self):
        return "file"

    def add_entry(self, body, timestamp):
        pass

    def update_entry(self, old_entry, new_entry):
        pass

    def open_entry(self, body, timestamp):
        pass

    def get_entries(self) -> list:
        pass
