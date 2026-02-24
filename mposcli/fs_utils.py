import logging
import os
from pathlib import Path


logger = logging.getLogger(__name__)


def list_executables(directory: Path) -> list[Path]:
    executables = []
    for entry in directory.iterdir():
        if entry.is_file():
            if os.access(entry, os.X_OK):
                executables.append(entry)
            else:
                logger.info('Skipping non-executable file: %s', entry)
    return executables
