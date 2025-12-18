import time

from player_actions import get_input, move_player, show_inventory, take_item, use_item
from utils import (attempt_open_treasure, describe_current_room,
                   print_slow, show_help, solve_puzzle)


def print_header():

    header = r"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║        🏰  𝕷𝖆𝖇𝖎𝖗𝖎𝖓𝖙𝖍  𝖔𝖋  𝕸𝖞𝖘𝖙𝖊𝖗𝖎𝖊𝖘  🏰                                    ║
║        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                     ║
║        Потерянные сокровища древних королей ждут своего                   ║
║        храбреца. Осмелитесь ли вы пройти через лабиринт                   ║
║        полный загадок, ловушек и древней магии?                           ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """
    print(header)
    time.sleep(1)


def print_footer():
    """Красивое окончание игры"""
    footer = r"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║        ⭐ Спасибо за игру! ⭐                                            ║
║        Надеемся, вам понравилось это приключение!                         ║
║        Лабиринт будет ждать следующего смельчака...                       ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """
    print(footer)


def process_command(game_state, command):
    parts = command.split()

    if not parts:
        return

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

        if game_state['current_room'] == 'treasure_room':
            attempt_open_treasure(game_state)
        else:
            solve_puzzle(game_state)
    elif command == 'help':
        show_help()
    elif command == 'quit':
        print_slow("\nВы решаете покинуть лабиринт...")
        game_state['game_over'] = True
    else:
        print("Неизвестная команда. Введите 'help' для списка команд.")


def main():
    print_header()
    time.sleep(1)

    print_slow("\n🌙 Ночь опустилась на древние земли...")
    time.sleep(0.5)
    print_slow("🚶 Вы стоите перед входом в легендарный Лабиринт...")
    time.sleep(0.5)
    print_slow("💭 Судьба сокровищ теперь в ваших руках...")
    time.sleep(1)

    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0,
        'player_name': input("\n🗣️  Как вас зовут, смельчак? ")
    }

    print_slow(f"\n✨ Добро пожаловать, {game_state['player_name']}! ✨")
    print_slow("Судьба сокровищ теперь в ваших руках...")
    time.sleep(1)

    describe_current_room(game_state)

    while not game_state['game_over']:
        try:
            command = get_input(
                f"\n🎮 {game_state['player_name']} > ").strip().lower()

            if command == 'quit':
                break

            process_command(game_state, command)

        except KeyboardInterrupt:
            print_slow("\n\n🚪 Выход из игры...")
            break

    print_footer()
    time.sleep(2)


if __name__ == "__main__":
    main()
