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

    def set_random_empty_cell(self, value: int):
        # Handle edge case when there is no empty cells
        cell = random.choice(self.empty_cells)
        self.set_cell(cell, value)

    def apply_force(self, direction: Direction):
        """
        Applies "force" on the board. Moves all the cells towards the specified direction if possible.
        """
        if direction == Direction.UP:
            cells = self.cells_as_columns()
            for column in cells:
                for cell_position in column:
                    if self.is_cell_empty(cell_position):
                        continue

                    furthest_position = self.get_furthest_empty_cell(column, direction)
                    if furthest_position and furthest_position.y < cell_position.y:
                        self.move_cell(cell_position, furthest_position)

        if direction == Direction.DOWN:
            cells = self.cells_as_columns()
            for column in cells:
                # Iterate over the column flipped
                for cell_position in column[::-1]:
                    if self.is_cell_empty(cell_position):
                        continue

                    furthest_position = self.get_furthest_empty_cell(column, direction)
                    if furthest_position and furthest_position.y > cell_position.y:
                        self.move_cell(cell_position, furthest_position)

        if direction == Direction.RIGHT:
            cells = self.cells_as_rows()
            for row in cells:
                for cell_position in row:
                    if self.is_cell_empty(cell_position):
                        continue

                    furthest_position = self.get_furthest_empty_cell(row, direction)
                    if furthest_position and furthest_position.x > cell_position.x:
                        self.move_cell(cell_position, furthest_position)

        if direction == Direction.LEFT:
            cells = self.cells_as_rows()
            for row in cells:
                # Iterate over the row flipped, starting from the first entry
                for cell_position in row[::-1]:
                    if self.is_cell_empty(cell_position):
                        continue

                    furthest_position = self.get_furthest_empty_cell(row, direction)
                    if furthest_position and furthest_position.x < cell_position.x:
                        self.move_cell(cell_position, furthest_position)

    def merge_cells(self, direction: Direction):
        pass

    def reset(self):
        self.board = []

        for i in range(BOARD_SIZE):
            self.board.append([None, None, None, None])

    def is_cell_empty(self, position: CellPosition) -> bool:
        return self.board[position.y][position.x] is None

    def set_cell(self, position: CellPosition, number: Optional[int]):
        self.board[position.y][position.x] = number

    def get_cell(self, position: CellPosition) -> Optional[int]:
        return self.board[position.y][position.x]

    def move_cell(self, position: CellPosition, target_position: CellPosition):
        if not self.is_cell_empty(target_position):
            raise ValueError(f'Cannot move cell {position} to non-empty cell {target_position}')

        current_value = self.get_cell(position)
        self.set_cell(target_position, current_value)
        self.set_cell(position, None)

    @property
    def empty_cells(self) -> List[CellPosition]:
        result = []
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                cell_position = CellPosition(x, y)

                if self.get_cell(cell_position) is None:
                    result.append(cell_position)
        return result

    def cells_as_rows(self) -> List[CellPosition]:
        result = []
        for y in range(BOARD_SIZE):
            row = []
            for x in range(BOARD_SIZE):
                row.append(CellPosition(x, y))
            result.append(row)
        return result

    def cells_as_columns(self) -> List[CellPosition]:
        result = []
        for x in range(BOARD_SIZE):
            row = []
            for y in range(BOARD_SIZE):
                row.append(CellPosition(x, y))
            result.append(row)
        return result

    def get_furthest_empty_cell(self, cells: List[CellPosition], direction: Direction) -> Optional[CellPosition]:
        """
        Given a cell position array and a direction, returns the "furthest" cell based on the direction.
        For example, if direction is UP - will return the empty cell with the lowest y position.
        """
        furthest_empty_cell = None

        for cell_position in cells:
            if self.is_cell_empty(cell_position):
                if furthest_empty_cell is None:
                    furthest_empty_cell = cell_position
                elif ((direction == Direction.UP and furthest_empty_cell.y > cell_position.y)
                      or (direction == Direction.DOWN and furthest_empty_cell.y < cell_position.y)
                      or (direction == Direction.RIGHT and furthest_empty_cell.x < cell_position.x)
                      or (direction == Direction.LEFT and furthest_empty_cell.x > cell_position.x)):
                    furthest_empty_cell = cell_position

        return furthest_empty_cell

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

        # Initialize 2 random cells to "2" value.
        for i in range(2):
            self.board.set_random_empty_cell(2)

    @property
    def is_over(self) -> bool:
        """
        Returns True if the game is over.
        """
        return False

    def move(self, direction: Direction):
        self.board.apply_force(direction)
        self.board.merge_cells(direction)
        self.board.apply_force(direction)
