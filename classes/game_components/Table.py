from pygame import Surface

from utils.settings import Tables, Mains


class Table:
    def __init__(
            self, 
            img: Surface,
            display_surface: Surface,
            ) -> None:
        self.display_surface: Surface = display_surface
        self.img = img

    
    def draw(self) -> None:
        for y in range(0, Mains.height, Tables.texture_size):
            for x in range(0, Mains.width, Tables.texture_size):
                self.display_surface.blit(self.img, (x, y))
