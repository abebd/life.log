import logging

logger = logging.getLogger(__name__)

def setup_logging(verbose: bool):
    log_level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(level=log_level, format="%(levelname)s [%(name)s]: %(message)s")
