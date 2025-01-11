from Rank import Rank
from Suit import Suit


class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def get_rank(self) -> Rank:
        return self.rank

    def get_color(self) -> str:
        return self.suit.get_color()

    def get_suit(self) -> Suit:
        return self.suit

    def get_bit_value(self) -> int:
        return (self.rank.value["bit_value"] << 16) | (self.suit.value << 12) | (self.rank.value["rank_value"] << 8) | self.rank.value["prime"]
