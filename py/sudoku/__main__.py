"""Run sudoku game from command line"""

import sys
from . import _gui

if __name__ == '__main__':
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--gui', '-g', 'gui']:
            _gui.run()
        elif sys.argv[1] in ['--help', '-h']:
            print("Sudoku Game")
            print("Usage: python -m sudoku [OPTIONS]")
            print("")
            print("Options:")
            print("  --gui, -g    Launch GUI (default)")
            print("  --help, -h   Show this help message")
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Use --help for usage information")
    else:
        # Default: launch GUI
        _gui.run()
