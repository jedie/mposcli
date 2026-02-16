# mposcli

[![tests](https://github.com/jedie/mposcli/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/jedie/mposcli/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/mposcli/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/mposcli)
[![mposcli @ PyPi](https://img.shields.io/pypi/v/mposcli?label=mposcli%20%40%20PyPi)](https://pypi.org/project/mposcli/)
[![Python Versions](https://img.shields.io/pypi/pyversions/mposcli)](https://github.com/jedie/mposcli/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/mposcli)](https://github.com/jedie/mposcli/blob/main/LICENSE)

Experimental CLI helper for MicroPythonOS: https://github.com/MicroPythonOS/MicroPythonOS

Main Idea: Install it via pipx (see below) and use `mposcli` command in MicroPythonOS repository path.

Install, e.g.:

```
sudo apt install pipx

pipx install mposcli
```

To upgrade an existing installation: Just call: `pipx upgrade PyHardLinkBackup`

Usage e.g.:

```
cd ~/MicroPythonOS
~/MicroPythonOS$ mposcli run-desktop
```


## CLI

[comment]: <> (✂✂✂ auto generated main help start ✂✂✂)
```
usage: mposcli [-h] {build,flash,run-desktop,update-submodules,version}



╭─ options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help             show this help message and exit                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ subcommands ────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ (required)                                                                                                           │
│   • build              Build MicroPythonOS by calling: ./scripts/build_mpos.sh <target> see:                         │
│                        https://docs.micropythonos.com/os-development/                                                │
│   • flash              Flash MicroPythonOS to the device. Display a file chooser to select the image to flash. All   │
│                        lvgl_micropython/build/*.bin files will be shown in the file chooser. see:                    │
│                        https://docs.micropythonos.com/os-development/installing-on-esp32/                            │
│   • run-desktop        Run MicroPythonOS on desktop. see:                                                            │
│                        https://docs.micropythonos.com/getting-started/running/#running-on-desktop                    │
│   • update-submodules  Update MicroPythonOS repository and all submodules see:                                       │
│                        https://docs.micropythonos.com/os-development/linux/#optional-updating-the-code               │
│   • version            Print version and exit                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated main help end ✂✂✂)



## CLI - build

[comment]: <> (✂✂✂ auto generated build start ✂✂✂)
```
usage: mposcli build [-h] [--target {esp32,esp32s3,unix,macOS}] [-v]

Build MicroPythonOS by calling: ./scripts/build_mpos.sh <target> see: https://docs.micropythonos.com/os-development/

╭─ options ────────────────────────────────────────────────────────────────╮
│ -h, --help       show this help message and exit                         │
│ --target {esp32,esp32s3,unix,macOS}                                      │
│                  Target platform to build for. (default: unix)           │
│ -v, --verbosity  Verbosity level; e.g.: -v, -vv, -vvv, etc. (repeatable) │
╰──────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated build end ✂✂✂)



## CLI - flash

[comment]: <> (✂✂✂ auto generated flash start ✂✂✂)
```
usage: mposcli flash [-h] [FLASH OPTIONS]

Flash MicroPythonOS to the device. Display a file chooser to select the image to flash. All lvgl_micropython/build/*.bin files will be shown in the file chooser. see: https://docs.micropythonos.com/os-development/installing-on-esp32/

╭─ options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help             show this help message and exit                                                               │
│ --port STR             Port used for esptoo and mpremote (default: /dev/ttyUSB0)                                     │
│ --address STR          Address (default: 0x0)                                                                        │
│ --flash-size STR       Flash Size (default: detect)                                                                  │
│ --verify, --no-verify  Verify after flashing? (default: True)                                                        │
│ --repl, --no-repl      After flashing/verify start REPL with mpremote to see the output of the device? (default:     │
│                        True)                                                                                         │
│ -v, --verbosity        Verbosity level; e.g.: -v, -vv, -vvv, etc. (repeatable)                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated flash end ✂✂✂)



## CLI - run-desktop


[comment]: <> (✂✂✂ auto generated run-desktop start ✂✂✂)
```
usage: mposcli run-desktop [-h] [--heapsize INT] [--script {None}|STR] [--binary {None}|STR] [-v]

Run MicroPythonOS on desktop. see: https://docs.micropythonos.com/getting-started/running/#running-on-desktop

╭─ options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help           show this help message and exit                                                                 │
│ --heapsize INT       Heap size in MB (default: 8, same as PSRAM on many ESP32-S3 boards) (default: 8)                │
│ --script {None}|STR  Script file (.py) or app name to run. If omitted, starts normally. (default: None)              │
│ --binary {None}|STR  Optional name of the binary to start. If omitted, shows a file chooser to select one from the   │
│                      lvgl_micropython build directory. (default: None)                                               │
│ -v, --verbosity      Verbosity level; e.g.: -v, -vv, -vvv, etc. (repeatable)                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated run-desktop end ✂✂✂)


## CLI - update-submodules


[comment]: <> (✂✂✂ auto generated update-submodules start ✂✂✂)
```
usage: mposcli update-submodules [-h] [-v]

Update MicroPythonOS repository and all submodules see: https://docs.micropythonos.com/os-development/linux/#optional-updating-the-code

╭─ options ────────────────────────────────────────────────────────────────╮
│ -h, --help       show this help message and exit                         │
│ -v, --verbosity  Verbosity level; e.g.: -v, -vv, -vvv, etc. (repeatable) │
╰──────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated update-submodules end ✂✂✂)






## start development

At least `uv` is needed. Install e.g.: via pipx:
```bash
apt-get install pipx
pipx install uv
```

Clone the project and just start the CLI help commands.
A virtual environment will be created/updated automatically.

```bash
~$ git clone https://github.com/jedie/mposcli.git
~$ cd mposcli
~/mposcli$ ./cli.py --help
~/mposcli$ ./dev-cli.py --help
```

[comment]: <> (✂✂✂ auto generated dev help start ✂✂✂)
```
usage: ./dev-cli.py [-h] {coverage,install,lint,mypy,nox,pip-audit,publish,shell-completion,test,update,update-readme-history,update-test-snapshot-files,version}



╭─ options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help     show this help message and exit                                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ subcommands ────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ (required)                                                                                                           │
│   • coverage   Run tests and show coverage report.                                                                   │
│   • install    Install requirements and 'mposcli' via pip as editable.                                               │
│   • lint       Check/fix code style by run: "ruff check --fix"                                                       │
│   • mypy       Run Mypy (configured in pyproject.toml)                                                               │
│   • nox        Run nox                                                                                               │
│   • pip-audit  Run pip-audit check against current requirements files                                                │
│   • publish    Build and upload this project to PyPi                                                                 │
│   • shell-completion                                                                                                 │
│                Setup shell completion for this CLI (Currently only for bash shell)                                   │
│   • test       Run unittests                                                                                         │
│   • update     Update dependencies (uv.lock) and git pre-commit hooks                                                │
│   • update-readme-history                                                                                            │
│                Update project history base on git commits/tags in README.md Will be exited with 1 if the README.md   │
│                was updated otherwise with 0.                                                                         │
│                                                                                                                      │
│                Also, callable via e.g.:                                                                              │
│                    python -m cli_base update-readme-history -v                                                       │
│   • update-test-snapshot-files                                                                                       │
│                Update all test snapshot files (by remove and recreate all snapshot files)                            │
│   • version    Print version and exit                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated dev help end ✂✂✂)


## History

[comment]: <> (✂✂✂ auto generated history start ✂✂✂)

* [**dev**](https://github.com/jedie/mposcli/compare/v0.1.0...main)
* [v0.1.0](https://github.com/jedie/mposcli/compare/1695026...v0.1.0)
  * 2026-02-16 - Add "update-submodules" command
  * 2026-02-16 - Add "build" command
  * 2026-02-16 - CLI command: "run-desktop"
  * 2026-02-16 - first commit

[comment]: <> (✂✂✂ auto generated history end ✂✂✂)
