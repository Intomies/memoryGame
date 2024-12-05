from pygame import MOUSEBUTTONDOWN, MOUSEMOTION, Surface
from pygame.event import Event
from pygame.display import get_surface
from pygame.key import ScancodeWrapper
from pygame.sprite import Group
from pygame.transform import scale
from random import choice, sample, shuffle
from typing import List, Optional

from classes.Button import Button
from classes.Card import Card
from classes.Deck import Deck
from classes.Engine import Engine
from classes.GameOver import GameOver
from classes.Player import Player
from classes.State import State
from classes.Table import Table
from classes.TextDisplay import TextDisplay

from utils.settings import Buttons, Cards, Paths, Screens, Tables, Fonts
from utils.support import get_graphics_images_from_folder


class MemoryGame(State):
    def __init__(
            self, 
            engine: Engine, 
            players_amount: int,
            player_1: Player, 
            player_2: Optional[Player] = None
            ) -> None:
        super().__init__(engine=engine)

        self.id: int = Screens.game_view_id
        self.display_surface: Surface = get_surface()
        self.screen_width: int = self.display_surface.get_width()
        self.screen_height: int = self.display_surface.get_height()
        self.interaction_entities: Group = Group()

        self.table: Optional[Table] = None
        self.deck: Optional[Deck] = None 
        self.players: List[Player] = []

        self.players_amount = players_amount
        self.player_1: Optional[Player] = player_1
        self.player_2: Optional[Player] = player_2
        self.active_player: Player = choice([self.player_1, self.player_2]) if self.players_amount == 2 else self.player_1
        
        self.player_1_name_display: Optional[TextDisplay] = None
        self.player_2_name_display: Optional[TextDisplay] = None
        
        self.player_1_score_display: Optional[TextDisplay] = None
        self.player_2_score_display: Optional[TextDisplay] = None

        self.button_back: Optional[Button] = None
        self.button_quit: Optional[Button] = None

        self.game_over_view: Optional[GameOver] = None

        self.open_cards: List[Card] = []
        self.player_found_pair = False
        self.turns = 0
        self.game_over = False

        self.init()


    def init(self) -> None:
        self.game_over = False
        self.player_1.score = 0
        if self.player_2: self.player_2.score = 0
        self.turns = 0
        self.open_cards = []
        self.player_found_pair = False
        self.game_over_view = None
        self.active_player: Player = choice([self.player_1, self.player_2]) if self.players_amount == 2 else self.player_1

        self.create_table()
        self.create_deck()
        self.create_screen_items()
    

    def create_table(self) -> None:
        table_graphics: List[Surface] | None = get_graphics_images_from_folder(Paths.table())
        table_texture: Surface = scale(choice(table_graphics), (Tables.texture_size, Tables.texture_size))
        self.table = Table(table_texture, self.display_surface)


    def create_deck(self) -> None:
        created_cards: List[Card] = []
        card_back_graphics: List[Surface] | None = get_graphics_images_from_folder(Paths.card_back())
        card_front_graphics: List[Surface] | None = get_graphics_images_from_folder(Paths.card_front())
        card_back_texture = choice(card_back_graphics)
        card_front_textures = sample(card_front_graphics, Cards.amount)

        for index, front_texture in enumerate(card_front_textures):
            created_card = Card(
                id=(index, 1), 
                front_img=scale(front_texture, (Cards.size, Cards.size)),
                back_img=scale(card_back_texture, (Cards.size, Cards.size))
                )
            created_card_pair = Card(
                id=(index, 2), 
                front_img=scale(front_texture, (Cards.size, Cards.size)),
                back_img=scale(card_back_texture, (Cards.size, Cards.size))
                )
            created_cards.append(created_card)
            created_cards.append(created_card_pair)

        shuffle(created_cards)
        self.deck = Deck(self.display_surface, created_cards)

    
    def create_screen_items(self) -> None:
        buttons_x = Buttons.padding_x
        button_quit_y = self.screen_height - Buttons.padding_y
        self.button_quit = Button(4, 'Quit', (buttons_x, button_quit_y), Fonts.medium())
        button_back_y = button_quit_y - Buttons.padding_y
        self.button_back = Button(3, 'Back', (buttons_x, button_back_y), Fonts.medium())

        self.player_1.set_display_surface(self.display_surface)
        self.player_1.set_name_display()
        self.player_1.set_score_display()
        self.player_1.set_image_display()
        
        if self.players_amount == 2:
            self.player_2.set_display_surface(self.display_surface)
            self.player_2.set_name_display()
            self.player_2.set_score_display()
            self.player_2.set_image_display()

        self.game_over_view = GameOver(self.display_surface)

    
    def handle_event(self, event: Event, keys: ScancodeWrapper) -> None:
        if event.type == MOUSEBUTTONDOWN:
            
            if self.button_back.rect.collidepoint(event.pos) or (self.game_over and self.game_over_view.ready and self.game_over_view.back_button.rect.collidepoint(event.pos)):
                self.engine.machine.next_state = self.engine.machine.previous()
            if self.button_quit.rect.collidepoint(event.pos):
                self.handle_game_over()

            if self.game_over and self.game_over_view.ready and self.game_over_view.new_game_button.rect.collidepoint(event.pos):
                self.init()
    
            self.handle_player_turn(event)

        if event.type == MOUSEMOTION:
            self.button_back.set_active(self.button_back.rect.collidepoint(event.pos) if self.button_back.rect else False)
            self.button_quit.set_active(self.button_quit.rect.collidepoint(event.pos) if self.button_quit.rect else False)
            if self.game_over:
                self.game_over_view.new_game_button.set_active(self.game_over_view.new_game_button.rect.collidepoint(event.pos))
                self.game_over_view.back_button.set_active(self.game_over_view.back_button.rect.collidepoint(event.pos))
            
    
    def handle_player_turn(self, event: Event) -> None:
        if self.game_over: return
        
        for card in self.deck.cards:
            if not card.rect.collidepoint(event.pos):
                continue
            
            if not self.handle_card_turn(card):
                continue
            
            if not self.player_found_pair and self.players_amount == 2:
                self.active_player = (
                    self.player_1 
                    if self.active_player.id != self.player_1.id 
                    else self.player_2
                )
            break

        self.player_found_pair = False
        self.is_game_over()

    
    def handle_card_turn(self, card: Card) -> bool:
        if card.id in [c.id for c in self.open_cards] and len(self.open_cards) < 2: return False
        if card.found_pair: return False
        
        if len(self.open_cards) < 2:
            card.turn()
            self.open_cards.append(card)
            return False
        
        elif len(self.open_cards) == 2 and self.open_cards[0].id[0] == self.open_cards[1].id[0]:
            for c in self.deck.cards:
                if c.id in [oc.id for oc in self.open_cards]:
                    c.found_pair = True
            self.open_cards.clear()
            self.active_player.add_points()
            self.player_found_pair = True
            self.turns += 1
            return True

        else: 
            for c in self.deck.cards:
                if c.id in [oc.id for oc in self.open_cards]:
                    c.turn()
            self.open_cards.clear()
            self.turns += 1
            return True
        

    def is_game_over(self) -> None:
        for card in self.deck.cards:
            if not card.found_pair: return
        
        self.handle_game_over()
        

    def handle_game_over(self) -> None:
        self.game_over = True
        self.game_over_view.player_1 = self.player_1
        self.game_over_view.player_2 = self.player_2
        self.game_over_view.turns = self.turns


    def update(self) -> None:
        self.player_1.set_score_display()
        if self.players_amount == 2:
            self.player_2.set_score_display()
        if self.game_over: self.game_over_view.populate()


    def draw(self) -> None:
        self.table.draw()
        self.deck.draw(self.screen_width, self.screen_height)
        self.button_back.draw_hoverable(self.display_surface)
        self.button_quit.draw_hoverable(self.display_surface)

        player_1_turn = self.active_player.id == self.player_1.id

        self.player_1.image_display.draw(active=player_1_turn)
        self.player_1.name_display.draw(display=self.display_surface, active=player_1_turn)
        self.player_1.score_display.draw(display=self.display_surface, active=player_1_turn)
        if self.players_amount == 2:
            self.player_2.image_display.draw(active=not player_1_turn)
            self.player_2.name_display.draw(display=self.display_surface, active=not player_1_turn)
            self.player_2.score_display.draw(display=self.display_surface, active=not player_1_turn)

        if self.game_over and self.game_over_view.ready: self.game_over_view.draw()


    def run(self) -> None:
        self.update()
        self.draw()