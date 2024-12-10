from enum import Enum


class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"

    def get_color(self):
        if self == Suit.HEARTS or self == Suit.DIAMONDS:
            return "red"
        return "black"
