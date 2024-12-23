from dataclasses import dataclass
from os.path import join as os_path_join
from pygame.font import Font, SysFont


@dataclass(frozen=True)
class Animations:
    speed: float = 0.15


@dataclass(frozen=True)
class Buttons:
    x_offset_mid: float = 1.5
    y_offset_mid: float = 2.0
    x_offset_down: float = 3.0
    y_offset_down: float = 4.5
    padding_x = 200
    padding_y = 100


@dataclass(frozen=True)
class Cards:
    size: int = 160
    amount: int = 32
    border_width = 2


@dataclass(frozen=True)
class Colors:
    background: str= '#222222'
    border: str = '#111111'
    active: str = 'gold'
    passive: str = '#64661e'
    energy: str = 'blue'
    health: str = 'red'
    text: str = '#EEEEEE'
    water: str = '#71ddee'


@dataclass(frozen=True)
class Decks:
    num_columns: int = 8
    num_rows: int = 8
    padding: int = 10
    margin: int = 50


@dataclass(frozen=True)
class Games:
    points_per_pair: int = 2


@dataclass(frozen=True)
class Images:
    size_smaller: int = 40
    size_small: int = 80
    size_mid: int = 160
    size_large: int = 240


@dataclass(frozen=True)
class Mains:
    app_name: str = 'Memory Game'
    width: int = 2560
    height: int = 1440
    fps: int = 60
    surface_default_size: tuple = (64, 64)


@dataclass(frozen=True)
class Tables:
    texture_size: int = 128


@dataclass(frozen=True)
class Fonts:
    main_font_style = './utils/font/Silkscreen/Silkscreen-Regular.ttf'
    
    large_font_size = 144
    medium_font_size = 72
    small_font_size = 36
    
    padding_top = 200
    padding_bottom = 100
    y_padding = 100
    padding_buttons = 200
    
    name_length = 8

    @classmethod
    def large(self) -> Font:
        return Font(self.main_font_style, self.large_font_size)

    @classmethod
    def medium(self) -> Font:
        return Font(self.main_font_style, self.medium_font_size)
    
    @classmethod
    def small(self) -> Font:
        return Font(self.main_font_style, self.small_font_size)
        

@dataclass(frozen=True)
class Paths:
    graphics_path: str = './data/images'
    main_menu_background: str = 'main_menu'
    card_front_folder: str = 'front'
    card_back_folder: str = 'back'
    table_folder: str = 'table'
    sounds_path: str = './data/sounds'
    sounds_format: str = 'wav'

    @classmethod
    def main_menu_bg(self) -> str:
        return os_path_join(self.graphics_path, self.main_menu_background)

    @classmethod
    def card_front(self) -> str:
        return os_path_join(self.graphics_path, self.card_front_folder)
    
    @classmethod
    def card_back(self) -> str:
        return os_path_join(self.graphics_path, self.card_back_folder)
    
    @classmethod
    def table(self) -> str:
        return os_path_join(self.graphics_path, self.table_folder)
    
    @classmethod
    def sound(self, sound: str):
        return f'{os_path_join(self.sounds_path, sound)}.{self.sounds_format}'


@dataclass(frozen=True)
class Screens:
    main_menu_id = 0
    player_info_id = 1
    game_view_id = 2


@dataclass(frozen=True)
class Sounds:
    button: str = 'button'
    turn: str = 'turn'
    pair: str = 'pair'