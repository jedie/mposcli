"""
    Allow mposcli to be executable
    through `python -m mposcli.cli_dev`.
"""

from mposcli.cli_dev import main


if __name__ == '__main__':
    main()
