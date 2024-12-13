import itertools
from collections.abc import Iterator

from Card import Card


class LookupTable:
    __max_royal_flush = 1
    __max_straight_flush = 10
    __max_four_of_a_kind = 166
    __max_full_house = 322
    __max_flush = 1599
    __max_straight = 1609
    __max_three_of_a_kind = 2467
    __max_two_pair = 3325
    __max_pair = 6185
    __max_high_card = 7462

    __max_to_rank_class = {__max_royal_flush: 0, __max_straight_flush: 1, __max_four_of_a_kind: 2, __max_full_house: 3, __max_flush: 4, __max_straight: 5,
                           __max_three_of_a_kind: 6, __max_two_pair: 7, __max_pair: 8, __max_high_card: 9}

    __rank_class_to_string = {0: "Royal Flush", 1: "Straight Flush", 2: "Four of a Kind", 3: "Full House", 4: "Flush", 5: "Straight", 6: "Three of a Kind",
                              7: "Two Pair", 8: "Pair", 9: "High Card"}

    @staticmethod
    def get_max_high_card() -> int:
        return LookupTable.__max_high_card

    @staticmethod
    def get_rank_class(hand_value: int):
        if 0 <= hand_value <= LookupTable.__max_royal_flush:
            return LookupTable.__max_to_rank_class[LookupTable.__max_royal_flush]
        if hand_value <= LookupTable.__max_straight_flush:
            return LookupTable.__max_to_rank_class[LookupTable.__max_straight_flush]
        if hand_value <= LookupTable.__max_four_of_a_kind:
            return LookupTable.__max_to_rank_class[LookupTable.__max_four_of_a_kind]
        if hand_value <= LookupTable.__max_full_house:
            return LookupTable.__max_to_rank_class[LookupTable.__max_full_house]
        if hand_value <= LookupTable.__max_flush:
            return LookupTable.__max_to_rank_class[LookupTable.__max_flush]
        if hand_value <= LookupTable.__max_straight:
            return LookupTable.__max_to_rank_class[LookupTable.__max_straight]
        if hand_value <= LookupTable.__max_three_of_a_kind:
            return LookupTable.__max_to_rank_class[LookupTable.__max_three_of_a_kind]
        if hand_value <= LookupTable.__max_two_pair:
            return LookupTable.__max_to_rank_class[LookupTable.__max_two_pair]
        if hand_value <= LookupTable.__max_pair:
            return LookupTable.__max_to_rank_class[LookupTable.__max_pair]
        return LookupTable.__max_to_rank_class[LookupTable.__max_high_card]

    @staticmethod
    def get_rank_class_string(rank_class):
        return LookupTable.__rank_class_to_string[rank_class]

    def __init__(self):
        self.__flush_lookup = {}
        self.__unsuited_lookup = {}
        self.__flushes()
        self.__multiples()

    def __flushes(self):
        straight_flushes = [7936, 3968, 1984, 992, 496, 248, 124, 62, 31, 4111]

        flushes = []
        generator = self.__get_lexicographically_next_bit_sequence(int('0b11111', 2))

        for i in range(1277 + len(straight_flushes) - 1):
            flush = next(generator)

            for straight_flush in straight_flushes:
                if not flush ^ straight_flush:
                    break
            else:
                flushes.append(flush)

        flushes.reverse()

        rank = 1
        for straight_flush in straight_flushes:
            prime_product = Card.prime_product_from_rankbits(straight_flush)
            self.__flush_lookup[prime_product] = rank
            rank += 1

        self.__straight_and_high_cards(straight_flushes, flushes)

    def __straight_and_high_cards(self, straights, high_cards):
        rank = LookupTable.__max_flush + 1
        for straight in straights:
            prime_product = Card.prime_product_from_rankbits(straight)
            self.__unsuited_lookup[prime_product] = rank
            rank += 1

        rank = LookupTable.__max_pair + 1
        for high_card in high_cards:
            prime_product = Card.prime_product_from_rankbits(high_card)
            self.__unsuited_lookup[prime_product] = rank
            rank += 1

    def __multiples(self):
        backwards_ranks = list(range(len(Card.int_ranks) - 1, -1, -1))

        # Four of a Kind
        rank = LookupTable.__max_straight_flush + 1
        for backwards_rank in backwards_ranks:
            kickers = backwards_ranks[:]
            kickers.remove(backwards_rank)
            for kicker in kickers:
                product = Card.primes[backwards_rank] ** 4 * Card.primes[kicker]
                self.__unsuited_lookup[product] = rank
                rank += 1

        # Full House
        rank = LookupTable.__max_four_of_a_kind + 1
        for backwards_rank in backwards_ranks:
            pair_ranks = backwards_ranks[:]
            pair_ranks.remove(backwards_rank)
            for pr in pair_ranks:
                product = Card.primes[backwards_rank] ** 3 * Card.primes[pr] ** 2
                self.__unsuited_lookup[product] = rank
                rank += 1

        # Three of a Kind
        rank = LookupTable.__max_straight + 1
        for backwards_rank in backwards_ranks:
            kickers = backwards_ranks[:]
            kickers.remove(backwards_rank)
            generator = itertools.combinations(kickers, 2)
            for two_kickers in generator:
                kicker1, kicker2 = two_kickers
                product = Card.primes[backwards_rank] ** 3 * Card.primes[kicker1] * Card.primes[kicker2]
                self.__unsuited_lookup[product] = rank
                rank += 1

        # Two Pair
        rank = LookupTable.__max_three_of_a_kind + 1
        two_pair_generator = itertools.combinations(tuple(backwards_ranks), 2)
        for two_pair in two_pair_generator:
            pair1, pair2 = two_pair
            kickers = backwards_ranks[:]
            kickers.remove(pair1)
            kickers.remove(pair2)
            for kicker in kickers:
                product = Card.primes[pair1] ** 2 * Card.primes[pair2] ** 2 * Card.primes[kicker]
                self.__unsuited_lookup[product] = rank
                rank += 1

        # Pair
        rank = LookupTable.__max_two_pair + 1
        for pair_rank in backwards_ranks:
            kickers = backwards_ranks[:]
            kickers.remove(pair_rank)
            generator = itertools.combinations(tuple(kickers), 3)
            for three_kickers in generator:
                kicker1, kicker2, kicker3 = three_kickers
                product = Card.primes[pair_rank] ** 2 * Card.primes[kicker1] * Card.primes[kicker2] * Card.primes[kicker3]
                self.__unsuited_lookup[product] = rank
                rank += 1

    @staticmethod
    def __get_lexicographically_next_bit_sequence(bits: int) -> Iterator[int]:
        t = int((bits | (bits - 1))) + 1
        next_bit_sequence = t | ((int(((t & -t) / (bits & -bits))) >> 1) - 1)
        yield next
        while True:
            t = (next_bit_sequence | (next_bit_sequence - 1)) + 1
            next_bit_sequence = t | ((((t & -t) // (next_bit_sequence & -next_bit_sequence)) >> 1) - 1)
            yield next
