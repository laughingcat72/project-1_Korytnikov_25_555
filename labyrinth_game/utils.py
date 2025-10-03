# labyrinth_game/utils.py
import math
from constants import ROOMS


def describe_current_room(game_state):
    current_room = game_state['current_room']
    room = ROOMS[current_room]

    print(f"\n== {current_room.upper()} ==")
    print(room['description'])

    if room['items']:
        print("Заметные предметы:", ", ".join(room['items']))

    if room['exits']:
        exits = [f"{direction} -> {target}" for direction,
                 target in room['exits'].items()]
        print("Выходы:", ", ".join(exits))

    if room['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def show_help():
    """Показать справку по командам"""
    from constants import COMMANDS
    print("\nДоступные команды:")
    for command, description in COMMANDS.items():
        print(f"  {command:<16} - {description}")


def pseudo_random(seed, modulo):
    """Псевдослучайный генератор на основе синуса"""
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional = x - math.floor(x)
    return int(fractional * modulo)


def trigger_trap(game_state):
    """Активация ловушки"""
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state['player_inventory']

    if inventory:
        # Выбираем случайный предмет для удаления
        item_index = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(item_index)
        print(f"Вы потеряли: {lost_item}!")
    else:
        # Игрок получает "урон"
        chance = pseudo_random(game_state['steps_taken'], 10)
        if chance < 3:
            print("Вы не смогли удержаться и упали в пропасть! Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вам чудом удалось удержаться!")


def random_event(game_state):
    """Случайные события при перемещении"""
    # 10% шанс события
    if pseudo_random(game_state['steps_taken'], 10) == 0:
        event_type = pseudo_random(game_state['steps_taken'] + 1, 3)

        if event_type == 0:
            # Находка
            print("Вы заметили блестящую монетку на полу!")
            from constants import ROOMS
            current_room = game_state['current_room']
            if 'coin' not in ROOMS[current_room]['items']:
                ROOMS[current_room]['items'].append('coin')

        elif event_type == 1:
            # Испуг
            print("Вы слышите странный шорох в темноте...")
            if 'sword' in game_state['player_inventory']:
                print("Вы достаёте меч, и шорох мгновенно прекращается.")

        elif event_type == 2:
            # Ловушка
            current_room = game_state['current_room']
            if current_room == 'trap_room' and 'torch' not in game_state['player_inventory']:
                print("В темноте вы не заметили ловушку!")
                trigger_trap(game_state)


def solve_puzzle(game_state):
    """Решить загадку в текущей комнате"""
    from constants import ROOMS

    current_room = game_state['current_room']
    room = ROOMS[current_room]

    if not room['puzzle']:
        print("Загадок здесь нет.")
        return

    question, answer = room['puzzle']
    print(f"\n{question}")
    user_answer = input("Ваш ответ: ").strip().lower()

    # Если игрок просто нажал Enter, выходим
    if not user_answer:
        return
    # Проверяем ответ (с альтернативными вариантами)
    if user_answer in [answer, 'десять', '10']:  # Принимаем разные варианты
        print("Верно! Загадка решена!")

        # Даём награду в зависимости от комнаты
        if current_room == 'hall':
            game_state['player_inventory'].append('treasure_key')
            print("Вы получаете: treasure_key")
        elif current_room == 'trap_room':
            game_state['player_inventory'].append('rusty_key')
            print("Вы получаете: rusty_key")

        # Убираем загадку
        room['puzzle'] = None
    else:
        print("Неверно. Попробуйте снова.")
        # В trap_room неверный ответ активирует ловушку
        if current_room == 'trap_room':
            trigger_trap(game_state)
