from pygame import Rect, Surface
from pygame.mixer import Sound

from utils.settings import Paths, Sounds

class Card:
    def __init__(
            self, 
            id: tuple, 
            front_img: Surface, 
            back_img: Surface,
            ) -> None:
        self.front_img = front_img
        self.back_img = back_img

        self.id = id
        self.found_pair: bool = False
        self.selected_img: Surface = self.back_img if not self.found_pair else self.front_img
        self.rect: Rect = self.selected_img.get_rect()
        self.sound = Sound(Paths.sound(Sounds.turn))
        
    def turn(self):
        self.sound.play()
        self.selected_img = self.front_img if self.selected_img != self.front_img else self.back_img