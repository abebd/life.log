import argparse
import os

from dataclasses import dataclass
from importlib.metadata import version as get_version

@dataclass(frozen=True)
class CliArgs:
    verbose: bool
    message: str
    title: str
    list_entries: bool
    read_entry: str
    new: bool
    config_file: str
    no_menu: bool


def parse_args() -> CliArgs:
    parser = argparse.ArgumentParser(description="Diary app")

    parser.add_argument(
        "-m",
        "--message",
        type=str,
        metavar="TEXT",
        help="Write the context of your diary entry as a string.",
    )

    parser.add_argument(
        "-t",
        "--title",
        type=str,
        metavar="TEXT",
        help="Title of the diary entry.",
        nargs="?",
        default="",
    )

    parser.add_argument("--list-entries", action="store_true", help="List entries")

    IS_DEBUG = os.getenv("DEBUG") == "1"
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output.",
        default=IS_DEBUG,
    )

    __version__ = get_version("enq")

    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    parser.add_argument(
        "-r",
        "--read-entry",
        type=str,
        nargs="?",
        const="today",
        metavar="TEXT",
        help="Write the content of an entry to stdio. Default value is today.",
    )

    parser.add_argument(
        "--config-file", type=str, metavar="TEXT", help="Specify config file to use."
    )

    parser.add_argument(
        "-n", "--new", action="store_true", help="Open an editor and write an entry."
    )

    parser.add_argument(
        "--no-menu", action="store_true", help="Don't launch the menu. Go full CLI mode."
    )

    args = parser.parse_args()

    # Print out args if none were provided
    # NOTE: no longer used since we have the MenuHandler
    #if len(sys.argv) == 1:
    #    parser.print_help()
    #    sys.exit(1)

    if args.title and not args.message:
        parser.error("--title requires --message")

    return CliArgs(**vars(parser.parse_args()))
