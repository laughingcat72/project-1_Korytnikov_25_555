import math
import sys
import time


from constants import COMMANDS, EVENT_ART, ROOMS

EVENT_PROBABILITY = 10
TRAP_DAMAGE_CHANCE = 3
EVENT_TYPES = 4
SIN_MULTIPLIER = 12.9898
RANDOM_MULTIPLIER = 43758.5453


def print_slow(text, delay=0.03):

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def describe_current_room(game_state):
    current_room = game_state['current_room']
    room = ROOMS[current_room]

    print("\n" * 3)

    print(room['art'])

    print(f"\n📍 ВЫ В: {current_room.upper()}")
    print("═" * 60)
    print_slow(f"📖 {room['description']}")
    print()

    if room['items']:
        print("✨ ЗАМЕТНЫЕ ПРЕДМЕТЫ:")
        for item in room['items']:
            print(f"   • {item}")
        print()

    if room['exits']:
        print("🚪 ВЫХОДЫ:")
        for direction, target in room['exits'].items():
            direction_icons = {'north': '⬆️ ',
                               'south': '⬇️ ', 'east': '➡️ ', 'west': '⬅️ '}
            print(
                f"   {direction_icons.get(direction, '•')} {direction} → {target}")
        print()

    if room['puzzle']:
        print("❓ Здесь есть ЗАГАДКА (используйте команду 'solve')")
        print("═" * 60)


def show_help():
    """Показать справку по командам"""
    print("\n" + "🆘 ПОМОЩЬ 🆘".center(50))
    print("═" * 50)
    print("📋 Доступные команды:")
    print("-" * 50)
    for command, description in COMMANDS.items():
        print(f"  {command:<20} - {description}")
    print("═" * 50)
    print("\n💡 Совет: Пробуйте разные команды и исследуйте каждую комнату!")
    print("   Некоторые предметы могут быть очень полезны...")


def pseudo_random(seed, modulo):
    x = math.sin(seed * SIN_MULTIPLIER) * RANDOM_MULTIPLIER
    fractional = x - math.floor(x)
    return int(fractional * modulo)


def trigger_trap(game_state):
    print("\n" + EVENT_ART['trap'])
    time.sleep(1)

    print_slow("💥 ЗЕМЛЯ ДРОЖИТ ПОД НОГАМИ!")
    time.sleep(0.5)
    print_slow("🪨 КАМНИ СКРЕЖЕТАЯ СМЕЩАЮТСЯ!")
    time.sleep(0.7)

    inventory = game_state['player_inventory']

    if inventory:

        item_index = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(item_index)
        print_slow(f"💔 В суматохе вы теряете: {lost_item}!")
        time.sleep(0.5)
        print_slow("😱 Придётся быть осторожнее...")
    else:

        chance = pseudo_random(game_state['steps_taken'], EVENT_PROBABILITY)
        if chance < TRAP_DAMAGE_CHANCE:
            print_slow("⚠️  ВАШЕ РАВНОВЕСИЕ ПОТЕРЯНО!")
            time.sleep(0.7)
            print_slow("😵 ВЫ ПАДАЕТЕ В ТЁМНУЮ БЕЗДНУ...")
            time.sleep(1)
            print_slow("\n💀 ИГРА ОКОНЧЕНА")
            game_state['game_over'] = True
        else:
            print_slow("🙏 ЧУДОМ ВАМ УДАЛОСЬ УДЕРЖАТЬСЯ!")
            time.sleep(0.5)
            print_slow("😅 Это было близко...")


def random_event(game_state):

    if pseudo_random(game_state['steps_taken'], EVENT_PROBABILITY) == 0:
        event_type = pseudo_random(game_state['steps_taken'] + 1, EVENT_TYPES)

        if event_type == 0:

            print("\n" + EVENT_ART['coin'])
            print_slow("✨ Что-то блеснуло под ногами...")
            time.sleep(0.3)
            print_slow("💰 Вы нашли древнюю золотую монету!")

            current_room = game_state['current_room']
            if 'монет' not in str(ROOMS[current_room]['items']).lower():
                ROOMS[current_room]['items'].append('💰 Золотая монета')

        elif event_type == 1:

            print("\n" + EVENT_ART['monster'])
            print_slow("👂 Вы слышите странный шорох из темноты...")
            time.sleep(0.7)
            if 'меч' in str(game_state['player_inventory']).lower():
                print_slow("⚔️  Вы хватаетесь за меч!")
                time.sleep(0.3)
                print_slow("👹 Шорох мгновенно прекращается...")
            else:
                print_slow("😨 Вы замираете от страха...")
                time.sleep(0.5)
                print_slow("👻 Похоже, это была лишь игра воображения...")

        elif event_type == 2:

            current_room = game_state['current_room']

            if (current_room == 'trap_room' and
                    'факел' not in str(game_state['player_inventory']).lower()):
                print_slow("🌑 В темноте вы не разглядели коварную плиту!")
                trigger_trap(game_state)

        elif event_type == 3:

            print_slow("\n💭 Внезапно к вам приходит озарение...")
            time.sleep(0.5)
            print_slow(
                "🧠 'Загадки в этом лабиринте часто имеют несколько ответов'")
            time.sleep(0.5)
            print_slow("💡 'Попробуйте разные варианты...'")


