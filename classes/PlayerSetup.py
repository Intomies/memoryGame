from random import choice
import pygame
from pygame import K_BACKSPACE, KEYDOWN, MOUSEBUTTONDOWN, TEXTINPUT, MOUSEMOTION, Surface
from pygame.draw import rect as draw_rect
from pygame.event import Event
from pygame.key import ScancodeWrapper
from pygame.time import get_ticks
from pygame.transform import scale
from typing import List, Optional

from classes import MainMenu
from classes.Button import Button
from classes.Engine import Engine
from classes.MemoryGame import MemoryGame
from classes.Player import Player
from classes.PlayerDetailEditor import PlayerDetailEditor
from classes.State import State
from classes.Table import Table
from utils.names import NAMES
from utils.settings import Buttons, Images, Paths, Screens, Fonts
from utils.support import get_graphics_images_from_folder


class PlayerSetup(State):
    def __init__(self, engine: Engine, players_amount: int, table: Table) -> None:
        super().__init__(engine)

        self.id: int = Screens.player_info_id
        self.players_amount = players_amount
        self.table = table
        
        self.display_surface: Surface = self.engine.screen
        self.screen_width: int = self.display_surface.get_width()
        self.screen_height: int = self.display_surface.get_height()

        self.active_player: Optional[Player] = None

        self.button_start_game: Optional[Button] = None
        self.button_back: Optional[Button] = None

        self.player_1_editor: Optional[PlayerDetailEditor] = None
        self.player_2_editor: Optional[PlayerDetailEditor] = None

        self.active_image_selector: Optional[PlayerDetailEditor] = None
        self.latest_event: Optional[Event] = None
        self.last_click_time = 0
        self.click_cooldown = 200

        self.init()


    def init(self) -> None:
        self.create_screen_items()

    
    def set_active_image_selector(self, value: PlayerDetailEditor | None) -> None:
        self.active_image_selector = value


    def handle_event(self, event: Event, keys: ScancodeWrapper):
        self.latest_event = event

        if event.type == MOUSEMOTION:
            self.button_back.active = self.button_back.rect.collidepoint(event.pos) if self.button_back.rect else False
            self.button_start_game.active = self.button_start_game.rect.collidepoint(event.pos) if self.button_start_game.rect else False
        
        if event.type == MOUSEBUTTONDOWN and not self.active_image_selector:
            self.last_click_time = get_ticks()

            if self.button_start_game.rect.collidepoint(event.pos):
                self.engine.machine.next_state = MemoryGame(
                    self.engine,
                    self.players_amount,
                    self.player_1_editor.player, 
                    self.player_2_editor.player if self.player_2_editor else None
                    )

            if self.button_back.rect.collidepoint(event.pos):
                self.engine.run(MainMenu.MainMenu(self.engine))

            self.player_1_editor.name_input_active = self.player_1_editor.name_editor_rect.collidepoint(event.pos)
            self.player_1_editor.image_selector_active = self.player_1_editor.player_img_rect.collidepoint(event.pos)

            if self.players_amount == 2:
                self.player_2_editor.name_input_active = self.player_2_editor.name_editor_rect.collidepoint(event.pos)
                self.player_2_editor.image_selector_active = self.player_2_editor.player_img_rect.collidepoint(event.pos)
            

        if self.player_1_editor.name_input_active or (self.players_amount == 2 and self.player_2_editor.name_input_active):
            self.handle_name_input(event)

        if not self.active_image_selector:
            if self.player_1_editor.image_selector_active or (self.players_amount == 2 and self.player_2_editor.image_selector_active):
                self.active_image_selector = self.player_1_editor if self.player_1_editor.image_selector_active else self.player_2_editor
            else:
                self.active_image_selector = None


    def handle_name_input(self, event: Event) -> None:
        active_editor: PlayerDetailEditor = self.player_1_editor if self.player_1_editor.name_input_active else self.player_2_editor
        name: str = active_editor.player.name
        
        if event.type == TEXTINPUT:
            name += event.text if len(name) < Fonts.name_length else ''
        if event.type == KEYDOWN: 
            if event.key == K_BACKSPACE:
                name = active_editor.player.name[:-1]
        
        active_editor.set_player_name(name)


    def create_screen_items(self) -> None:
        headline_pos_x = self.screen_width // 2
        headline_pos_y = self.screen_height // 5
        button_back_pos_x = headline_pos_x - Buttons.padding_x
        button_start_pos_x = headline_pos_x + Buttons.padding_x
        button_pos_y = headline_pos_y + Fonts.padding_top * Buttons.y_offset_down

        player_images: List[Surface] | None = get_graphics_images_from_folder(Paths.card_front())

        self.button_start_game = Button(3, 'Start', (button_start_pos_x, button_pos_y), Fonts.medium())
        self.button_back = Button(3, 'Back', (button_back_pos_x, button_pos_y), Fonts.medium())
        
        player = Player(1, choice(NAMES), image=scale(choice(player_images), (Images.size_mid, Images.size_mid)))     
        self.player_1_editor = PlayerDetailEditor(self.display_surface, player, player_images, self.players_amount)

        if self.players_amount == 2:
            player = Player(2, choice(NAMES), image=scale(choice(player_images), (Images.size_mid, Images.size_mid))) 
            self.player_2_editor = PlayerDetailEditor(self.display_surface, player, player_images, self.players_amount)

    
    def handle_player_draw(self) -> None:
        self.player_1_editor.draw_player_details_editor()
        
        if self.players_amount == 2:
            self.player_2_editor.draw_player_details_editor()


    def draw(self) -> None:
        self.table.draw()
        self.handle_player_draw()
        self.button_start_game.draw_hoverable(self.display_surface)
        self.button_back.draw_hoverable(self.display_surface)
        cooldown = get_ticks() - self.last_click_time < self.click_cooldown
        if self.active_image_selector is not None:
            self.active_image_selector.draw_image_selector(self.set_active_image_selector, self.latest_event, cooldown)


    def run(self) -> None:
        self.draw()