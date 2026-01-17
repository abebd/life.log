import argparse
import sys

from dataclasses import dataclass
from importlib.metadata import version as get_version

@dataclass(frozen=True)
class CliArgs:

    verbose: bool
    message: str
    title: str
    list_entries: bool
    read_entry: str


def parse_args() -> CliArgs:

    parser = argparse.ArgumentParser(
        description="Diary app"
    )

    parser.add_argument(
        "-m", "--message",
        type=str,
        metavar="TEXT",
        help="Write the context of your diary entry as a string."
    )

    parser.add_argument(
        "-t", "--title",
        type=str,
        metavar="TEXT",
        help="Title of the diary entry."
    )

    parser.add_argument(
        "--list-entries",
        action="store_true",
        help="List entries"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output."
    )

    __version__ = get_version("mypy-diary")

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    parser.add_argument(
        "-s", "--read-entry",
        type=str,
        metavar="TEXT",
        help="Write the content of an entry to stdio."
    )

    args = parser.parse_args()

    # Verify args
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if args.title and not args.message:
        parser.error("--title requires --message")


    return CliArgs(**vars(parser.parse_args()))

