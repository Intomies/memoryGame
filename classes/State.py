from pygame.event import Event
from pygame.key import (
    ScancodeWrapper
    )

class State():
    def __init__(self, engine) -> None:
        self.engine = engine
    
    def run(self): pass
    def handle_event(self, event: Event, keys: ScancodeWrapper): pass 