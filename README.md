# Sudoku Game

A complete Sudoku game with a beautiful PySide6 GUI and built-in solver.

## Features

- **Three Difficulty Levels**: Easy, Medium, and Hard
- **Intelligent Puzzle Generation**: Creates valid puzzles with unique solutions
- **Built-in Solver**: Uses backtracking algorithm to solve any valid Sudoku
- **Interactive GUI**: Clean, modern interface built with PySide6
- **Game Features**:
  - New Game generation
  - Hints system
  - Solution checker
  - Reset to initial puzzle
  - Show complete solution
  - Visual distinction between initial clues and user entries

## Installation

1. Install the required dependency:
```bash
pip install PySide6
```

## Usage

### Running the GUI Game

To launch the interactive game:

```bash
python -m sudoku
```

Or explicitly:

```bash
python -m sudoku --gui
```

### Using as a Library

```python
from sudoku import SudokuBoard, generate_puzzle, solve_sudoku

# Create a new game
board = SudokuBoard('medium')

# Get puzzle and solution
puzzle, solution = generate_puzzle('hard')

# Solve a puzzle
import copy
puzzle_copy = copy.deepcopy(puzzle)
solve_sudoku(puzzle_copy)
print(puzzle_copy)

# Access board properties
value = board.get_cell(0, 0)
board.set_cell(1, 1, 5)
is_initial = board.is_initial_cell(0, 0)
board.get_hint()
board.reset()
board.solve()
```

## Game Controls

- **Difficulty Dropdown**: Select Easy, Medium, or Hard
- **New Game**: Generate a new puzzle with selected difficulty
- **Hint**: Reveal one cell from the solution
- **Check**: Verify if your current solution is correct
- **Solve**: Show the complete solution
- **Reset**: Clear all user entries and return to initial puzzle

## How to Play

1. Launch the game
2. Select your difficulty level
3. Click "New Game" to generate a puzzle
4. Click on any white cell to enter a number (1-9)
5. Initial puzzle numbers (gray cells) cannot be changed
6. Use "Hint" if you're stuck
7. Use "Check" to verify your progress
8. Complete the puzzle so each row, column, and 3x3 box contains digits 1-9

## Implementation Details

### Puzzle Generation Algorithm

1. Generates a complete, valid Sudoku board by:
   - Filling diagonal 3x3 boxes with random numbers
   - Using backtracking to complete the remaining cells
2. Removes cells while ensuring unique solution:
   - Easy: 40-45 clues remain
   - Medium: 30-35 clues remain
   - Hard: 25-30 clues remain
3. Validates that each removal maintains exactly one solution

### Solver Algorithm

Uses a backtracking algorithm:
1. Find next empty cell
2. Try digits 1-9
3. Check if digit is valid (no conflicts in row, column, or 3x3 box)
4. Recursively solve remaining cells
5. Backtrack if no valid solution found

## Project Structure

```
sudoku/
├── __init__.py          # Package exports
├── __main__.py          # Command-line entry point
├── _sudoku.py          # Board logic and puzzle generation
├── _solve_engine.py    # Solver algorithms
└── _gui.py             # PySide6 GUI implementation
```

## Requirements

- Python 3.7+
- PySide6

## License

See main repository LICENSE file.

## Credits

Created as a complete Sudoku game implementation with modern GUI and efficient solving algorithms.
