import datetime
import os
import sys
from pathlib import Path

from rich import print


def file_chooser(paths) -> Path | None:
    """
    Display a numbered list of files sorted by modification time (newest first).
    Show mtime and file name. Input number, ENTER = 1. Return selected Path.
    """
    print()

    files = [(p, p.stat().st_mtime) for p in paths if p.is_file()]
    if not files:
        print('[red]No files found.[/red]')
        return None
    files.sort(key=lambda x: x[1], reverse=True)

    print('[bold]Choose a file:[/bold]\n')
    for idx, (p, mtime) in enumerate(files):
        dt = datetime.datetime.fromtimestamp(mtime).astimezone().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{idx}] {dt} - {p.name}')

    print()

    number = input('Enter number (ENTER = 0 - the newest file): ').strip() or 0
    print('Selected:', number)
    try:
        number = int(number)
    except ValueError as err:
        print(f'[red]Invalid input: {err}[/red]')
        sys.exit(1)

    try:
        selection = files[number][0]
    except IndexError:
        print(f'[red]Invalid selection: {number}[/red]')
        sys.exit(1)

    print(f'Selected file: {selection}')
    return selection


def get_newest_files(directory, limit=10) -> Path | None:
    files = []

    def scan(dir_path):
        with os.scandir(dir_path) as it:
            for entry in it:
                if entry.is_file(follow_symlinks=False):
                    files.append((entry, entry.stat().st_mtime))
                elif entry.is_dir(follow_symlinks=False):
                    scan(entry.path)

    scan(directory)
    files.sort(key=lambda x: x[1], reverse=True)

    print(f'[bold]Choose a file[/bold] (only from the newest {limit}):\n')
    for idx, (entry, mtime) in enumerate(files[:limit]):
        dt = datetime.datetime.fromtimestamp(mtime).astimezone().strftime('%Y-%m-%d %H:%M:%S')
        rel_path = Path(entry.path).relative_to(directory)
        print(f'[{idx}] {dt} - {rel_path}')

    print()

    number = input('Enter number (ENTER = 0 - the newest file, "a" for all files): ').strip() or '0'
    print('Selected:', number)
    if number.lower() == 'a':
        return None

    try:
        number = int(number)
    except ValueError as err:
        print(f'[red]Invalid input: {err}[/red]')
        sys.exit(1)

    try:
        selection = files[number][0]
    except IndexError:
        print(f'[red]Invalid selection: {number}[/red]')
        sys.exit(1)

    print(f'Selected file: {selection}')
    return Path(selection)
