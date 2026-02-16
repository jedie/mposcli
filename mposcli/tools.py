import shutil
import sys
from pathlib import Path

from cli_base.cli_tools.subprocess_utils import verbose_check_call


def get_bin(name: str) -> Path:
    bin_path = shutil.which(name)
    if bin_path is None:
        print(f'[red]Error: {name} is not installed or not found in PATH.[/red]')
        print('Hint: Install via pipx, e.g.:')
        print(f'\tpipx install {name}')
        sys.exit(1)
    return Path(bin_path)


def get_esptool_bin() -> Path:
    esptool_bin = get_bin('esptool')
    verbose_check_call(esptool_bin, 'version')
    return esptool_bin


def get_mpremote_bin():
    mpremote_bin = get_bin('mpremote')
    verbose_check_call(mpremote_bin, '--version')
    return mpremote_bin
