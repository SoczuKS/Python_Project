import random


def create_ai():
    ai_type = random.randint(AI.AI_TYPE_CAREFULLY, AI.AI_TYPE_AGGRESSIVE)
    return AI(ai_type)


def _make_move_carefully(game, player):
    can_check = game.get_call_value() == player.get_bet_pot()
    must_all_in = game.get_call_value() >= (player.get_money() + player.get_bet_pot())

    if can_check:
        game.call_check(True)
    elif must_all_in:
        game.fold(True)
    else:
        if game.get_call_value() < player.get_money() // 4:
            game.call_check(True)
        else:
            game.fold(True)


def _make_move_normal(game, player):
    can_check = game.get_call_value() == player.get_bet_pot()
    must_all_in = game.get_call_value() >= (player.get_money() + player.get_bet_pot())
    can_raise = game.can_raise() and not must_all_in

    if must_all_in:
        game.fold(True)
    elif can_check and can_raise:
        game.raise_bet(game.get_min_raise_value(), made_by_ai=True)
    else:
        game.call_check(True)


def _make_move_aggressive(game, player):
    can_check = game.get_call_value() == player.get_bet_pot()
    must_all_in = game.get_call_value() >= (player.get_money() + player.get_bet_pot())
    can_raise = game.can_raise() and not must_all_in

    if must_all_in:
        game.call_check(True)
    elif can_check and can_raise:
        game.raise_bet(game.get_min_raise_value(), made_by_ai=True)
    else:
        game.call_check(True)


class AI:
    AI_TYPE_CAREFULLY = 0
    AI_TYPE_NORMAL = 1
    AI_TYPE_AGGRESSIVE = 2

    def __init__(self, ai_type):
        self.__ai_type = ai_type

    def make_move(self, game, player):
        if self.__ai_type == AI.AI_TYPE_CAREFULLY:
            _make_move_carefully(game, player)
        elif self.__ai_type == AI.AI_TYPE_NORMAL:
            _make_move_normal(game, player)
        elif self.__ai_type == AI.AI_TYPE_AGGRESSIVE:
            _make_move_aggressive(game, player)
