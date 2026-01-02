





"""Sudoku board generation and game logic.

This module provides functionality for generating valid Sudoku puzzles with unique
solutions, managing game state, and validating moves. It includes:

- Puzzle generation with configurable difficulty levels (easy, medium, hard)
- Complete board generation using randomized diagonal boxes and backtracking
- Solution validation ensuring unique solutions
- Game board management with initial puzzle tracking
- Move validation for rows, columns, and 3x3 boxes
- Hint system and board state management

Classes:
    SudokuBoard: Main game board class with puzzle generation and game logic

Functions:
    is_valid_move: Validate if a number can be placed at a specific position
    solve_sudoku: Solve a Sudoku puzzle using backtracking algorithm
    generate_full_board: Generate a complete, valid Sudoku board
    count_solutions: Count number of solutions for a puzzle (up to a limit)
    generate_puzzle: Generate a Sudoku puzzle with unique solution at specified difficulty

"""

import random
import copy
def is_valid_move(board, row, col, num):
    """Check if placing num at board[row][col] is valid"""
    # Check row
    if num in board[row]:
        return False
    
    # Check column
    if num in [board[i][col] for i in range(9)]:
        return False
    
    # Check 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    
    return True


def solve_sudoku(board):
    """Solve sudoku using backtracking"""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid_move(board, row, col, num):
                        board[row][col] = num
                        
                        if solve_sudoku(board):
                            return True
                        
                        board[row][col] = 0
                
                return False
    return True


def generate_full_board():
    """Generate a complete, valid sudoku board"""
    board = [[0 for _ in range(9)] for _ in range(9)]
    
    # Fill diagonal 3x3 boxes first (they don't depend on each other)
    for box in range(0, 9, 3):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                board[box + i][box + j] = nums[i * 3 + j]
    
    # Solve the rest
    solve_sudoku(board)
    return board


def count_solutions(board, limit=2):
    """Count number of solutions (up to limit)"""
    count = [0]
    
    def solve_count(board):
        if count[0] >= limit:
            return
        
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid_move(board, row, col, num):
                            board[row][col] = num
                            solve_count(board)
                            board[row][col] = 0
                    return
        
        count[0] += 1
    
    board_copy = copy.deepcopy(board)
    solve_count(board_copy)
    return count[0]


def generate_puzzle(difficulty='medium'):
    """Generate a sudoku puzzle with unique solution
    
    Args:
        difficulty: 'easy' (40-45 clues), 'medium' (30-35 clues), 'hard' (25-30 clues)
    """
    board = generate_full_board()
    solution = copy.deepcopy(board)
    
    # Determine number of cells to remove
    if difficulty == 'easy':
        cells_to_remove = random.randint(36, 41)  # 40-45 clues remain
    elif difficulty == 'medium':
        cells_to_remove = random.randint(46, 51)  # 30-35 clues remain
    elif difficulty == 'hard':
        cells_to_remove = random.randint(51, 56)  # 25-30 clues remain
    else:
        cells_to_remove = 46
    
    # Remove cells while ensuring unique solution
    positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(positions)
    
    removed = 0
    for row, col in positions:
        if removed >= cells_to_remove:
            break
        
        backup = board[row][col]
        board[row][col] = 0
        
        # Check if still has unique solution
        board_copy = copy.deepcopy(board)
        if count_solutions(board_copy, 2) == 1:
            removed += 1
        else:
            board[row][col] = backup
    
    return board, solution


class SudokuBoard(object):
    """Represents a sudoku game board"""
    
    def __init__(self, difficulty='medium'):
        super().__init__()
        self._base_size = 3
        self._board_length = self._base_size ** 2
        self._difficulty = difficulty
        self._puzzle, self._solution = generate_puzzle(difficulty)
        self._current_board = copy.deepcopy(self._puzzle)
        self._initial_board = copy.deepcopy(self._puzzle)

    @property
    def difficulty(self):
        """(str) Difficulty level: easy, medium, or hard"""
        return self._difficulty

    @property
    def puzzle(self):
        """Get the initial puzzle board"""
        return self._initial_board
    
    @property
    def solution(self):
        """Get the solution board"""
        return self._solution
    
    @property
    def current_board(self):
        """Get the current state of the board"""
        return self._current_board
    
    def get_cell(self, row, col):
        """Get value at specific cell"""
        return self._current_board[row][col]
    
    def set_cell(self, row, col, value):
        """Set value at specific cell if it's not part of initial puzzle"""
        if self._initial_board[row][col] == 0:
            self._current_board[row][col] = value
            return True
        return False
    
    def is_initial_cell(self, row, col):
        """Check if cell is part of the initial puzzle"""
        return self._initial_board[row][col] != 0
    
    def is_valid_move(self, row, col, num):
        """Check if move is valid"""
        return is_valid_move(self._current_board, row, col, num)
    
    def is_complete(self):
        """Check if puzzle is completely filled"""
        for row in range(9):
            for col in range(9):
                if self._current_board[row][col] == 0:
                    return False
        return True
    
    def is_correct(self):
        """Check if current board matches solution"""
        return self._current_board == self._solution
    
    def reset(self):
        """Reset board to initial puzzle state"""
        self._current_board = copy.deepcopy(self._initial_board)
    
    def solve(self):
        """Fill in the solution"""
        self._current_board = copy.deepcopy(self._solution)
    
    def get_hint(self):
        """Get a hint by revealing one empty cell from the solution"""
        empty_cells = [(i, j) for i in range(9) for j in range(9) 
                      if self._current_board[i][j] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self._current_board[row][col] = self._solution[row][col]
            return row, col
        return None
    