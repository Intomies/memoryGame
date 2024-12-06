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
            player_1: Optional[Player] = None,
            player_2: Optional[Player] = None,
            turns: Optional[int] = None
            ) -> None:
        self.display_surface = display_surface
        self.player_1 = player_1
        self.player_2 = player_2
        self.turns = turns
        self.font = Fonts.small()

        self.screen_bg_rect: Optional[Rect] = None
        self.screen_bg: Optional[Surface] = None
        
        self.headline_field: Optional[Surface] = None
        self.result_field: Optional[Surface] = None

        self.player_1_image_rect: Optional[Rect] = None
        self.player_2_image_rect: Optional[Rect] = None
        
        self.player_1_name_field: Optional[Surface] = None
        self.player_2_name_field: Optional[Surface] = None
        
        self.player_1_score_field: Optional[Surface] = None
        self.player_2_score_field: Optional[Surface] = None

        self.turns_field: Optional[Surface] = None
        self.back_button: Optional[Button] = None

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

        images_y = result_y + self.result_field.get_height() + self.player_1_image_rect.height // 2 + padding_y
        player_1_x = center[0] if not self.player_2 else self.screen_bg_rect.left + padding_x + self.player_1.image.get_width() // 2
        self.player_1_image_rect.x = player_1_x
        self.player_1_image_rect.y = images_y
        self.display_surface.blit(self.player_1.image, self.player_1.image.get_rect(center=(player_1_x, images_y)))
        
        names_y = self.player_1_image_rect.center[1] + self.player_1_name_field.get_height() + padding_y
        player_1_name_x = center[0] if not self.player_2 else self.player_1_image_rect.x
        self.display_surface.blit(self.player_1_name_field, self.player_1_name_field.get_rect(center=(player_1_name_x, names_y)))

        scores_y = names_y + self.player_1_name_field.get_height() + padding_y
        player_1_score_x = center[0] if not self.player_2 else self.player_1_image_rect.x
        self.display_surface.blit(self.player_1_score_field, self.player_1_score_field.get_rect(center=(player_1_score_x, scores_y)))

        if self.player_2:
            player_2_x = self.screen_bg_rect.right - padding_x - self.player_1.image.get_width() // 2
            self.player_2_image_rect.x = player_2_x
            self.player_2_image_rect.y = images_y
            self.display_surface.blit(self.player_2.image, self.player_2.image.get_rect(center=(player_2_x, images_y)))
            
            player_2_name_x = self.player_2_image_rect.x
            self.display_surface.blit(self.player_2_name_field, self.player_2_name_field.get_rect(center=(player_2_name_x, names_y)))

            player_2_score_x = self.player_2_image_rect.x
            self.display_surface.blit(self.player_2_score_field, self.player_2_score_field.get_rect(center=(player_2_score_x, scores_y)))

        self.new_game_button.draw_hoverable(self.display_surface)
        self.back_button.draw_hoverable(self.display_surface)


    def populate(self) -> None:
        self.player_1.active = self.player_1.score > self.player_2.score or self.player_1.score == self.player_2.score if self.player_2 else True
        if self.player_2: self.player_2.active = self.player_2.score > self.player_1.score or self.player_2.score == self.player_1.score
        
        self.headline_field = self.font.render('Game over!', True, Colors.active)
        self.result_field = self.font.render(self.get_result_text(), True, Colors.active)
        self.result_field = self.font.render(self.get_result_text(), True, Colors.active)

        self.player_1_image_rect = self.player_1.image.get_rect()
        self.player_2_image_rect = self.player_2.image.get_rect() if self.player_2 else None

        self.player_1_name_field = self.font.render(self.player_1.name, True, Colors.active)
        self.player_2_name_field = self.font.render(self.player_2.name, True, Colors.active) if self.player_2 else None

        self.player_1_score_field = self.font.render(f'Score: {self.player_1.score}', True, Colors.active)
        self.player_2_score_field = self.font.render(f'Score: {self.player_2.score}', True, Colors.active) if self.player_2 else None

        self.ready = True


    def set_active_player(self) -> None:
        self.player_1.active = self.player_1.score > self.player_2.score or self.player_1.score == self.player_2.score if self.player_2 else True
        
        if self.player_2: self.player_2.active = self.player_2.score > self.player_1.score or self.player_2.score == self.player_1.score


    def get_result_text(self) -> str:
        if not self.player_2: return f'{self.player_1.name} won the game on turn {self.turns}!'

        if self.player_1.score == self.player_2.score:
            return f'Game ended with tie on turn {self.turns}!'
        
        if self.player_1.score > self.player_2.score:
            return f'{self.player_1.name} wins on turn {self.turns}!'
        
        return f'{self.player_2.name} wins on turn {self.turns}!'

        



        