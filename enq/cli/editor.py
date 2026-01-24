import shutil
import subprocess

from pathlib import Path

from enq.cli.interface import ui, State


class Editor:
    def __init__(self, editor_name):
        self.editor = editor_name
        self._verify_editor()

    def _verify_editor(self):
        if shutil.which(self.editor) is None:
            raise FileNotFoundError(f"Editor '{self.editor}' not found in your system.")

    def open(self, file_path: Path):
        try:
            ui.state = State.IN_EDITOR
            subprocess.run([self.editor, str(file_path)], check=True)
            ui.reset_state()
        except subprocess.CalledProcessError as e:
            wrint(f"Editor exited with an error: {e}")
