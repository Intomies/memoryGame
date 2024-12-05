from pygame import init as init_game
from classes.state_machine.Engine import Engine
from classes.screens.MainMenu import MainMenu


def main() -> None:
    init_game()
    engine = Engine()
    engine.run(MainMenu(engine=engine))


if __name__ == '__main__':
    main()