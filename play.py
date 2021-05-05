from game.game import Game2048

game = Game2048()

while not game.is_over:
    direction = input('Enter direction (W/A/S/D): ')
    print(str(game.board))

