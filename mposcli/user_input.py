import datetime
import sys

from rich import print


def file_chooser(paths):
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
        dt = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{idx}] {dt} - {p.name}')

    number = input('Enter number (ENTER = 0 - the newest file): ').strip() or 0
    print('Selected:', number)
    try:
        number = int(number)
    except Exception as err:
        print(f'[red]Invalid input: {err}[/red]')
        sys.exit(1)

    try:
        selection = files[number][0]
    except IndexError:
        print(f'[red]Invalid selection: {number}[/red]')
        sys.exit(1)

    print(f'Selected file: {selection}')
    return selection
