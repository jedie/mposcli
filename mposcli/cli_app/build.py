import logging
from typing import Annotated, Literal

import tyro
from bx_py_utils.path import assert_is_file
from cli_base.cli_tools.subprocess_utils import verbose_check_call
from cli_base.cli_tools.verbosity import setup_logging
from cli_base.tyro_commands import TyroVerbosityArgType
from rich import print  # noqa

from mposcli.cli_app import app
from mposcli.mpos_utils import get_mpos_path


logger = logging.getLogger(__name__)


@app.command
def build(
    target: Annotated[
        Literal['esp32', 'esp32s3', 'unix', 'macOS'],
        tyro.conf.arg(
            help='Target platform to build for.',
        ),
    ] = 'unix',
    /,
    verbosity: TyroVerbosityArgType = 1,
):
    """
    Build MicroPythonOS by calling: ./scripts/build_mpos.sh <target>
    see: https://docs.micropythonos.com/os-development/
    """
    setup_logging(verbosity=verbosity)

    mpos_path = get_mpos_path()

    script_path = mpos_path / 'scripts' / 'build_mpos.sh'
    assert_is_file(script_path)

    verbose_check_call(
        script_path,
        target,
        verbose=True,
        cwd=mpos_path,
        timeout=None,
        text=None,
    )
