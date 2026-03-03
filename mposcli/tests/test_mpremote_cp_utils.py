import tempfile
from pathlib import Path
from unittest import TestCase

from mposcli.mpremote_cp_utils import MpOsPathResolver


class ProjectSetupTestCase(TestCase):
    def test_mpos_path_resolver(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            mpos_path = Path(temp_dir)

            camera_assets = mpos_path / 'internal_filesystem/apps/com.micropythonos.camera/assets/'
            camera_assets.mkdir(parents=True)
            (camera_assets / 'camera_app.py').touch()

            board_path = mpos_path / 'internal_filesystem/lib/mpos/board/'
            board_path.mkdir(parents=True)
            (board_path / 'unphone.py').touch()

            (mpos_path / 'internal_filesystem/lib/drivers/display/hx8357d/').mkdir(parents=True)

            resolver = MpOsPathResolver(mpos=mpos_path)
            self.assertEqual(
                resolver.resolve(mpos_path / 'internal_filesystem/apps/com.micropythonos.camera'),
                (
                    'internal_filesystem/apps/com.micropythonos.camera/',
                    ':apps/',
                ),
            )
            self.assertEqual(
                resolver.resolve(mpos_path / 'internal_filesystem/apps/com.micropythonos.camera/assets/'),
                (
                    'internal_filesystem/apps/com.micropythonos.camera/assets/',
                    ':apps/com.micropythonos.camera/',
                ),
            )
            self.assertEqual(
                resolver.resolve(mpos_path / 'internal_filesystem/apps/com.micropythonos.camera/assets/camera_app.py'),
                (
                    'internal_filesystem/apps/com.micropythonos.camera/assets/camera_app.py',
                    ':apps/com.micropythonos.camera/assets/camera_app.py',
                ),
            )

            self.assertEqual(
                resolver.resolve(mpos_path / 'internal_filesystem/lib/mpos/board/'),
                (
                    'internal_filesystem/lib/mpos/board/',
                    ':mpos/',
                ),
            )
            self.assertEqual(
                resolver.resolve(mpos_path / 'internal_filesystem/lib/mpos/board/unphone.py'),
                (
                    'internal_filesystem/lib/mpos/board/unphone.py',
                    ':mpos/board/unphone.py',
                ),
            )

            self.assertEqual(
                resolver.resolve(mpos_path / 'internal_filesystem/lib/drivers/display/hx8357d'),
                (
                    'internal_filesystem/lib/drivers/display/hx8357d/',
                    ':lib/drivers/display/',
                ),
            )
            self.assertEqual(
                resolver.resolve(mpos_path / 'internal_filesystem/lib/drivers/display'),
                (
                    'internal_filesystem/lib/drivers/display/',
                    ':lib/drivers/',
                ),
            )
