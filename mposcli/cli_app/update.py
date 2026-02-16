import logging

from cli_base.cli_tools.subprocess_utils import verbose_check_call
from cli_base.cli_tools.verbosity import setup_logging
from cli_base.tyro_commands import TyroVerbosityArgType
from rich import print  # noqa

from mposcli.cli_app import app
from mposcli.mpos_utils import get_mpos_path


logger = logging.getLogger(__name__)


@app.command
def update_submodules(verbosity: TyroVerbosityArgType = 1):
    """
    Update MicroPythonOS repository and all submodules
    see: https://docs.micropythonos.com/os-development/linux/#optional-updating-the-code
    """
    setup_logging(verbosity=verbosity)
    mpos_path = get_mpos_path()

    commands = (
        ('git', 'submodule', 'foreach', '--recursive', 'git', 'clean', '-f', ';', 'git', 'checkout', '.'),
        ('git', 'pull', '--recurse-submodules'),
    )
    for popenargs in commands:
        verbose_check_call(
            *popenargs,
            verbose=True,
            cwd=mpos_path,
            timeout=None,
            text=None,
        )
