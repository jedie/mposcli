import shutil
import sys
from pathlib import Path


def get_bin(name: str) -> Path:
    bin_path = shutil.which(name)
    if bin_path is None:
        print(f'[red]Error: {name} is not installed or not found in PATH.[/red]')
        print('Hint: Install via pipx, e.g.:')
        print(f'\tpipx install {name}')
        sys.exit(1)
    return Path(bin_path)


def get_esptool_bin() -> Path:
    return get_bin('esptool')


def get_mpremote_bin():
    return get_bin('mpremote')
