from typing import Callable, Optional
from pygame import Surface
from pygame.draw import rect as draw_rect
from pygame.font import Font
from pygame.rect import Rect

from utils.settings import Cards, Colors


class Button:
    def __init__(
            self,
            id: int,
            text: str,
            position: tuple[int, int], 
            font_style: Font, 
            active_color: str = Colors.active,
            passive_color: str = Colors.passive,
            border_visible: bool = False
            ) -> None:
        
        self.id = id
        self.text = text
        self.position = position
        self.font_style = font_style
        self.active_color = active_color
        self.passive_color = passive_color
        self.border_visible = border_visible
        
        self.active: bool = False
        self.rect: Optional[Rect] = None

    
    def set_clickable_active(self, get_active: Callable) -> None:
        self.active = get_active().id == self.id

    
    def set_active(self, value: bool):
        self.active = value


    def draw_clickable(self, display: Surface, get_active: Callable) -> Surface:
        self.active = get_active().id == self.id
        color = self.active_color if self.active else self.passive_color
        value: Surface = self.font_style.render(str(self.text), True, color)
        self.rect: Rect = value.get_rect(center=self.position)

        if self.border_visible: 
            draw_rect(
            value, 
            color, 
            value.get_rect(), 
            Cards.border_width
        )

        display.blit(value, self.rect)


    def draw_hoverable(self, display: Surface) -> Surface:
        color = self.active_color if self.active else self.passive_color
        value: Surface = self.font_style.render(str(self.text), True, color)
        self.rect: Rect = value.get_rect(center=self.position)
        display.blit(value, self.rect)
        

    def draw_basic(self, display: Surface, color: str = Colors.active) -> None:
        value: Surface = self.font_style.render(str(self.text), True, color)
        value_rect: Rect = value.get_rect(center=self.position)

        self.rect = value_rect

        display.blit(value, value_rect)