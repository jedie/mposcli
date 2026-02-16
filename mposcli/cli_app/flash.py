import logging
from typing import Annotated

import tyro
from cli_base.cli_tools.subprocess_utils import verbose_check_call
from cli_base.cli_tools.verbosity import setup_logging
from cli_base.tyro_commands import TyroVerbosityArgType
from rich import print  # noqa

from mposcli.cli_app import app
from mposcli.mpos_utils import get_mpos_path
from mposcli.tools import get_esptool_bin, get_mpremote_bin
from mposcli.user_input import file_chooser


logger = logging.getLogger(__name__)


@app.command
def flash(
    port: Annotated[str, tyro.conf.arg(help='Port used for esptoo and mpremote')] = '/dev/ttyUSB0',
    address: Annotated[str, tyro.conf.arg(help='Address')] = '0x0',
    flash_size: Annotated[str, tyro.conf.arg(help='Flash Size')] = 'detect',
    verify: Annotated[bool, tyro.conf.arg(help='Verify after flashing?')] = True,
    repl: Annotated[
        bool,
        tyro.conf.arg(help='After flashing/verify start REPL with mpremote to see the output of the device?'),
    ] = True,
    verbosity: TyroVerbosityArgType = 1,
):
    """
    Flash MicroPythonOS to the device. Display a file chooser to select the image to flash.
    All lvgl_micropython/build/*.bin files will be shown in the file chooser.
    see: https://docs.micropythonos.com/os-development/installing-on-esp32/
    """
    setup_logging(verbosity=verbosity)

    mpos_path = get_mpos_path()

    esptool_bin = get_esptool_bin()
    verbose_check_call(esptool_bin, 'version')
    mpremote_bin = get_mpremote_bin()
    verbose_check_call(mpremote_bin, '--version')

    print('\n')

    lvgl_micropython_build_path = mpos_path / 'lvgl_micropython' / 'build'
    image_files = lvgl_micropython_build_path.glob('*.bin')
    image_file = file_chooser(image_files)

    verbose_check_call(
        esptool_bin,
        '--port',
        port,
        'write-flash',
        '--flash-size',
        flash_size,
        address,
        image_file,
        verbose=True,
        cwd=mpos_path,
        timeout=None,
        text=None,
    )

    if verify:
        verbose_check_call(
            esptool_bin,
            '--port',
            port,
            'verify-flash',
            address,
            image_file,
            verbose=True,
            cwd=mpos_path,
            timeout=None,
            text=None,
        )

    if repl:
        verbose_check_call(
            mpremote_bin,
            'repl',
            port,
            verbose=True,
            cwd=mpos_path,
            timeout=None,
            text=None,
        )
