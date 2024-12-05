from dataclasses import dataclass
from random import choice, randint, randrange
from pygame import BLEND_RGBA_MULT, MOUSEMOTION, MOUSEBUTTONDOWN, Surface
from pygame.draw import rect as draw_rect
from pygame.event import Event
from pygame.key import ScancodeWrapper
from pygame.rect import Rect
from pygame.transform import scale
from typing import Callable, Dict, List, Optional

from classes.components.Button import Button
from classes.state_machine.Engine import Engine
from classes.screens.PlayerSetup import PlayerSetup
from classes.state_machine.State import State
from classes.components.Table import Table
from classes.components.TextDisplay import TextDisplay
from utils.settings import Buttons, Colors, Images, Mains, Paths, Screens, Tables, Fonts
from utils.support import get_graphics_images_from_folder
from time import time_ns

@dataclass
class BackgroundItem:
    id: int
    pic: Surface
    rect: Rect
    size: int
    speed: float


class MainMenu(State):
    def __init__(self, engine: Engine):
        super().__init__(engine=engine)

        self.id: int = Screens.main_menu_id
        self.game_name: str = Mains.app_name
        self.display_surface: Surface = self.engine.screen
        self.screen_width: int = self.display_surface.get_width()
        self.screen_height: int = self.display_surface.get_height()

        self.table: Optional[Table] = None
        self.headline: Optional[TextDisplay] = None
        self.button_1_player: Optional[Button] = None
        self.button_2_players: Optional[Button] = None
        self.button_start: Optional[Button] = None
        self.button_quit: Optional[Button] = None
        
        self.hover_buttons: list[Button] = []
        self.selection_buttons: list[Button] = []
        self.button_actions: dict[Button, Callable] = None

        self.active_button: Optional[Button] = None
        
        self.animation_images: Optional[list[Surface]] = None
        self.max_active_animations: int = 55
        self.active_animation_images: list[BackgroundItem] = []
        self.animation_started: bool = False


        self.init()
    

    def init(self) -> None:
        self.create_table()
        self.create_bg_animation()
        self.create_items()
        self.active_button = self.button_1_player


    def create_table(self) -> None:
        table_graphics: list[Surface] | None = get_graphics_images_from_folder(Paths.main_menu_bg())
        table_texture: Surface = scale(choice(table_graphics), (Tables.texture_size, Tables.texture_size))
        self.table = Table(table_texture, self.display_surface)

    
    def create_bg_animation(self) -> None:
        self.animation_images = get_graphics_images_from_folder(Paths.card_front())

        for i in range(self.max_active_animations):
            self.create_bg_animation_item()

        self.animation_started = True

    
    def create_bg_animation_item(self) -> None:
        if len(self.active_animation_images) >= self.max_active_animations: return
        
        image_size = Images.size_smaller
        start_pos_y = -1 - image_size
        alpha = 128
        image: Surface = scale(choice(self.animation_images).copy(), (image_size, image_size))
        image.fill((255, 255, 255, alpha), None, BLEND_RGBA_MULT)
        x_pos: int = randrange(0, self.display_surface.get_width())
        y_pos: int = start_pos_y if self.animation_started else randrange(start_pos_y, self.screen_height)
        item = BackgroundItem(
            id=int(time_ns() // randint(9, 9999)),
            pic=image,
            rect=image.get_rect(center=(x_pos, y_pos)),
            size=image_size,
            speed=randint(1,4)
        )
        self.active_animation_images.append(item)

    
    def get_active_button(self) -> Button:
         return self.active_button
         

    def handle_event(self, event: Event, keys: ScancodeWrapper):

        if event.type == MOUSEMOTION:
            for button in self.hover_buttons:
                button.set_active(button.rect.collidepoint(event.pos) if button.rect else False)

        if event.type == MOUSEBUTTONDOWN:
            for button, action in self.button_actions.items():
                if button.rect.collidepoint(event.pos):
                    action()
                    break

            self.active_button = next((button for button in self.selection_buttons if button.rect.collidepoint(event.pos)), self.active_button)

    
    def create_items(self) -> None:
        center = self.screen_width // 2
        headline_pos_y = self.screen_height // 5
        
        self.headline = TextDisplay(self.game_name, Fonts.large(), (center, headline_pos_y))

        button_1_p_pos_x = center - Fonts.padding_top * Buttons.x_offset_mid
        button_1_p_pos_y = headline_pos_y + Fonts.padding_top * Buttons.y_offset_mid
        
        self.button_1_player = Button(1, '1 Player', (button_1_p_pos_x, button_1_p_pos_y), Fonts.medium())
        self.active_button = self.button_1_player

        button_2_p_pos_x = center + Fonts.padding_top * Buttons.x_offset_mid
        button_2_p_pos_y = headline_pos_y + Fonts.padding_top * Buttons.y_offset_mid
        
        self.button_2_players = Button(2, '2 Players', (button_2_p_pos_x, button_2_p_pos_y), Fonts.medium())
        
        start_quit_pos_y = headline_pos_y + Fonts.padding_top * Buttons.y_offset_down
        button_quit_x = center - Buttons.padding_x

        self.button_quit = Button(4, 'Exit', (button_quit_x, start_quit_pos_y), Fonts.medium()) 

        button_start_pos_x = center + Buttons.padding_x
        
        self.button_start = Button(3, 'Start', (button_start_pos_x, start_quit_pos_y), Fonts.medium())

        self.hover_buttons = [self.button_quit, self.button_start]
        self.selection_buttons = [self.button_1_player, self.button_2_players]
        self.button_actions = {
            self.button_quit: lambda: self.engine.exit_game(),
            self.button_start: lambda: setattr(self.engine.machine, 'next_state', PlayerSetup(self.engine, self.active_button.id, self.table))
        }

    
    def handle_bg_animation(self) -> None:
        if not self.active_animation_images: return
        
        for index, item in enumerate(self.active_animation_images):
            item.rect.y += item.speed    
            if item.rect.y > self.screen_height + item.size + 1:
                self.active_animation_images.pop(index)
                self.create_bg_animation_item()

    
    def draw_bg_animation(self) -> None:
        for item in self.active_animation_images:
            self.display_surface.blit(item.pic, item.rect)
            draw_rect(item.pic, Colors.background, item.rect, 1)


    def update(self) -> None:
        self.handle_bg_animation()


    def draw(self):
         self.table.draw()
         self.draw_bg_animation()
         self.headline.draw_static_text(self.display_surface, Colors.active)
         self.button_1_player.draw_clickable(self.display_surface, self.get_active_button)
         self.button_2_players.draw_clickable(self.display_surface, self.get_active_button)
         self.button_start.draw_hoverable(self.display_surface)
         self.button_quit.draw_hoverable(self.display_surface)


    def run(self):
        self.update()
        self.draw()