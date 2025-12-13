import time
from constants import ROOMS
from utils import print_slow
from utils import describe_current_room
from utils import random_event
from utils import print_slow


def get_input(prompt="🎮 > "):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\n🚪 Выход из игры...")
        return "quit"


def show_inventory(game_state):
    inventory = game_state['player_inventory']
    if inventory:
        print("\n" + "═" * 50)
        print("🎒 ВАШ ИНВЕНТАРЬ:")
        print("═" * 50)
        for i, item in enumerate(inventory, 1):
            print(f"  {i}. {item}")
        print("═" * 50)
    else:
        print("\n🎒 Ваш инвентарь пуст...")


def move_player(game_state, direction):

    current_room = game_state['current_room']
    room = ROOMS[current_room]

    if direction in room['exits']:
        next_room = room['exits'][direction]

        if next_room == 'treasure_room':

            has_key = False
            for item in game_state['player_inventory']:
                if 'ключ' in str(item).lower():
                    has_key = True
                    break

            if has_key:
                print("Вы используете найденный ключ, чтобы открыть "
                      "путь в комнату сокровищ.")
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return

        game_state['current_room'] = next_room
        game_state['steps_taken'] += 1

        random_event(game_state)

        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):

    current_room = game_state['current_room']
    room = ROOMS[current_room]

    found_item = None
    for item in room['items']:
        if item_name.lower() in item.lower():
            found_item = item
            break

    if found_item:

        game_state['player_inventory'].append(found_item)

        room['items'].remove(found_item)

        print_slow(f"✨ Вы подняли: {found_item}")
        time.sleep(0.3)

        if 'факел' in found_item.lower():
            print_slow("🔥 Факел загорается, отгоняя тени...")
        elif 'ключ' in found_item.lower():
            print_slow("🗝️  Ключ холодный на ощупь...")
        elif 'книга' in found_item.lower():
            print_slow("📖 Страницы шелестят древней мудростью...")
    else:
        print_slow("Такого предмета здесь нет.")


def use_item(game_state, item_name):

    inventory = game_state['player_inventory']

    found_item = None
    for item in inventory:
        if item_name.lower() in item.lower():
            found_item = item
            break

    if not found_item:
        print_slow("У вас нет такого предмета.")
        return

    if 'факел' in found_item.lower():
        print_slow("🔥 Вы зажигаете факел! Стало светлее.")

    elif 'ключ' in found_item.lower():
        current_room = game_state['current_room']
        if (current_room == 'treasure_room' and
                'сундук' in str(ROOMS[current_room]['items']).lower()):
            print_slow("\n" + "💎" * 25)
            print_slow("🗝️  Вы вставляете ключ в замок сундука...")
            time.sleep(0.7)
            print_slow("🔓 Замок поддаётся! Сундук открывается!")
            print_slow("✨ ВЫ НАШЛИ СОКРОВИЩА! ПОБЕДА!")
            print_slow("💎" * 25)
            game_state['game_over'] = True
        else:
            print_slow(
                "🗝️  Вы вертите ключ в руках... Но здесь не к чему его применить.")

    elif 'книга' in found_item.lower():
        print_slow("📖 Вы открываете древнюю книгу...")
        time.sleep(0.5)
        print_slow("💡 На одной из страниц карта лабиринта!")

    else:
        print_slow(f"🤷 Вы не знаете, как использовать {found_item}...")
