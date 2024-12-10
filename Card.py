from Rank import Rank
from Suit import Suit


class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank}{self.suit.value}"

    def get_color(self):
        return self.suit.get_color()
