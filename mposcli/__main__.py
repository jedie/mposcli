"""
    Allow mposcli to be executable
    through `python -m mposcli`.
"""

from mposcli.cli_app import main


if __name__ == '__main__':
    main()
