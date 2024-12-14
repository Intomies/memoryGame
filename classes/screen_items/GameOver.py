from typing import Optional
from pygame import Surface, Rect
from pygame.draw import rect as draw_rect

from classes.screen_items.Button import Button
from classes.game_components.Player import Player
from utils.settings import Buttons, Colors, Fonts


class GameOver:
    def __init__(
            self,
            display_surface: Surface,
            players: list[Player] = [],
            turns: Optional[int] = None
            ) -> None:
        self.display_surface = display_surface
        self.players = players
        
        self.turns = turns
        self.font = Fonts.small()

        self.screen_bg_rect: Optional[Rect] = None
        self.screen_bg: Optional[Surface] = None
        
        self.headline_field: Optional[Surface] = None
        self.result_field: Optional[Surface] = None

        self.player_image_rects: list[Rect] = []
        self.player_name_fields: list[Surface] = []
        self.player_score_fields: list[Surface] = []

        self.turns_field: Optional[Surface] = None
        self.back_button: Optional[Button] = None
        self.new_game_button: Optional[Button] = None

        self.ready = False

        self.__init()


    def __init(self) -> None:
        screen_width = self.display_surface.get_width()
        screen_height = self.display_surface.get_height()
        bg_width = screen_width // 3
        bg_height = screen_height // 2
        bg_left = screen_width // 2 - bg_width // 2
        bg_top = screen_height // 2 - bg_height // 2

        self.screen_bg_rect = Rect(bg_left, bg_top, bg_width, bg_height)
        self.screen_bg = Surface((self.screen_bg_rect.size))

        button_x = self.screen_bg_rect.center[0]
        back_button_y = self.screen_bg_rect.bottom - Buttons.padding_y
        self.back_button = Button(3, 'Back to menu', (button_x, back_button_y), self.font)
        
        new_game_button_y = self.screen_bg_rect.bottom - Buttons.padding_y - Fonts.small_font_size * 1.1
        self.new_game_button = Button(4, 'New game', (button_x, new_game_button_y), self.font)


    def draw(self) -> None:
        self.display_surface.blit(self.screen_bg, self.screen_bg_rect)
        draw_rect(self.display_surface, Colors.active, self.screen_bg_rect, 2)
        padding_y = 20
        padding_x = 100
        center = self.screen_bg_rect.center

        headline_y = self.screen_bg_rect.top + padding_y
        self.display_surface.blit(self.headline_field, self.headline_field.get_rect(center=center, top=headline_y))

        result_y = headline_y + self.headline_field.get_height() + padding_y
        self.display_surface.blit(self.result_field, self.result_field.get_rect(center=center, top=result_y))

        self.new_game_button.draw_hoverable(self.display_surface)
        self.back_button.draw_hoverable(self.display_surface)

        player_area_width = self.screen_bg_rect.width - 2 * padding_x
        player_spacing = player_area_width // (len(self.players) + 1)
        base_y = result_y + self.result_field.get_height() + padding_y
        
        for i, player in enumerate(self.players):
            # Calculate player x-position
            player_x = self.screen_bg_rect.left + padding_x + (i + 1) * player_spacing
            
            # Draw player image
            player_image_y = base_y + player.image.get_height() // 2
            self.display_surface.blit(player.image, player.image.get_rect(center=(player_x, player_image_y)))
            
            # Draw player name
            player_name_y = player_image_y + player.image.get_height() // 2 + padding_y
            self.display_surface.blit(self.player_name_fields[i], self.player_name_fields[i].get_rect(center=(player_x, player_name_y)))
            
            # Draw player score
            player_score_y = player_name_y + self.player_name_fields[i].get_height() + padding_y
            self.display_surface.blit(self.player_score_fields[i], self.player_score_fields[i].get_rect(center=(player_x, player_score_y)))


    def populate(self) -> None:
        self.__set_active_player()
        
        self.headline_field = self.font.render('Game over!', True, Colors.active)
        self.result_field = self.font.render(self.__get_result_text(), True, Colors.active)

        self.player_image_rects = [player.image.get_rect() for player in self.players]
        self.player_name_fields = [self.font.render(player.name, True, Colors.active) for player in self.players]
        self.player_score_fields = [self.font.render(f'Score: {player.score}', True, Colors.active) for player in self.players]

        self.ready = True


    def __set_active_player(self) -> None:
        highest_score = max(self.players, key=lambda player: player.score) 
        lowest_score = min(self.players, key=lambda player: player.score)

        if highest_score == lowest_score:
            for player in self.players: player.active = True
            return
        
        highest_score.active = True
        


    def __get_result_text(self) -> str:
        highest_score = max(self.players, key=lambda player: player.score) 
        lowest_score = min(self.players, key=lambda player: player.score) 

        if highest_score == lowest_score:
            return f'Game ended with tie on turn {self.turns}!'
        
        return f'{highest_score.name} wins the game on turn {self.turns}!'

        



        