install:
    poetry install

project:
    poetry run python labyrinth_game/main.py

lint:
    poetry run ruff check .

build:
    poetry build