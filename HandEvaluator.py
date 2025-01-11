import itertools

from LookupTable import LookupTable


def _prime_product(cards):
    product = 1
    for card in cards:
        product *= card.get_rank().value["prime"]

    return product


def get_hand_name(hand_value):
    if 0 <= hand_value <= LookupTable.max_royal_flush:
        return "Royal Flush"
    elif hand_value <= LookupTable.max_straight_flush:
        return "Straight Flush"
    elif hand_value <= LookupTable.max_four_of_a_kind:
        return "Four of a Kind"
    elif hand_value <= LookupTable.max_full_house:
        return "Full House"
    elif hand_value <= LookupTable.max_flush:
        return "Flush"
    elif hand_value <= LookupTable.max_straight:
        return "Straight"
    elif hand_value <= LookupTable.max_three_of_a_kind:
        return "Three of a Kind"
    elif hand_value <= LookupTable.max_two_pair:
        return "Two Pair"
    elif hand_value <= LookupTable.max_pair:
        return "Pair"
    else:
        return "High Card"


class HandEvaluator:
    __HAND_LENGTH = 2
    __BOARD_LENGTH = 5

    def __init__(self):
        self.__lookup_table = LookupTable()
        self.__hand_size_mapping = {5: self.__five, 6: self.__six_or_seven, 7: self.__six_or_seven}

    def evaluate(self, hand_cards, common_cards):
        all_cards = hand_cards + common_cards
        return self.__hand_size_mapping[len(all_cards)](all_cards)

    def __five(self, cards):
        prime_product = _prime_product(cards)

        if cards[0].get_suit() == cards[1].get_suit() == cards[2].get_suit() == cards[3].get_suit() == cards[4].get_suit():
            return self.__lookup_table.flush_lookup(prime_product)

        return self.__lookup_table.unsuited_lookup(prime_product)

    def __six_or_seven(self, cards):
        min_score = LookupTable.max_high_card

        for combination in itertools.combinations(cards, 5):
            score = self.__five(combination)
            if score < min_score:
                min_score = score

        return min_score
