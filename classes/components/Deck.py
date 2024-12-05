from pygame import Surface
from pygame.draw import rect as draw_rect
from typing import List

from classes.components.Card import Card
from utils.settings import Cards, Colors, Decks


class Deck:
    def __init__(
            self,
            display_surface: Surface,
            cards: List[Card],
            ) -> None:
        self.display_surface: Surface = display_surface
        self.cards: List[Card] = cards
        self.open_cards: List[Card] = []


    def draw(self, screen_width: int, screen_height: int):
        display_cards: List[Card] = self.cards.copy()
        rows = Decks.num_rows
        cols = Decks.num_columns
        card_size = Cards.size
        margin = Decks.padding
        padding = Decks.padding
        x_start = (screen_width // 2) - ((card_size * cols) + ((cols - 1) * padding)) // 2 - margin
        y_start = (screen_height // 2) - ((card_size * cols) + ((cols - 1) * padding)) // 2 - margin
        
        for row in range(rows):
            for col in range(cols):
                x = x_start + margin + col * (card_size + padding)
                y = y_start + margin + row * (card_size + padding)

                card = display_cards.pop()
                # print(card.selected_img.get_rect(topleft=(x, y)))
                card.rect = card.selected_img.get_rect(topleft=(x, y))
                draw_rect(
                    card.selected_img, 
                    Colors.active if card.found_pair else Colors.border, 
                    card.selected_img.get_rect(), 
                    Cards.border_width
                    )
                
                self.display_surface.blit(card.selected_img, (x, y))


