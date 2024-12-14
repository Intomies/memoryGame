from typing import Optional
from pygame import Surface

from classes.screen_items.ImageDisplay import ImageDisplay
from classes.screen_items.TextDisplay import TextDisplay
from utils.settings import Games, Fonts


class Player:
    def __init__(
            self,
            id: int,
            name: str,
            image: Optional[Surface] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.image = image
        self.score: int = 0
        self.active = False
        self.turns = 0

        self.display_surface = None
        self.name_display: Optional[TextDisplay] = None
        self.score_display: Optional[TextDisplay] = None
        self.image_display: Optional[ImageDisplay] = None

    
    def add_points(self):
        self.score += Games.points_per_pair
        self.__set_score_display()


    def set_display_surface(self, display_surface: Surface) -> None:
        self.display_surface = display_surface


    def set_view(self, display_surface: Surface) -> None:
        self.display_surface = display_surface
        self.__set_image_display()
        self.__set_name_display()
        self.__set_score_display()


    def __set_image_display(self) -> None:
        view_x_pos = self.__get_view_x_position()
        pos_x = view_x_pos - self.image.get_width() // 2
        pos_y = Fonts.padding_bottom

        self.image_display = ImageDisplay(
            display_surface=self.display_surface,
            player_id=self.id,
            image=self.image,
            position=(pos_x, pos_y)
        )


    def __set_name_display(self) -> None:
        pos_x = self.__get_view_x_position()
        pos_y = self.image.get_height() + Fonts.padding_top
        self.name_display = TextDisplay(
            text=self.name,
            font_style=Fonts.medium(),
            position=(pos_x, pos_y)
        )

    
    def __set_score_display(self) -> None:
        pos_x = self.__get_view_x_position()
        pos_y = self.image.get_height() + Fonts.padding_top + Fonts.padding_bottom
        self.score_display = TextDisplay(
            text=f'Score: {self.score}',
            font_style=Fonts.medium(),
            position=(pos_x, pos_y)
        )


    def __get_view_x_position(self) -> int:
        screen_width = self.display_surface.get_width()
        player_1_name_pos_x: tuple = screen_width // 8
        player_2_name_pos_x: tuple = screen_width - (screen_width // 8)
        
        match self.id:
            case 0: return player_1_name_pos_x
            case 1: return player_2_name_pos_x
            case _: return (0, 0)