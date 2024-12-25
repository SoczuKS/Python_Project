from enum import Enum


class Suit(Enum):
    HEARTS = 0b0010
    DIAMONDS = 0b0100
    CLUBS = 0b1000
    SPADES = 0b0001

    def get_color(self):
        if self == Suit.HEARTS or self == Suit.DIAMONDS:
            return "red"
        return "black"

    def __str__(self):
        string_representation = {Suit.HEARTS: "♥", Suit.DIAMONDS: "♦", Suit.CLUBS: "♣", Suit.SPADES: "♠"}
        return string_representation[self]
