from Rank import Rank
from Suit import Suit


class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def get_color(self):
        return self.suit.get_color()

    def get_bit_value(self) -> int:
        return (self.rank.value["bit_value"] << 16) | (self.suit.value << 12) | (self.rank.value["rank_value"] << 8) | self.rank.value["prime"]
