import enum
import random

BOARD_SIZE = 4


class Direction(enum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


class Board:
    def __init__(self):
        self.board = None
        self._init_board()

    def _init_board(self):
        self.board = []

        for i in range(BOARD_SIZE):
            self.board.append([None, None, None, None])


class Game2048:
    def __init__(self):
        self.board = None

    def reset(self):
        self.board = []

        for i in range(BOARD_SIZE):
            self.board.append([None, None, None, None])

    def move(self, direction: Direction):
        pass
