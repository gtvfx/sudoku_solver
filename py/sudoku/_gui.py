"""Sudoku GUI using PySide6"""
import sys
from PySide6 import QtCore, QtGui, QtWidgets

from ._sudoku import SudokuBoard


class SudokuCell(QtWidgets.QLineEdit):
    """Custom cell widget for sudoku grid"""
    
    cell_changed = QtCore.Signal(int, int, int)  # row, col, value
    
    def __init__(self, row, col, is_initial=False):
        super().__init__()
        self.row = row
        self.col = col
        self.is_initial = is_initial
        
        # Styling
        self.setMaxLength(1)
        self.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.setFont(font)
        self.setFixedSize(50, 50)
        
        if is_initial:
            self.setReadOnly(True)
            self.setStyleSheet("""
                QLineEdit {
                    background-color: #e8e8e8;
                    color: #000000;
                    border: 1px solid #999;
                }
            """)
        else:
            self.setStyleSheet("""
                QLineEdit {
                    background-color: #ffffff;
                    color: #0066cc;
                    border: 1px solid #999;
                }
                QLineEdit:focus {
                    border: 2px solid #0066cc;
                }
            """)
        
        self.textChanged.connect(self._on_text_changed)
    
    def _on_text_changed(self, text):
        """Handle text input"""
        if text and text.isdigit():
            value = int(text)
            if 1 <= value <= 9:
                self.cell_changed.emit(self.row, self.col, value)
            else:
                self.setText('')
        elif text == '':
            self.cell_changed.emit(self.row, self.col, 0)
        else:
            self.setText('')
    
    def set_value(self, value):
        """Set cell value without triggering signal"""
        self.blockSignals(True)
        self.setText(str(value) if value != 0 else '')
        self.blockSignals(False)
    
    def set_initial(self, is_initial):
        """Update whether cell is initial"""
        self.is_initial = is_initial
        self.setReadOnly(is_initial)
        if is_initial:
            self.setStyleSheet("""
                QLineEdit {
                    background-color: #e8e8e8;
                    color: #000000;
                    border: 1px solid #999;
                }
            """)
        else:
            self.setStyleSheet("""
                QLineEdit {
                    background-color: #ffffff;
                    color: #0066cc;
                    border: 1px solid #999;
                }
                QLineEdit:focus {
                    border: 2px solid #0066cc;
                }
            """)


