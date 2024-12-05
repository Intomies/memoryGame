from classes.State import State


class Machine:
    def __init__(self):
        self.current_state: State = None
        self.previous_state: State = None
        self.next_state: State = None

    def update(self):
        if self.next_state:
            self.previous_state = self.current_state
            self.current_state = self.next_state
            self.next_state = None

    
    def previous(self) -> None:
        self.current_state = self.previous_state
        self.next_state = None