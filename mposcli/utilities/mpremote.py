import shlex
import subprocess
import time
from pathlib import Path

from bx_py_utils.path import assert_is_dir
from rich import print

from mposcli.tools import get_mpremote_bin


class MpOsPathResolver:
    def __init__(self, mpos: Path):
        self.mpos = mpos  # e.g.: ~/repos/MicroPythonOS
        self.internal_fs = mpos / 'internal_filesystem'
        self.lib_mpos = self.internal_fs / 'lib' / 'mpos'
        assert_is_dir(self.lib_mpos)
        self.apps_path = self.internal_fs / 'apps'
        assert_is_dir(self.apps_path)

    def resolve(self, source: Path):
        source = source.resolve()
        assert source.exists(), f'Not existing path: {source=}'
        assert source.is_relative_to(self.mpos), f'{source=} is not inside {self.mpos=}'

        if source.is_relative_to(self.apps_path):
            device_base_path = self.apps_path.parent
        elif source.is_relative_to(self.lib_mpos):
            device_base_path = self.lib_mpos.parent
        elif source.is_relative_to(self.internal_fs):
            device_base_path = self.internal_fs
        else:
            raise ValueError(f'Path {source} is not in a recognized location')

        remote_path = source.relative_to(device_base_path)
        source_path = source.relative_to(self.mpos)
        if source.is_dir():
            remote_path = remote_path.parent
            local_path_str = f'{source_path}/'
            remote_str = f':{remote_path}/'
        else:
            local_path_str = f'{source_path}'
            remote_str = f':{remote_path}'

        return local_path_str, remote_str


def start_mpremote_repl(max_try=10, wait_time=1):
    print('Starting mpremote REPL...')
    time.sleep(wait_time)
    mpremote_bin = get_mpremote_bin()

    popen_args = (mpremote_bin, 'repl')

    for try_count in range(max_try):
        print(f'\n+ {shlex.join(str(arg) for arg in popen_args)}')
        try:
            return subprocess.check_call(popen_args)
        except subprocess.CalledProcessError as err:
            print(
                f'[yellow]mpremote finished with [red]exit code {err.returncode!r}[/red]'
                f' Retrying in {wait_time} seconds... (try {try_count + 1}/{max_try})'
            )
            time.sleep(wait_time)
