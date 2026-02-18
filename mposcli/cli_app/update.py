import logging

from cli_base.cli_tools.git import Git
from cli_base.cli_tools.verbosity import setup_logging
from cli_base.tyro_commands import TyroVerbosityArgType
from rich import print  # noqa

from mposcli.cli_app import app
from mposcli.mpos_utils import get_mpos_path


logger = logging.getLogger(__name__)


def _update_submodules(git: Git):
    git.git_verbose_check_call('submodule', 'foreach', '--recursive', 'git', 'clean', '-f', ';', 'git', 'checkout', '.')
    git.git_verbose_check_call('pull', '--recurse-submodules')


@app.command
def update_submodules(verbosity: TyroVerbosityArgType = 1):
    """
    Updates MicroPythonOS git submodules only.
    Use "mposcli update" to update the main repository and optionally the submodules as well.
    see: https://docs.micropythonos.com/os-development/linux/#optional-updating-the-code
    """
    setup_logging(verbosity=verbosity)
    mpos_path = get_mpos_path()
    git = Git(cwd=mpos_path)
    _update_submodules(git)


@app.command
def update(verbosity: TyroVerbosityArgType = 1):
    """
    Update MicroPythonOS repository. Assume that there is a "origin" and/or "upstream" remote configured.
    Will also ask if you want to update the submodules as well, which is recommended.
    """
    setup_logging(verbosity=verbosity)
    mpos_path = get_mpos_path()
    git = Git(cwd=mpos_path)

    main_branch_name = git.get_main_branch_name()
    print(f'The main branch is: [yellow blue]{main_branch_name}')

    git.git_verbose_check_call('fetch', '--all')

    output = git.git_verbose_check_output('remote')
    remotes = output.splitlines()
    print(f'Git {remotes=}')

    for remote_name in ('origin', 'upstream'):
        if remote_name in remotes:
            git.git_verbose_check_call('rebase', '--no-verify', f'{remote_name}/{main_branch_name}', exit_on_error=True)
        else:
            print(f'[yellow]Remote "{remote_name}" not found, skipping rebase to it.')

    print('\n')
    if input('Do you want to update submodules as well? [Y/n] (default: Yes): ') in ('y', ''):
        print('\nUpdating submodules...\n')
        _update_submodules(git)
