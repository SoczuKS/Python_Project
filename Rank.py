from enum import Enum


class Rank(Enum):
    TWO = {"bit_value": 0b0000000000001, "rank_value": 0, "prime": 2}
    THREE = {"bit_value": 0b0000000000010, "rank_value": 1, "prime": 3}
    FOUR = {"bit_value": 0b0000000000100, "rank_value": 2, "prime": 5}
    FIVE = {"bit_value": 0b0000000001000, "rank_value": 3, "prime": 7}
    SIX = {"bit_value": 0b0000000010000, "rank_value": 4, "prime": 11}
    SEVEN = {"bit_value": 0b0000000100000, "rank_value": 5, "prime": 13}
    EIGHT = {"bit_value": 0b0000001000000, "rank_value": 6, "prime": 17}
    NINE = {"bit_value": 0b0000010000000, "rank_value": 7, "prime": 19}
    TEN = {"bit_value": 0b0000100000000, "rank_value": 8, "prime": 23}
    JACK = {"bit_value": 0b0001000000000, "rank_value": 9, "prime": 29}
    QUEEN = {"bit_value": 0b0010000000000, "rank_value": 10, "prime": 31}
    KING = {"bit_value": 0b0100000000000, "rank_value": 11, "prime": 37}
    ACE = {"bit_value": 0b1000000000000, "rank_value": 12, "prime": 41}

    def __str__(self):
        string_representation = {Rank.TWO: "2", Rank.THREE: "3", Rank.FOUR: "4", Rank.FIVE: "5", Rank.SIX: "6", Rank.SEVEN: "7", Rank.EIGHT: "8", Rank.NINE: "9", Rank.TEN: "10",
                                 Rank.JACK: "J", Rank.QUEEN: "Q", Rank.KING: "K", Rank.ACE: "A"}
        return string_representation[self]
