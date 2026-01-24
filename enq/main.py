import logging

from importlib.metadata import version as get_version

from enq.core.entry import EntryHandler
from enq.cli.args import parse_args
from enq.core.logger import setup_logging
from enq.core.config import Config
from enq.cli.menu import MenuHandler
from enq.cli.interface import ui

logger = logging.getLogger(__name__)

class App():

    def __init__(self):
        self.args = parse_args()

        setup_logging(self.args.verbose)

        logger.debug(f"-----| Starting run @ enq-{get_version("enq")} |-----")
        logger.debug(f"Current state: {ui.state}")
        logger.debug(f"Args passed from user: {self.args}")
    
        self.config = Config(self.args.config_file)

        self.entry_handler = EntryHandler(self.config)
        self.menu_handler = MenuHandler(self, self.config)

    def run(self):
        ran_something = False

        if self.args.list_entries:
            ran_something = True
            self.entry_handler.list_entries()

        if self.args.message:
            ran_something = True
            self.entry_handler.add_entry(self.args.message, self.args.title)

        if self.args.read_entry:
            ran_something = True
            #self.entry_handler.read_entry(self.args.read_entry)
            self.entry_handler.open_entry_in_editor(self.args.read_entry)

        if self.args.new:
            ran_something = True
            self.entry_handler.get_entry_from_editor()

        # If nothing ran, open the interactive menu
        if not ran_something and not self.args.no_menu:
            self.menu_handler.run()


def main():
    app = App()
    app.run()
