from typing import List
from pygame import (
    FULLSCREEN,
    Surface,
    QUIT,
    quit,
    K_ESCAPE
    )

from pygame.display import flip, set_caption, set_mode
    
from pygame.event import Event, get as get_event
from pygame.key import get_pressed, ScancodeWrapper
from pygame.mixer import init as init_mixer
from pygame.time import Clock
from sys import exit

from classes.state_machine.Machine import Machine
from classes.state_machine.State import State
from utils.settings import Mains, Colors


class Engine:
    def __init__(self):
        self.screen: Surface = set_mode((0,0), FULLSCREEN)
        self.clock: Clock = Clock()
        self.fps: int = Mains.fps

        self.machine = Machine()
        self.background_color = Colors.background
    
        set_caption(Mains.app_name)
        init_mixer()

    def loop(self):
        while True:
            self.machine.update()
            event_list: List[Event] = get_event()
            keys: ScancodeWrapper = get_pressed()
            
            for event in event_list:
                if event.type == QUIT or keys[K_ESCAPE]:
                    self.exit_game()
                else:
                    self.machine.current_state.handle_event(event=event, keys=keys)
                    
            self.screen.fill(self.background_color)

            self.machine.current_state.run()
            
            flip()
            self.clock.tick(self.fps)

    def exit_game(self) -> None:
        quit()
        exit()

    def run(self, state: State) -> None:
        self.machine.current_state = state
        self.loop()
    