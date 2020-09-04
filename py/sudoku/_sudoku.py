





def generate_board():
    # Generate full, randomized sudoku board
    pass

def generate_section():
    # generate a randomized, 3x3 seciont of the board
    pass


class SudokuBoard(object):
    """

    """
    def __init__(self, difficulty):
        super().__init__()
        self._base_size = 3
        self._board_length = self._base_size ** 2
        self._difficulty = None
        self.difficulty = difficulty
        self._max_solves = None

    @property
    def difficulty(self):
        """(int) Higher levels will provide fewer numbers on the board"""
        return self._difficulty

    @difficulty.setter
    def difficulty(self, difficulty):
        if difficulty < 0 or difficulty > 10:
            raise ValueError("difficulty must be an integer between 0 and 10")
        # TODO: This is no good
        max_grids = self._board_length ** 2
        min_provided = 17 # The theoretical minimum to solve the board
        self._max_solves = int((max_grids - min_provided) * .01 * difficulty)
        self._difficulty
