Установка:
bash
make install
# или
poetry install
Запуск игры:
bash
make project
# или
poetry run python labyrinth_game/main.py
Проверка кода:
bash
make lint
🎮 Управление
Команда	Описание
north/south/east/west	Движение
look	Осмотреть комнату
take <предмет>	Взять предмет
use <предмет>	Использовать предмет
inventory	Инвентарь
solve	Решить загадку
help	Помощь
quit	Выход
🏆 Как победить
Возьми факел в entrance

Реши загадку в hall или trap_room

Получи ключ

Иди в treasure_room

Открой сундук с помощью ключа

📁 Структура проекта
text
labyrinth_game/
├── main.py          # Игровой цикл
├── constants.py     # Комнаты и команды
├── player_actions.py # Действия игрока
└── utils.py         # Вспомогательные функции




🎥 Демо


Запись демонстрационного прохождения