import random

from Card import Card
from Rank import Rank
from Suit import Suit


class Deck:
    def __init__(self):
        self.__cards = None

    def __build(self):
        self.__cards = []
        for suit in Suit:
            for rank in Rank:
                self.__cards.append(Card(suit, rank))

    def shuffle(self):
        self.__build()
        random.shuffle(self.__cards)

    def draw_card(self):
        return self.__cards.pop()
