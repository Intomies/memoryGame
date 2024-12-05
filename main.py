from pygame import init as init_game
from classes.Engine import Engine
from classes.MemoryGame import MemoryGame
from classes.MainMenu import MainMenu


def main() -> None:
    init_game()
    engine = Engine()
    engine.run(MainMenu(engine=engine))


if __name__ == '__main__':
    main()