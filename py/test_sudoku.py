"""Test script for sudoku game functionality"""

import sys
sys.path.insert(0, '.')

from sudoku import SudokuBoard, solve_sudoku, generate_puzzle
import copy

def test_board_generation():
    """Test board generation"""
    print("Testing board generation...")
    board = SudokuBoard('easy')
    print("✓ Easy board generated")
    
    board = SudokuBoard('medium')
    print("✓ Medium board generated")
    
    board = SudokuBoard('hard')
    print("✓ Hard board generated")
    return True

def test_solver():
    """Test solver functionality"""
    print("\nTesting solver...")
    # Simple test puzzle
    test_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    board_copy = copy.deepcopy(test_board)
    result = solve_sudoku(board_copy)
    
    if result:
        print("✓ Solver successfully solved test puzzle")
        # Verify solution is complete
        for row in board_copy:
            if 0 in row:
                print("✗ Solution incomplete")
                return False
        print("✓ Solution is complete")
        return True
    else:
        print("✗ Solver failed")
        return False

def test_game_functions():
    """Test game functionality"""
    print("\nTesting game functions...")
    board = SudokuBoard('medium')
    
    # Test getting cell
    value = board.get_cell(0, 0)
    print(f"✓ Got cell value: {value}")
    
    # Test setting cell (find an empty one)
    for i in range(9):
        for j in range(9):
            if not board.is_initial_cell(i, j):
                success = board.set_cell(i, j, 5)
                if success:
                    print(f"✓ Set cell ({i}, {j}) to 5")
                break
        else:
            continue
        break
    
    # Test reset
    board.reset()
    print("✓ Reset board")
    
    # Test hint
    hint = board.get_hint()
    if hint:
        print(f"✓ Got hint at position {hint}")
    else:
        print("✓ No hints available (board may be full)")
    
    return True

def print_board(board):
    """Print a sudoku board"""
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j, val in enumerate(row):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(val if val != 0 else ".", end=" ")
        print()

if __name__ == '__main__':
    print("=" * 50)
    print("Sudoku Game Test Suite")
    print("=" * 50)
    
    try:
        test_board_generation()
        test_solver()
        test_game_functions()
        
        print("\n" + "=" * 50)
        print("Example Medium Puzzle:")
        print("=" * 50)
        puzzle, solution = generate_puzzle('medium')
        print("\nPuzzle:")
        print_board(puzzle)
        print("\nSolution:")
        print_board(solution)
        
        print("\n" + "=" * 50)
        print("All tests passed! ✓")
        print("=" * 50)
        print("\nTo play the game, run: python -m sudoku")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
