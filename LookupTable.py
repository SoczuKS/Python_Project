import itertools

from Rank import Rank


def _get_lexicographically_next_bit_sequence(bits):
    t = int((bits | (bits - 1))) + 1
    next_value = t | ((int(((t & -t) / (bits & -bits))) >> 1) - 1)
    yield next_value
    while True:
        t = (next_value | (next_value - 1)) + 1
        next_value = t | ((((t & -t) // (next_value & -next_value)) >> 1) - 1)
        yield next_value


def _prime_product_from_rank_bits(rank_bits):
    product = 1
    for rank in Rank:
        if rank.value['bit_value'] & rank_bits:
            product *= rank.value['prime']
    return product


class LookupTable:
    max_royal_flush = 1
    max_straight_flush = 10
    max_four_of_a_kind = 166
    max_full_house = 322
    max_flush = 1599
    max_straight = 1609
    max_three_of_a_kind = 2467
    max_two_pair = 3325
    max_pair = 6185
    max_high_card = 7462

    def __init__(self):
        self.__flush_lookup = {}
        self.__unsuited_lookup = {}

        self.__create_flush_lookup()
        self.__multiples()

    def flush_lookup(self, prime_product):
        return self.__flush_lookup[prime_product]

    def unsuited_lookup(self, prime_product):
        return self.__unsuited_lookup[prime_product]

    def __create_flush_lookup(self):
        straight_flushes = [0b1111100000000, 0b111110000000, 0b11111000000, 0b1111100000, 0b111110000, 0b11111000, 0b1111100, 0b111110, 0b11111, 0b1000000001111]

        flushes = []
        generator = _get_lexicographically_next_bit_sequence(0b11111)

        for i in range(1277 + len(straight_flushes) - 1):
            flush = next(generator)
            not_straight_flush = True
            for straight_flush in straight_flushes:
                if not flush ^ straight_flush:
                    not_straight_flush = False

            if not_straight_flush:
                flushes.append(flush)

        flushes.reverse()

        rank = 1
        rank_2 = LookupTable.max_flush + 1
        for straight_flush in straight_flushes:
            prime_product = _prime_product_from_rank_bits(straight_flush)
            self.__flush_lookup[prime_product] = rank
            self.__unsuited_lookup[prime_product] = rank_2
            rank += 1
            rank_2 += 1

        rank = LookupTable.max_full_house + 1
        rank_2 = LookupTable.max_pair + 1
        for flush in flushes:
            prime_product = _prime_product_from_rank_bits(flush)
            self.__flush_lookup[prime_product] = rank
            self.__unsuited_lookup[prime_product] = rank_2
            rank += 1
            rank_2 += 1

    def __multiples(self):
        backwards_ranks = list(Rank)[::-1]

        rank = LookupTable.max_straight_flush + 1
        for backward_rank in backwards_ranks:
            kickers = backwards_ranks[:]
            kickers.remove(backward_rank)
            for kicker in kickers:
                product = backward_rank.value['prime'] ** 4 * kicker.value['prime']
                self.__unsuited_lookup[product] = rank
                rank += 1

        rank = LookupTable.max_four_of_a_kind + 1
        for backward_rank in backwards_ranks:
            pair_ranks = backwards_ranks[:]
            pair_ranks.remove(backward_rank)
            for pair_rank in pair_ranks:
                product = backward_rank.value['prime'] ** 3 * pair_rank.value['prime'] ** 2
                self.__unsuited_lookup[product] = rank
                rank += 1

        rank = LookupTable.max_straight + 1
        for backward_rank in backwards_ranks:
            kickers = backwards_ranks[:]
            kickers.remove(backward_rank)
            generator = itertools.combinations(kickers, 2)
            for kicker_2_combination in generator:
                kicker1, kicker2 = kicker_2_combination
                product = backward_rank.value['prime'] ** 3 * kicker1.value['prime'] * kicker2.value['prime']
                self.__unsuited_lookup[product] = rank
                rank += 1

        rank = LookupTable.max_three_of_a_kind + 1
        rank_tuple_generator = itertools.combinations(tuple(backwards_ranks), 2)
        for rank_tuple in rank_tuple_generator:
            pair1, pair2 = rank_tuple
            kickers = backwards_ranks[:]
            kickers.remove(pair1)
            kickers.remove(pair2)
            for kicker in kickers:
                product = pair1.value['prime'] ** 2 * pair2.value['prime'] ** 2 * kicker.value['prime']
                self.__unsuited_lookup[product] = rank
                rank += 1

        rank = LookupTable.max_two_pair + 1
        for pair_rank in backwards_ranks:
            kickers = backwards_ranks[:]
            kickers.remove(pair_rank)
            generator = itertools.combinations(tuple(kickers), 3)
            for kicker_3_combination in generator:
                kicker1, kicker2, kicker3 = kicker_3_combination
                product = pair_rank.value['prime'] ** 2 * kicker1.value['prime'] * kicker2.value['prime'] * kicker3.value['prime']
                self.__unsuited_lookup[product] = rank
                rank += 1
