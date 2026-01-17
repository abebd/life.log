from enum import Enum, auto


class StorageType(Enum):
    DATABASE = auto()
    FILE = auto()


def resolve_type_from_string(type):
    match type:
        case "database":
            return StorageType.DATABASE

        case "file":
            return StorageType.FILE
