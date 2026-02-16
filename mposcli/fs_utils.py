import os
from pathlib import Path


def list_executables(directory: Path) -> list[Path]:
    return [f for f in directory.iterdir() if f.is_file() and os.access(f, os.X_OK)]
