import logging
import sys
from pathlib import Path

from rich import print


logger = logging.getLogger(__name__)


def get_mpos_path() -> Path:
    """
    Get the path to the MicroPythonOS project root directory.
    Assume that mposcli is only called from the root directory of a MicroPythonOS project.
    """
    current_path = Path().cwd().resolve()
    logger.info('Current working directory: %s', current_path)

    for dir_name in ('internal_filesystem', Path('lvgl_micropython', 'build')):
        dir_path = current_path / dir_name
        logger.debug('Checking for directory: %s', dir_path)
        if not dir_path.is_dir():
            print(f"Error: Directory '{dir_name}' not found in {current_path}.")
            print('Hint: Call "mposcli" only in the root directory of a MicroPythonOS project!')
            sys.exit(1)

    return current_path

