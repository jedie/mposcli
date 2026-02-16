import json
import logging
import os
import sys
from pathlib import Path
from typing import Annotated

import tyro
from bx_py_utils.path import assert_is_file
from cli_base.cli_tools.subprocess_utils import verbose_check_call
from cli_base.cli_tools.verbosity import setup_logging
from cli_base.tyro_commands import TyroVerbosityArgType
from rich import print  # noqa

from mposcli.cli_app import app
from mposcli.fs_utils import list_executables
from mposcli.mpos_utils import get_mpos_path
from mposcli.user_input import file_chooser


logger = logging.getLogger(__name__)


@app.command
def run_desktop(
    heapsize: Annotated[
        int,
        tyro.conf.arg(
            help='Heap size in MB (default: 8, same as PSRAM on many ESP32-S3 boards)',
        ),
    ] = 8,
    script: Annotated[
        str | None,
        tyro.conf.arg(help='Script file (.py) or app name to run. If omitted, starts normally.'),
    ] = None,
    binary: Annotated[
        str | None,
        tyro.conf.arg(
            help='Optional name of the binary to start.'
            ' If omitted, shows a file chooser to select one from the lvgl_micropython build directory.'
        ),
    ] = None,
    verbosity: TyroVerbosityArgType = 1,
):
    """
    Run MicroPythonOS on desktop.
    see: https://docs.micropythonos.com/getting-started/running/#running-on-desktop
    """
    setup_logging(verbosity=verbosity)

    mpos_path = get_mpos_path()

    internal_fs = mpos_path / 'internal_filesystem'
    lvgl_micropython_build_path = mpos_path / 'lvgl_micropython' / 'build'

    executables = list_executables(lvgl_micropython_build_path)
    if not executables:
        print(f'Error: No executable found in {lvgl_micropython_build_path}.')
        print('Hint: Download or build the lvgl_micropython binary first.')
        print('Hint 2: Forgotten to make the binary executable? e.g.: chmod +x <binary>')
        sys.exit(1)

    if binary:
        binary = lvgl_micropython_build_path / binary
    else:
        binary = file_chooser(executables)
    assert_is_file(binary)

    os.environ['HEAPSIZE'] = f'{heapsize}M'

    # Change to internal_filesystem dir
    os.chdir(internal_fs)

    popenargs = [binary]

    if script and script.endswith('.py') and Path(script).is_file():
        # Run script file directly
        script_path = str(Path(script).resolve())
        popenargs += ('-v', '-i', script_path)
    else:
        if script:
            # Treat as app name
            config_file = Path('data/com.micropythonos.settings/config.json')
            config_file.parent.mkdir(parents=True, exist_ok=True)
            if config_file.exists():
                with config_file.open('r', encoding='utf-8') as f:
                    try:
                        config = json.load(f)
                    except Exception:
                        config = {}
            else:
                config = {}
            config['auto_start_app'] = script
            with config_file.open('w', encoding='utf-8') as f:
                json.dump(config, f)
        popenargs += ('-X', f'heapsize={os.environ["HEAPSIZE"]}', '-v', '-i', '-c', Path('main.py').read_text())

    verbose_check_call(
        *popenargs,
        env=os.environ,
        verbose=True,
        cwd=internal_fs,
        timeout=None,
        text=None,
    )
