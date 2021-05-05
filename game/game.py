import collections
import enum
import random
from typing import Optional, List, Set

CONVENTIONAL_BOARD_SIZE = 4


class Direction(enum.Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


CellPosition = collections.namedtuple('CellPosition', ['x', 'y'])


class Board:
    """
    Represents a square board for the 2048 game. It supports special actions like "applying force" in a given direction
        or "merging" similar cells.
    """

    def __init__(self, size: int):
        self.board = None
        self.size = size
        self.reset()

    def set_random_empty_cell(self, value: int):
        empty_cells = self.empty_cell_positions
        if len(empty_cells) == 0:
            raise ValueError('There are no empty cells in the board')

        cell = random.choice(empty_cells)
        self.set_cell_value(cell, value)

    def apply_force(self, direction: Direction) -> bool:
        """
        Applies "force" on the board. Moves all the cells towards the specified direction if possible.

        Returns True if at least one cell was moved.
        """
        cell_was_moved = False

        if direction == Direction.UP:
            cells = self.cells_positions_as_columns()
            for column in cells:
                for cell_position in column:
                    if self.is_cell_empty(cell_position):
                        continue

                    furthest_position = self.get_furthest_empty_cell(column, direction)
                    if furthest_position and furthest_position.y < cell_position.y:
                        cell_was_moved = True
                        self.move_cell(cell_position, furthest_position)

        if direction == Direction.DOWN:
            cells = self.cells_positions_as_columns()
            for column in cells:
                # Iterate over the column flipped
                for cell_position in column:
                    if self.is_cell_empty(cell_position):
                        continue

                    furthest_position = self.get_furthest_empty_cell(column, direction)
                    if furthest_position and furthest_position.y > cell_position.y:
                        cell_was_moved = True
                        self.move_cell(cell_position, furthest_position)

        if direction == Direction.RIGHT:
            cells = self.cells_positions_as_rows()
            for row in cells:
                for cell_position in row:
                    if self.is_cell_empty(cell_position):
                        continue

                    furthest_position = self.get_furthest_empty_cell(row, direction)
                    if furthest_position and furthest_position.x > cell_position.x:
                        cell_was_moved = True
                        self.move_cell(cell_position, furthest_position)

        if direction == Direction.LEFT:
            cells = self.cells_positions_as_rows()
            for row in cells:
                # Iterate over the row flipped, because we want to look
                for cell_position in row:
                    if self.is_cell_empty(cell_position):
                        continue

                    furthest_position = self.get_furthest_empty_cell(row, direction)
                    if furthest_position and furthest_position.x < cell_position.x:
                        cell_was_moved = True
                        self.move_cell(cell_position, furthest_position)

        return cell_was_moved

    def merge_cells(self, direction: Direction) -> bool:
        """
        Merges 2 adjacent cells if they posses the same value, based on the direction.
        It may be seen as though a force was applied in a specified direction and the cells which are adjacent
            and similar are "squeezed" together and become one.

        Returns True if at least one cell was merged.
        """
        cell_was_merged = False

        if direction == Direction.UP:
            cells = self.cells_positions_as_columns()
            for column in cells:
                for cell_position in column:
                    current_cell_value = self.get_cell_value(cell_position)
                    if current_cell_value is None:
                        continue

                    if cell_position.y == self.size - 1:
                        continue

                    cell_below_position = CellPosition(cell_position.x, cell_position.y + 1)
                    cell_below_value = self.get_cell_value(cell_below_position)

                    if current_cell_value == cell_below_value:
                        current_cell_value *= 2
                        self.set_cell_value(cell_position, current_cell_value)
                        self.set_cell_value(cell_below_position, None)

                        cell_was_merged = True

        if direction == Direction.DOWN:
            cells = self.cells_positions_as_columns()
            for column in cells:
                for cell_position in column:
                    current_cell_value = self.get_cell_value(cell_position)
                    if current_cell_value is None:
                        continue

                    if cell_position.y == 0:
                        continue

                    cell_below_position = CellPosition(cell_position.x, cell_position.y - 1)
                    cell_below_value = self.get_cell_value(cell_below_position)

                    if current_cell_value == cell_below_value:
                        current_cell_value *= 2
                        self.set_cell_value(cell_position, current_cell_value)
                        self.set_cell_value(cell_below_position, None)

                        cell_was_merged = True

        if direction == Direction.RIGHT:
            cells = self.cells_positions_as_rows()
            for row in cells:
                for cell_position in row:
                    current_cell_value = self.get_cell_value(cell_position)
                    if current_cell_value is None:
                        continue

                    if cell_position.x == self.size - 1:
                        continue

                    cell_below_position = CellPosition(cell_position.x + 1, cell_position.y)
                    cell_below_value = self.get_cell_value(cell_below_position)

                    if current_cell_value == cell_below_value:
                        current_cell_value *= 2
                        self.set_cell_value(cell_position, current_cell_value)
                        self.set_cell_value(cell_below_position, None)

                        cell_was_merged = True

        if direction == Direction.LEFT:
            cells = self.cells_positions_as_rows()
            for row in cells:
                for cell_position in row:
                    current_cell_value = self.get_cell_value(cell_position)
                    if current_cell_value is None:
                        continue

                    if cell_position.x == 0:
                        continue

                    cell_below_position = CellPosition(cell_position.x - 1, cell_position.y)
                    cell_below_value = self.get_cell_value(cell_below_position)

                    if current_cell_value == cell_below_value:
                        current_cell_value *= 2
                        self.set_cell_value(cell_position, current_cell_value)
                        self.set_cell_value(cell_below_position, None)

                        cell_was_merged = True

        return cell_was_merged

    def reset(self):
        self.board = []

        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(None)
            self.board.append(row)

    def is_cell_empty(self, position: CellPosition) -> bool:
        return self.board[position.y][position.x] is None

    def set_cell_value(self, position: CellPosition, number: Optional[int]):
        self.board[position.y][position.x] = number

    def get_cell_value(self, position: CellPosition) -> Optional[int]:
        return self.board[position.y][position.x]

    def move_cell(self, position: CellPosition, target_position: CellPosition):
        if not self.is_cell_empty(target_position):
            raise ValueError(f'Cannot move cell {position} to non-empty cell {target_position}')

        current_value = self.get_cell_value(position)
        self.set_cell_value(target_position, current_value)
        self.set_cell_value(position, None)

    @property
    def empty_cell_positions(self) -> List[CellPosition]:
        """
        Returns all the cell positions for empty cells.
        :return:
        """
        result = []
        for x in range(self.size):
            for y in range(self.size):
                cell_position = CellPosition(x, y)

                if self.get_cell_value(cell_position) is None:
                    result.append(cell_position)
        return result

    @property
    def unique_cell_values(self) -> Set[int]:
        """
        Returns all the values existing in the board cells.
        """
        result = set()

        for x in range(self.size):
            for y in range(self.size):
                cell_position = CellPosition(x, y)

                value = self.get_cell_value(cell_position)
                if value is not None:
                    result.add(value)

        return result

    def cells_positions_as_rows(self) -> List[CellPosition]:
        result = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                row.append(CellPosition(x, y))
            result.append(row)
        return result

    def cells_positions_as_columns(self) -> List[CellPosition]:
        result = []
        for x in range(self.size):
            row = []
            for y in range(self.size):
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
            if i != self.size - 1:
                result += "\n"
        return result


class Game2048:
    def __init__(self):
        self.board = Board(CONVENTIONAL_BOARD_SIZE)
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
        return self.is_win

    @property
    def is_win(self) -> bool:
        return 2048 in self.board.unique_cell_values

    def move(self, direction: Direction) -> bool:
        """
        Makes a game move based on the specified direction.
        Returns True if the move had any effect on the board. (Some cell moved or a merge had happened)
        """
        applied_force_had_effect = self.board.apply_force(direction)
        merge_had_effect = self.board.merge_cells(direction)
        self.board.apply_force(direction)

        move_had_any_effect = applied_force_had_effect or merge_had_effect
        if not move_had_any_effect:
            return False

        if len(self.board.empty_cell_positions) > 0:
            self.board.set_random_empty_cell(2)

        return True
