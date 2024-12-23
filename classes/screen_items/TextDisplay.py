from pygame import Surface, Rect
from pygame.draw import rect as draw_rect
from pygame.font import Font

from utils.settings import Cards, Colors

class TextDisplay:
    def __init__(
            self, 
            text: str, 
            font_style: Font, 
            position: tuple[int, int]
            ) -> None:
        self.text = text
        self.font_style = font_style
        self.position = position

    # Draws basic texts on display
    def draw_static(self, display: Surface, color: str | tuple[int, int, int]) -> None:
        value: Surface = self.font_style.render(str(self.text), True, color)
        value_rect: Rect = value.get_rect(center=self.position)
        display.blit(value, value_rect)


    def draw(self, display: Surface, active: bool) -> None:
        color = Colors.active if active else Colors.passive
        value: Surface = self.font_style.render(str(self.text), True, color, Colors.border)
        value_rect: Rect = value.get_rect(center=self.position)
        draw_rect(
            value, 
            Colors.active if active else Colors.passive, 
            value.get_rect(), 
            Cards.border_width
        )
        display.blit(value, value_rect)