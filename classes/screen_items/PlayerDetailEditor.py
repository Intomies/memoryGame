from typing import Callable, List, Optional
from pygame import MOUSEBUTTONDOWN, Rect, Surface
from pygame.draw import rect as draw_rect
from pygame.event import Event
from pygame.transform import scale

from classes.game_components.Player import Player
from utils.settings import Colors, Images, Fonts


class PlayerDetailEditor:
    def __init__(
            self, 
            display_surface: Surface,
            player: Player,
            player_images: List[Surface],
            player_amount: int
            ) -> None:
        
        self.display_surface: Surface = display_surface
        self.screen_width = display_surface.get_width()
        self.screen_height = display_surface.get_height()
        self.player = player
        self.player_images = player_images
        self.player_amount = player_amount
        self.name_editor_font = Fonts.medium()

        self.editor_bg_surface: Optional[Surface] = None
        self.editor_bg_rect: Optional[Rect] = None
        self.player_img_rect: Optional[Rect] = None
        self.name_editor_surface: Optional[Surface] = None
        self.name_editor_rect: Optional[Rect] = None
        self.active_name_editor_border: Optional[Surface] = None
        self.active_name_editor_border_rect: Optional[Rect] = None
        
        self.name_input_active: bool = False
        self.image_selector_active: bool = False

        self.__init()


    def draw_player_details_editor(self) -> None:
        border_width = 2
        name_editor_border_color = Colors.active if self.name_input_active else Colors.passive
        # self.name_editor_rect.width = self.editor_bg_rect.width - 10
        self.name_editor_rect.x = self.editor_bg_rect.x + (self.editor_bg_rect.width - self.name_editor_rect.width) // 2

        self.display_surface.blit(self.editor_bg_surface, self.editor_bg_rect)
        draw_rect(self.display_surface, Colors.passive, self.editor_bg_rect, border_width)
        
        self.display_surface.blit(self.player.image, self.player_img_rect)
        draw_rect(self.display_surface, Colors.passive, self.player_img_rect, border_width)

        if self.name_input_active:
            self.display_surface.blit(self.active_name_editor_border, self.active_name_editor_border_rect)
            draw_rect(self.display_surface, name_editor_border_color, self.active_name_editor_border_rect, border_width)
        self.display_surface.blit(self.name_editor_surface, self.name_editor_rect)

    
    def draw_image_selector(self, set_active_image_selector: Callable, latest_mouse_event: Event, cooldown: bool):
        padding = 10
        image_size = Images.size_small
        images_per_row = (self.screen_width // 3) // (image_size + padding)
        row_count = (len(self.player_images) + images_per_row - 1) // images_per_row
        
        start_x = (self.screen_width - (images_per_row * (image_size + padding) - padding)) // 2
        start_y = self.screen_height // 5
        
        img_select_bg_rect = Rect(
            start_x - padding // 2, 
            start_y - padding // 2, 
            images_per_row * (image_size + padding), 
            row_count * (image_size + padding)
            )
        
        self.display_surface.blit(Surface(img_select_bg_rect.size), img_select_bg_rect)
        draw_rect(self.display_surface, Colors.active, img_select_bg_rect, 2)
        for idx, image in enumerate(self.player_images):
            
            col = idx % images_per_row
            row = idx // images_per_row
            x = start_x + col * (image_size + padding)
            y = start_y + row * (image_size + padding)
            image_rect = Rect(x, y, image_size, image_size)
            
            self.display_surface.blit(scale(image, (image_size, image_size)), (x, y))
            if latest_mouse_event and latest_mouse_event.type == MOUSEBUTTONDOWN and not cooldown:
                if image_rect.collidepoint(latest_mouse_event.pos):
                    player_image_size = (Images.size_mid, Images.size_mid)
                    self.player.image = scale(image, player_image_size)
                    set_active_image_selector(None)
                    self.image_selector_active = False
                    return           

    
    def set_player_name(self, name: str) -> None:
        self.player.name = name
        self.name_editor_surface = self.name_editor_font.render(name, True, Colors.active)
        self.name_editor_rect = self.name_editor_surface.get_rect(center=self.name_editor_rect.center)


    def __init(self) -> None:
        self.editor_bg_rect = self.__get_bg_rect()
        self.editor_bg_surface = Surface((self.editor_bg_rect.size), masks=Colors.background)

        image_pos = (self.editor_bg_rect.centerx, self.editor_bg_rect.top + Fonts.padding_top)
        self.player_img_rect = self.player.image.get_rect(center=image_pos)

        name_editor_pos = (self.editor_bg_rect.centerx, self.player_img_rect.bottom + Fonts.padding_top)
        
        self.name_editor_surface = self.name_editor_font.render(str(self.player.name), True, Colors.active)
        self.name_editor_rect = self.name_editor_surface.get_rect(center=name_editor_pos)

        self.active_name_editor_border_rect = Rect(self.editor_bg_rect.left, self.name_editor_rect.top, self.editor_bg_rect.width - 10, self.name_editor_rect.height)
        self.active_name_editor_border = Surface(self.active_name_editor_border_rect.size)


    def __get_bg_rect(self) -> Rect:
        center_div_x = 2
        center_div_y = 4
        width_div = 5
        height_div = 2
        offset_div_x_2_pla = width_div // 1.5
        offset_div_1_p = width_div * 2

        match self.player.id:
            case 0:
                rect_left_offset = offset_div_x_2_pla if self.player_amount == 2 else offset_div_1_p
                return Rect(
                    self.screen_width // center_div_x - self.screen_width // rect_left_offset, 
                    self.screen_height // center_div_y, 
                    self.screen_width // width_div, 
                    self.screen_height // height_div
                )
            case 1:
                return Rect(
                    self.screen_width // center_div_x + self.screen_width // offset_div_x_2_pla - self.screen_width // width_div, 
                    self.screen_height // center_div_y, 
                    self.screen_width // width_div, 
                    self.screen_height // height_div
                )
            case _:
                return Rect(
                    self.screen_width // center_div_x - self.screen_width // offset_div_1_p, 
                    self.screen_height // center_div_y, 
                    self.screen_width // width_div, 
                    self.screen_height // height_div
                ) 
    
