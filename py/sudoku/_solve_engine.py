"""Sudoku solving engine using backtracking algorithm.

This module implements a backtracking algorithm to solve Sudoku puzzles. The solver
recursively fills empty cells by trying digits 1-9 and backtracking when conflicts
are detected.

The algorithm checks three constraints for each placement:
- No duplicate in the same row
- No duplicate in the same column
- No duplicate in the same 3x3 box

Functions:
    solve: Main entry point to solve a Sudoku puzzle
    is_valid_board: Validate that a board state has no conflicts

"""


def solve(board):
    """
    Solve a sudoku puzzle using backtracking
    
    Args:
        board: 9x9 2D list representing the sudoku board (0 for empty cells)
    
    Returns:
        bool: True if solved successfully, False otherwise
    """
    return _solve_backtrack(board)


def _solve_backtrack(board):
    """Internal backtracking solver"""
    # Find next empty cell
    empty = _find_empty_cell(board)
    if not empty:
        return True  # No empty cells, puzzle is solved
    
    row, col = empty
    
    # Try digits 1-9
    for num in range(1, 10):
        if _is_valid(board, row, col, num):
            board[row][col] = num
            
            if _solve_backtrack(board):
                return True
            
            # Backtrack
            board[row][col] = 0
    
    return False


def _find_empty_cell(board):
    """Find the next empty cell (with value 0)"""
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None


def _is_valid(board, row, col, num):
    """Check if placing num at board[row][col] is valid"""
    # Check row
    for j in range(9):
        if board[row][j] == num:
            return False
    
    # Check column
    for i in range(9):
        if board[i][col] == num:
            return False
    
    # Check 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    
    return True


def is_valid_board(board):
    """
    Check if the current board state is valid (no conflicts)
    
    Args:
        board: 9x9 2D list representing the sudoku board
    
    Returns:
        bool: True if valid, False otherwise
    """
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                num = board[i][j]
                board[i][j] = 0  # Temporarily remove to check
                if not _is_valid(board, i, j, num):
                    board[i][j] = num
                    return False
                board[i][j] = num
    return True
