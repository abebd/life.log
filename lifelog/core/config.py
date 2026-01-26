import tomllib
import logging
import os

from pathlib import Path
from importlib import resources
from platformdirs import user_config_dir

from lifelog.core.constants import DEFAULT_CONFIG_NAME, CONFIG_TEMPLATE_NAME

logger = logging.getLogger(__name__)

IS_DEBUG = os.getenv("DEBUG") == "1"


class Config:
    def __init__(self, user_provided_path: str):
        default_path = Path(user_config_dir("lifelog")) / DEFAULT_CONFIG_NAME

        self.config_file = self._resolve_config_path(user_provided_path, default_path)

        logger.debug(f"Using config file: {str(self.config_file)}")
        self.data = self._load_config()
        self.settings = self.data["settings"]
        self.paths = self.data["paths"]
        self.storage = self.data["storage"]

    def _resolve_config_path(self, user_provided_path: str, default_path: Path):
        if user_provided_path:
            user_path = Path(user_provided_path)
            if user_path.exists():
                return user_path
            else:
                logger.error(
                    f"Explicitly provided config file not found: {user_provided_path}"
                )
                raise FileNotFoundError(
                    f"Could not find config file {user_provided_path}"
                )

        if not default_path.exists():
            logger.debug(f"Could not find default config file, creating it")
            self._create_default_config(default_path)

        return default_path

    def _load_config(self):
        self.config_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_file, "rb") as f:
            return tomllib.load(f)

    def _create_default_config(self, default_path):
        template = resources.files("lifelog.assets").joinpath(CONFIG_TEMPLATE_NAME)

        default_path.parent.mkdir(parents=True, exist_ok=True)
        default_path.write_bytes(template.read_bytes())

        logger.debug(f"Created default config at {default_path}")
