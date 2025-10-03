# labyrinth_game/player_actions.py
def get_input(prompt="> "):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def show_inventory(game_state):
    inventory = game_state['player_inventory']
    if inventory:
        print("Инвентарь:", ", ".join(inventory))
    else:
        print("Инвентарь пуст")


def move_player(game_state, direction):
    """Переместить игрока в указанном направлении"""
    from constants import ROOMS

    current_room = game_state['current_room']
    room = ROOMS[current_room]

    # Проверяем, есть ли выход в этом направлении
    if direction in room['exits']:
        next_room = room['exits'][direction]

        # Проверка на treasure_room
        if next_room == 'treasure_room':
            if 'treasure_key' in game_state['player_inventory'] or 'rusty_key' in game_state['player_inventory']:
                print(
                    "Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return

        # Меняем комнату игрока
        game_state['current_room'] = next_room
        game_state['steps_taken'] += 1

        # Случайное событие
        from utils import random_event
        random_event(game_state)

        # Показываем новую комнату
        from utils import describe_current_room
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    """Взять предмет из комнаты"""
    from constants import ROOMS

    current_room = game_state['current_room']
    room = ROOMS[current_room]

    if item_name in room['items']:
        # Добавляем в инвентарь
        game_state['player_inventory'].append(item_name)
        # Убираем из комнаты
        room['items'].remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    """Использовать предмет из инвентаря"""
    inventory = game_state['player_inventory']

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    if item_name == 'torch':
        print("Вы зажигаете факел. Стало светлее.")
    elif item_name == 'sword':
        print("Вы чувствуете уверенность с мечом в руках.")
    elif item_name == 'bronze box':
        if 'rusty_key' not in inventory:
            print("Вы открываете бронзовую шкатулку и находите внутри rusty_key!")
            inventory.append('rusty_key')
        else:
            print("Шкатулка пуста.")
    elif item_name == 'treasure_key' or item_name == 'rusty_key':
        from constants import ROOMS
        current_room = game_state['current_room']
        if current_room == 'treasure_room' and 'treasure chest' in ROOMS[current_room]['items']:
            print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
            print("В сундуке сокровище! Вы победили!")
            game_state['game_over'] = True
        else:
            print("Здесь не к чему применить этот ключ.")
    else:
        print(f"Вы не знаете, как использовать {item_name}.")
