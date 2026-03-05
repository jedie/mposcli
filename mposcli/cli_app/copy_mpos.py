import logging
import time
from pathlib import Path
from typing import Annotated

import tyro
from bx_py_utils.path import assert_is_dir
from cli_base.cli_tools.subprocess_utils import verbose_check_call
from cli_base.cli_tools.verbosity import setup_logging
from cli_base.tyro_commands import TyroVerbosityArgType
from rich import print

from mposcli.cli_app import app
from mposcli.mpos_utils import get_mpos_path
from mposcli.tools import get_mpremote_bin
from mposcli.user_input import choose_newest_modified_directory, get_newest_files
from mposcli.utilities.mpremote import MpOsPathResolver, start_mpremote_repl


logger = logging.getLogger(__name__)


@app.command
def cp(
    local_path: Annotated[
        Path | None,
        tyro.conf.arg(help='Optional file or directory path.'),
    ] = None,
    /,
    new_file_limit: Annotated[
        int,
        tyro.conf.arg(help='How many of the newest files to show in the file chooser?'),
    ] = 10,
    reset: Annotated[
        bool,
        tyro.conf.arg(help='Reset the device after copy/update?'),
    ] = True,
    repl: Annotated[
        bool,
        tyro.conf.arg(help='After flashing/verify start REPL with mpremote to see the output of the device?'),
    ] = True,
    verbosity: TyroVerbosityArgType = 1,
):
    """
    Copy/update internal_filesystem/lib/mpos files to the device via "mpremote fs cp".
    Display a file chooser to select which files to copy/update.
    But can also be used to copy/update all files.
    see: https://docs.micropythonos.com/architecture/filesystem/
    """
    setup_logging(verbosity=verbosity)

    mpos_path = get_mpos_path()
    resolver = MpOsPathResolver(mpos=mpos_path)

    mpremote_bin = get_mpremote_bin()

    print('\n')

    if not local_path:
        # Let's the user select from the list of the newest modified files in internal_filesystem/lib/mpos:
        local_path = get_newest_files(resolver.lib_mpos, limit=new_file_limit)
        if not local_path:
            print('Copy/update all files in lib/mpos to the device')
            local_path = resolver.lib_mpos

    print(f'Copy/update app: "{local_path}" ...')

    if not local_path.exists():
        print(f'[red]Error: The specified source path "{local_path}" does not exist.[/red]')
        return

    local_path_str, remote_str = resolver.resolve(local_path)

    popenargs = (mpremote_bin, 'fs')

    if local_path.is_dir():
        popenargs += ('-r',)
        print(f'Copying directory "[bold]{local_path_str}[/bold]" to device at "[bold]{remote_str}[/bold]" ...')
    else:
        print(f'Copying file "[bold]{local_path_str}[/bold]" to device at "[bold]{remote_str}[/bold]" ...')

    verbose_check_call(
        *popenargs,
        'cp',
        local_path_str,
        remote_str,
        verbose=True,
        cwd=mpos_path,
        text=None,
    )

    if reset:
        time.sleep(1)
        verbose_check_call(
            mpremote_bin,
            'reset',
            verbose=True,
            cwd=mpos_path,
            text=None,
        )

    if repl:
        start_mpremote_repl()


@app.command
def cp_app(
    reset: Annotated[
        bool,
        tyro.conf.arg(help='Reset the device after copy/update?'),
    ] = True,
    repl: Annotated[
        bool,
        tyro.conf.arg(help='After flashing/verify start REPL with mpremote to see the output of the device?'),
    ] = True,
    verbosity: TyroVerbosityArgType = 1,
):
    """
    Copy/update internal_filesystem/apps to the device via "mpremote fs cp".
    Display a file chooser to select which app to copy/update.
    But can also be used to copy/update all files.
    see: https://docs.micropythonos.com/os-development/installing-on-esp32/
    """
    setup_logging(verbosity=verbosity)

    mpos_path = get_mpos_path()

    internal_fs = mpos_path / 'internal_filesystem'
    apps_path = internal_fs / 'apps'
    assert_is_dir(apps_path)

    mpremote_bin = get_mpremote_bin()
    popenargs = (mpremote_bin, 'fs', 'cp', '-r')

    app = choose_newest_modified_directory(apps_path)

    print('\n')

    if not app:
        print('Copy/update all apps in "internal_filesystem/apps" to the device')
        local_path = 'internal_filesystem/apps'
        remote_path = ':/apps'
    else:
        print(f'Copy/update {app=} ...')
        local_path = f'internal_filesystem/apps/{app.name}'
        remote_path = f':/apps/{app.name}'

    popenargs += (local_path, remote_path)
    verbose_check_call(
        *popenargs,
        verbose=True,
        cwd=mpos_path,
        text=None,
    )

    if reset:
        time.sleep(1)
        verbose_check_call(
            mpremote_bin,
            'reset',
            verbose=True,
            cwd=mpos_path,
            text=None,
        )

    if repl:
        time.sleep(1)
        verbose_check_call(
            mpremote_bin,
            'repl',
            verbose=True,
            cwd=mpos_path,
            timeout=None,
            text=None,
        )
