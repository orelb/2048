from game.game import Game2048, Direction

game = Game2048()


def convert_string_to_direction(direction_str: str) -> Direction:
    direction_str = direction_str.lower()

    if direction_str == 'w':
        return Direction.UP
    if direction_str == 's':
        return Direction.DOWN
    if direction_str == 'd':
        return Direction.RIGHT
    if direction_str == 'a':
        return Direction.LEFT

    raise ValueError(f'Invalid direction string: {direction_str}')


print(str(game.board))
while not game.is_over:
    direction_input = input('Enter direction (W/A/S/D): ')

    try:
        direction = convert_string_to_direction(direction_input)
    except ValueError:
        print('Invalid input. Please try again.')
        continue

    move_had_effect = game.move(direction)
    if not move_had_effect:
        print('Illegal move. Please try again.')

    print(str(game.board))
