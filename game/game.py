import collections
import enum
import random
from typing import Optional, List

BOARD_SIZE = 4


class Direction(enum.Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


CellPosition = collections.namedtuple('CellPosition', ['x', 'y'])


class Board:
    def __init__(self):
        self.board = None
        self.reset()

    def apply_force(self, direction: Direction):
        pass

    def merge_cells(self, direction: Direction):
        pass

    def reset(self):
        self.board = []

        for i in range(BOARD_SIZE):
            self.board.append([None, None, None, None])

    def set_cell(self, position: CellPosition, number: Optional[int]):
        self.board[position.y][position.x] = number

    def get_cell(self, position: CellPosition) -> Optional[int]:
        return self.board[position.y][position.x]

    @property
    def empty_cells(self) -> List[CellPosition]:
        for cell_position in self.all_cells:
            if self.get_cell(cell_position) is None:
                yield cell_position

    @property
    def all_cells(self):
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                yield CellPosition(x, y)

    def get_cells_as_rows(self):
        result = []
        for y in range(BOARD_SIZE):
            row = []
            for x in range(BOARD_SIZE):
                row.append(CellPosition(x, y))
            result.append(row)
        return result

    def get_cells_as_columns(self):
        result = []
        for x in range(BOARD_SIZE):
            row = []
            for y in range(BOARD_SIZE):
                row.append(CellPosition(x, y))
            result.append(row)
        return result

    def __str__(self):
        result = ""
        for i, row in enumerate(self.board):
            for number in row:
                if number is None:
                    result += "X"
                else:
                    result += str(number)
                result += " "
            if i != BOARD_SIZE - 1:
                result += "\n"
        return result


class Game2048:
    def __init__(self):
        self.board = Board()
        self.reset()

    def reset(self):
        self.board.reset()

        empty_cells = list(self.board.empty_cells)
        initial_cells = random.choices(empty_cells, k=2)

        for cell in initial_cells:
            self.board.set_cell(cell, 2)

    @property
    def is_over(self) -> bool:
        """
        Returns True if the game is over.
        """
        return False

    def move(self, direction: Direction):
        self.board.apply_force(direction)
        self.board.merge_cells(direction)
