import logging

from mypy_diary.core.handler import MessageHandler, EntryHandler
from mypy_diary.cli.args import parse_args
from mypy_diary.core.logger import setup_logging
from mypy_diary.core.config import Config

logger = logging.getLogger(__name__)

def main():

    args = parse_args()

    setup_logging(args.verbose)

    config = Config()

    #TODO add part to override config values with parameters
    # e.g. override storagetype

    entry_handler = EntryHandler(config)

    if args.list_entries:
        entry_handler.list_entries()

    if args.message:
        #message_handler = MessageHandler(config)
        #message_handler(content=args.message)
        entry_handler.add_entry(args.message)
        
    if args.read_entry:
        entry_handler.read_entry(args.read_entry)