def solve_puzzle(game_state):

    current_room = game_state['current_room']
    room = ROOMS[current_room]

    if not room['puzzle']:
        print_slow("🤔 Вы осматриваетесь... Кажется, здесь нет загадок.")
        return

    question, answer = room['puzzle']
    print_slow("\n" + "❓ ЗАГАДКА ❓".center(50))
    print("═" * 50)
    print_slow(f"{question}")
    print("═" * 50)

    user_answer = input("\n🎯 Ваш ответ: ").strip().lower()

    if not user_answer:
        print_slow("🤐 Вы остаётесь в молчании...")
        return

    correct_answers = [answer.lower()]

    if answer == '10':
        correct_answers.extend(['десять', '10', 'ten', 'десятка'])
    elif answer == 'шаг шаг шаг':
        correct_answers.extend(['шагшагшаг', 'step step step', 'stepstepstep'])

    if user_answer in correct_answers:
        print_slow("\n" + "✅ ПРАВИЛЬНО! ✅".center(50))
        time.sleep(0.5)
        print_slow("✨ Загадка решена! Магия рассеивается...")
        time.sleep(0.3)

        if current_room == 'hall':
            game_state['player_inventory'].append(
                '🗝️ Золотой ключ от сокровищницы')
            print_slow("🗝️  Вы получаете: ЗОЛОТОЙ КЛЮЧ ОТ СОКРОВИЩНИЦЫ!")
        elif current_room == 'trap_room':
            game_state['player_inventory'].append(
                '🗝️ Ржавый ключ с таинственными узорами')
            print_slow("🗝️  Вы получаете: РЖАВЫЙ КЛЮЧ С ТАИНСТВЕННЫМИ УЗОРАМИ!")

        room['puzzle'] = None
        time.sleep(0.7)

    else:
        print_slow("\n" + "❌ НЕВЕРНО ❌".center(50))
        print_slow("😞 Эта догадка оказалась ошибочной...")

        if current_room == 'trap_room':
            time.sleep(0.5)
            print_slow("⚠️  Загадка была защищена ловушкой!")
            trigger_trap(game_state)


def attempt_open_treasure(game_state):

    current_room = game_state['current_room']
    room = ROOMS[current_room]

    print_slow("\n" + "🎁 СОКРОВИЩНЫЙ СУНДУК 🎁".center(50))
    print("═" * 50)

    if 'сундук' in str(room['items']).lower():
        if any('ключ' in item.lower() for item in game_state['player_inventory']):
            key_item = next(
                (item for item in game_state['player_inventory']
                 if 'ключ' in item.lower()),
                None)

            print_slow(f"🗝️  Вы достаёте {key_item}...")
            time.sleep(0.7)
            print_slow("🔑 Медленно вставляете его в замочную скважину...")
            time.sleep(1)
            print_slow("🔓 *ЩЁЛК!* Замок поддаётся!")
            time.sleep(0.5)

            print("\n" + EVENT_ART['treasure'])
            time.sleep(1)

            print_slow("\n" + "✨" * 25)
            print_slow("🌟 СУНДУК ОТКРЫВАЕТСЯ С ОСЛЕПИТЕЛЬНЫМ БЛЕСКОМ!")
            print_slow(
                f"🏆 {game_state['player_name'].upper()}, ВЫ СТАЛИ ЛЕГЕНДОЙ!")
            print_slow("💰 Горы золота, драгоценные камни и древние артефакты!")
            print_slow("👑 ВАША ПОБЕДА ВЕЧНА!")
            print_slow("✨" * 25)

            game_state['game_over'] = True
        else:
            print_slow("🔒 Сундук заперт на массивный амбарный замок.")
            print_slow(
                "🔍 Нужен особый ключ... Похоже, придётся поискать его в лабиринте!")
    else:
        print_slow("👀 Странно... Вы помните, что здесь был сундук...")
