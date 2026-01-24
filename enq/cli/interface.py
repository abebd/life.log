import logging

from enum import Enum, auto

logger = logging.getLogger(__file__)

class State(Enum): 
    CLI = auto()
    MENU = auto()
    IN_EDITOR = auto()

class Interface:
    def __init__(self):
        self._last_state = None
        self._state = State.CLI
        self._buffer = []
        
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: State):
        logger.debug(f"Setting state to: {value}")
        self._last_state = self._state
        self._state = value 

    @property
    def buffer(self):
        return self._buffer

    def reset_state(self):
        if not self._last_state:
            raise Exception("Can't reset state if its last state was None")

        logger.debug(f"Setting state to: {self._last_state}")
        self._state = self._last_state

    def print(self, *args):
        message = " ".join(map(str, args))

        match self.state:
            case State.MENU:
                self._buffer.append(message)

            case State.CLI:
                logger.debug(f"Printing message: '{message}'") #TODO: maybe unecessary idk
                print(message)

            case _:
                raise ValueError(f"State {self.state} does not have a valid way of dealing with user messages.")

    def flush_buffer(self):
        content = "\n".join(self._buffer)
        self._buffer = []
        return content

ui = Interface()
