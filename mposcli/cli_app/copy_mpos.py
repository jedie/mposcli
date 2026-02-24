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
    see: https://docs.micropythonos.com/os-development/installing-on-esp32/
    """
    setup_logging(verbosity=verbosity)

    mpos_path = get_mpos_path()

    internal_fs = mpos_path / 'internal_filesystem'
    lib_mpos = internal_fs / 'lib' / 'mpos'
    assert_is_dir(lib_mpos)
    apps_path = internal_fs / 'apps'
    assert_is_dir(apps_path)

    mpremote_bin = get_mpremote_bin()

    print('\n')

    popenargs = (mpremote_bin, 'fs', 'cp')

    if local_path:
        if not local_path.is_absolute():
            local_path = mpos_path / local_path

        print(f'Copy/update app: "{local_path}" ...')

        if not local_path.exists():
            print(f'[red]Error: The specified source path "{local_path}" does not exist.[/red]')
            return

        # Is source a sub path of "apps_path" ?
        if local_path.is_relative_to(apps_path):
            local_rel_path = local_path.relative_to(mpos_path)
            remote_path = f':/{local_path.relative_to(internal_fs)}'
        else:
            raise NotImplementedError
    else:
        local_path = get_newest_files(lib_mpos, limit=new_file_limit)
        if not local_path:
            print('Copy/update all files in lib/mpos to the device')
            local_path = lib_mpos

        local_rel_path = local_path.relative_to(mpos_path)
        remote_path = f':/{local_path.relative_to(lib_mpos.parent)}'

    if local_path.is_dir():
        popenargs += ('-r',)
        print(f'Copying directory "[bold]{local_rel_path}[/bold]" to device at "[bold]{remote_path}[/bold]" ...')
    else:
        print(f'Copying file "[bold]{local_rel_path}[/bold]" to device at "[bold]{remote_path}[/bold]" ...')

    popenargs += (local_rel_path, remote_path)
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
        local_rel_path = 'internal_filesystem/apps'
        remote_path = ':/apps'
    else:
        print(f'Copy/update {app=} ...')
        local_rel_path = f'internal_filesystem/apps/{app.name}'
        remote_path = f':/apps/{app.name}'

    popenargs += (local_rel_path, remote_path)
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