class SudokuGUI(QtWidgets.QMainWindow):
    """Main sudoku game window"""
    
    def __init__(self):
        super().__init__()
        self.board = None
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.init_ui()
        self.new_game('medium')
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('Sudoku Game')
        self.setFixedSize(600, 700)
        
        # Central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        
        # Title
        title = QtWidgets.QLabel('Sudoku')
        title.setAlignment(QtCore.Qt.AlignCenter)
        title_font = QtGui.QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Sudoku grid
        grid_frame = QtWidgets.QFrame()
        grid_frame.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        grid_frame.setLineWidth(3)
        grid_layout = QtWidgets.QGridLayout(grid_frame)
        grid_layout.setSpacing(0)
        
        for i in range(9):
            for j in range(9):
                cell = SudokuCell(i, j)
                cell.cell_changed.connect(self.on_cell_changed)
                self.cells[i][j] = cell
                grid_layout.addWidget(cell, i, j)
                
                # Add thicker borders for 3x3 boxes
                if j % 3 == 2 and j < 8:
                    cell.setStyleSheet(cell.styleSheet() + "border-right: 3px solid #333;")
                if i % 3 == 2 and i < 8:
                    cell.setStyleSheet(cell.styleSheet() + "border-bottom: 3px solid #333;")
        
        main_layout.addWidget(grid_frame, alignment=QtCore.Qt.AlignCenter)
        
        # Control buttons
        controls_layout = QtWidgets.QHBoxLayout()
        
        # Difficulty selector
        self.difficulty_combo = QtWidgets.QComboBox()
        self.difficulty_combo.addItems(['Easy', 'Medium', 'Hard'])
        self.difficulty_combo.setCurrentText('Medium')
        controls_layout.addWidget(QtWidgets.QLabel('Difficulty:'))
        controls_layout.addWidget(self.difficulty_combo)
        
        controls_layout.addStretch()
        
        # New Game button
        new_game_btn = QtWidgets.QPushButton('New Game')
        new_game_btn.clicked.connect(self.on_new_game)
        controls_layout.addWidget(new_game_btn)
        
        # Hint button
        hint_btn = QtWidgets.QPushButton('Hint')
        hint_btn.clicked.connect(self.on_hint)
        controls_layout.addWidget(hint_btn)
        
        # Check button
        check_btn = QtWidgets.QPushButton('Check')
        check_btn.clicked.connect(self.on_check)
        controls_layout.addWidget(check_btn)
        
        # Solve button
        solve_btn = QtWidgets.QPushButton('Solve')
        solve_btn.clicked.connect(self.on_solve)
        controls_layout.addWidget(solve_btn)
        
        # Reset button
        reset_btn = QtWidgets.QPushButton('Reset')
        reset_btn.clicked.connect(self.on_reset)
        controls_layout.addWidget(reset_btn)
        
        main_layout.addLayout(controls_layout)
        
        # Status label
        self.status_label = QtWidgets.QLabel('Welcome! Select difficulty and click New Game.')
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        status_font = QtGui.QFont()
        status_font.setPointSize(10)
        self.status_label.setFont(status_font)
        main_layout.addWidget(self.status_label)
    
    def new_game(self, difficulty='medium'):
        """Start a new game"""
        self.board = SudokuBoard(difficulty.lower())
        self.update_display()
        self.status_label.setText(f'New {difficulty.capitalize()} game started!')
    
    def update_display(self):
        """Update the grid display from board state"""
        for i in range(9):
            for j in range(9):
                value = self.board.get_cell(i, j)
                is_initial = self.board.is_initial_cell(i, j)
                self.cells[i][j].set_initial(is_initial)
                self.cells[i][j].set_value(value)
    
    def on_cell_changed(self, row, col, value):
        """Handle cell value change"""
        if not self.board:
            return
        
        if self.board.set_cell(row, col, value):
            # Check if puzzle is complete
            if self.board.is_complete():
                if self.board.is_correct():
                    QtWidgets.QMessageBox.information(self, 'Congratulations!', 
                                          'You solved the puzzle correctly!')
                    self.status_label.setText('Puzzle solved! Start a new game?')
                else:
                    QtWidgets.QMessageBox.warning(self, 'Incorrect', 
                                      'The puzzle is complete but has errors.')
                    self.status_label.setText('Puzzle has errors. Keep trying!')
    
    def on_new_game(self):
        """Start a new game with selected difficulty"""
        difficulty = self.difficulty_combo.currentText()
        self.new_game(difficulty)
    
    def on_hint(self):
        """Provide a hint"""
        if not self.board:
            return
        
        result = self.board.get_hint()
        if result:
            row, col = result
            self.cells[row][col].set_value(self.board.get_cell(row, col))
            self.status_label.setText(f'Hint: Filled cell at row {row+1}, column {col+1}')
        else:
            self.status_label.setText('No more hints available!')
    
    def on_check(self):
        """Check current solution"""
        if not self.board:
            return
        
        if self.board.is_complete():
            if self.board.is_correct():
                QtWidgets.QMessageBox.information(self, 'Correct!', 
                                      'Your solution is correct!')
                self.status_label.setText('Perfect! You solved it correctly!')
            else:
                QtWidgets.QMessageBox.warning(self, 'Incorrect', 
                                  'Your solution has errors.')
                self.status_label.setText('There are errors in your solution.')
        else:
            QtWidgets.QMessageBox.information(self, 'Incomplete', 
                                  'The puzzle is not yet complete.')
            self.status_label.setText('Keep going! Puzzle is not complete yet.')
    
    def on_solve(self):
        """Show the solution"""
        if not self.board:
            return
        
        reply = QtWidgets.QMessageBox.question(self, 'Solve Puzzle',
                                    'Are you sure you want to see the solution?',
                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        
        if reply == QtWidgets.QMessageBox.Yes:
            self.board.solve()
            self.update_display()
            self.status_label.setText('Solution revealed!')
    
    def on_reset(self):
        """Reset to initial puzzle state"""
        if not self.board:
            return
        
        self.board.reset()
        self.update_display()
        self.status_label.setText('Puzzle reset to initial state.')


def run():
    """Run the sudoku GUI application"""
    app = QtWidgets.QApplication(sys.argv)
    window = SudokuGUI()
    window.show()
    sys.exit(app.exec())
