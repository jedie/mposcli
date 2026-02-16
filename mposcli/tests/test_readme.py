from bx_py_utils.auto_doc import assert_readme_block
from bx_py_utils.path import assert_is_file
from cli_base.cli_tools.test_utils.assertion import assert_in
from cli_base.cli_tools.test_utils.rich_test_utils import NoColorEnvRich, invoke
from manageprojects.tests.base import BaseTestCase

from mposcli import constants
from mposcli.cli_dev import PACKAGE_ROOT


def assert_cli_help_in_readme(text_block: str, marker: str):
    README_PATH = PACKAGE_ROOT / 'README.md'
    assert_is_file(README_PATH)

    text_block = text_block.replace(constants.CLI_EPILOG, '')
    text_block = f'```\n{text_block.strip()}\n```'
    assert_readme_block(
        readme_path=README_PATH,
        text_block=text_block,
        start_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} start ✂✂✂)',
        end_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} end ✂✂✂)',
    )


class ReadmeTestCase(BaseTestCase):

    def test_main_help(self):
        with NoColorEnvRich():
            stdout = invoke(
                cli_bin=PACKAGE_ROOT / 'cli.py',
                args=['--help'],
                strip_line_prefix='usage: ',
            )
        assert_in(
            content=stdout,
            parts=(
                'usage: mposcli [-h]',
                ' version ',
                'Print version and exit',
                constants.CLI_EPILOG,
            ),
        )
        assert_cli_help_in_readme(text_block=stdout, marker='main help')

    def test_dev_help(self):
        with NoColorEnvRich():
            stdout = invoke(
                cli_bin=PACKAGE_ROOT / 'dev-cli.py',
                args=['--help'],
                strip_line_prefix='usage: ',
            )
        assert_in(
            content=stdout,
            parts=(
                'usage: ./dev-cli.py [-h]',
                ' lint ',
                ' coverage ',
                ' update-readme-history ',
                ' publish ',
                constants.CLI_EPILOG,
            ),
        )
        assert_cli_help_in_readme(text_block=stdout, marker='dev help')

    def test_cli_commands(self):
        commands = ('build', 'run-desktop')
        for command in commands:
            with self.subTest(command):
                with NoColorEnvRich():
                    stdout = invoke(
                        cli_bin=PACKAGE_ROOT / 'cli.py',
                        args=[command, '--help'],
                        strip_line_prefix='usage: ',
                    )
                assert_in(
                    content=stdout,
                    parts=(f'usage: mposcli {command} [-h]',),
                )
                assert_cli_help_in_readme(text_block=stdout, marker=command)
