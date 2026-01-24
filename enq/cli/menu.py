import questionary
import logging

from simple_term_menu import TerminalMenu
from enq.utils.cli import send_cls
from enq.cli.interface import ui, State

class MenuHandler():

    def __init__(self, app, config):
        self.app = app

        self.menu_options = [
            ("n", "Create a new entry", self.app.entry_handler.get_entry_from_editor),
            ("r", "Read an entry", self.select_and_open_entry),
            (("q", "exit"), "Quit.", self._exit)
        ]

    def _send_header(self):
        send_cls()
        
        for keys, label, _ in self.menu_options:
            display_key = keys[0] if isinstance(keys, tuple) else keys
            print(f"[{display_key}] {label}")

    def run(self):
        ui.state = State.MENU
        while True:
            self._send_header()

            logging.debug(f"Current buffer: {ui.buffer}")

            choice = input("\nEnter option: ").strip().lower()

            found = False
            for keys, _, func in self.menu_options:
                if choice == keys or (isinstance(keys, tuple) and choice in keys):
                    func()
                    found = True
                    break


            if not found:
                self._send_header()
                input("\nInvalid option. Enter a valid option. ")
        

    def _exit(self):
        exit(0)

    def select_and_open_entry(self):
        # Keys currently is just the filename, and this is fine as a 
        # key if we're just fetching entries from one folder.
        # If we start fetching entries from multiple folders,
        # we might need to provide the full path instead.
        
        entry_name =  run_interm_browser(
            items=[item["name"] for item in self.app.entry_handler.entries], 
            title="Select entry to view: ",
        )

        logging.debug(f"Chose entry: {entry_name}")
        self.app.entry_handler.open_entry_in_editor(entry_name)
    

def run_interm_browser(items: tuple, title: str, ignore_help: bool = False): 

    if not ignore_help:
        title += "\n(Press / and start typing to filter the list)"
    
    terminal_menu = TerminalMenu(
        [item for item in items],
        title=title,
        menu_cursor="> ",
        menu_cursor_style=("fg_cyan", "bold"),
    )

    selected_index = terminal_menu.show()

    if selected_index is not None:
        selected_object = items[selected_index]

        return selected_object

