from pathlib import Path

from bx_py_utils.path import assert_is_dir


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
