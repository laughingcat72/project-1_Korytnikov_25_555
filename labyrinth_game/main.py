#!/usr/bin/env python3

def process_command(game_state, command):
    """Обработать команду игрока"""
    parts = command.split()

    if not parts:
        return

    # Обработка односложных команд движения
    direction_commands = ['north', 'south', 'east', 'west']
    if parts[0] in direction_commands:
        move_player(game_state, parts[0])
        return

    if parts[0] == 'go' and len(parts) > 1:
        move_player(game_state, parts[1])
    elif parts[0] == 'take' and len(parts) > 1:
        take_item(game_state, ' '.join(parts[1:]))
    elif parts[0] == 'use' and len(parts) > 1:
        use_item(game_state, ' '.join(parts[1:]))
    elif command == 'look':
        describe_current_room(game_state)
    elif command == 'inventory':
        show_inventory(game_state)
    elif command == 'solve':
        solve_puzzle(game_state)
    elif command == 'help':
        show_help()
    elif command == 'quit':
        game_state['game_over'] = True
    else:
        print("Неизвестная команда. Введите 'help' для списка команд.")


def main():
    print("Добро пожаловать в Лабиринт сокровищ!")

    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0
    }

    from utils import describe_current_room
    describe_current_room(game_state)

    from player_actions import get_input

    while not game_state['game_over']:
        command = get_input().strip().lower()

        if command == 'quit':
            break

        process_command(game_state, command)


if __name__ == "__main__":
    main()
