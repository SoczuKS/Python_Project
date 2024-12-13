import itertools
from typing import List, Sequence

from Card import Card
from LookupTable import LookupTable


class HandEvaluator:
    def __init__(self):
        self.__lookup_table = LookupTable()
        self.__hand_size_map = {
            5: self.__five,
            6: self.__six_or_seven,
            7: self.__six_or_seven
        }

    def evaluate(self, hand: List[Card], community_cards: List[Card]):
        all_cards = hand + community_cards
        return self.__hand_size_map[len(all_cards)](all_cards)

    def __five(self, cards: Sequence[Card]) -> int:
        if cards[0] & cards[1] & cards[2] & cards[3] & cards[4] & 0xF000:
            hand_value = (cards[0] | cards[1] | cards[2] | cards[3] | cards[4]) >> 16
            prime = Card.prime_product_from_rankbits(hand_value)
            return self.__lookup_table.get_flush_lookup(prime)
        else:
            prime = Card.prime_product_from_hand(cards)
            return self.__lookup_table.get_unsuited_lookup(prime)

    def __six_or_seven(self, cards: Sequence[Card]) -> int:
        minimum = LookupTable.get_max_high_card()
        for combination in itertools.combinations(cards, 5):
            score = self.__five(combination)
            if score < minimum:
                minimum = score
        return minimum
