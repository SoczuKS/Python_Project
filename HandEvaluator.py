import itertools

from LookupTable import LookupTable


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
        first_card_bit_value = cards[0].get_bit_value()
        second_card_bit_value = cards[1].get_bit_value()
        third_card_bit_value = cards[2].get_bit_value()
        fourth_card_bit_value = cards[3].get_bit_value()
        fifth_card_bit_value = cards[4].get_bit_value()

        prime_product = self.__prime_product(cards)

        if first_card_bit_value & second_card_bit_value & third_card_bit_value & fourth_card_bit_value & fifth_card_bit_value & 0xF000:
            return self.__lookup_table.flush_lookup(prime_product)

        return self.__lookup_table.unsuited_lookup(prime_product)


    def __six_or_seven(self, cards):
        min_score = LookupTable.max_high_card

        for combination in itertools.combinations(cards, 5):
            score = self.__five(combination)
            if score < min_score:
                min_score = score

        return min_score

    @staticmethod
    def __prime_product(cards):
        product = 1
        for card in cards:
            product *= card.get_rank()["prime"]

        return product
