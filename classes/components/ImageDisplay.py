from pygame import Surface
from pygame.draw import rect as draw_rect

from utils.settings import Colors, Images, Fonts


class ImageDisplay:
    def __init__(
            self,
            display_surface: Surface,
            player_id: int,
            image: Surface,
            position: tuple[int, int],
            
            ) -> None:
        self.display_surface = display_surface
        self.player_id = player_id
        self.image = image
        self.position = position


    def draw(self, active: bool) -> None:
        color = Colors.active if active else Colors.passive
        self.image.get_rect(center=self.position)
        draw_rect(
            self.image,
            color,
            self.image.get_rect(),
            2
        )

        self.display_surface.blit(self.image, self.position)