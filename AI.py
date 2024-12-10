import random


def create_ai():
    ai_type = random.randint(AI.AI_TYPE_CAREFULLY, AI.AI_TYPE_AGGRESSIVE)
    return AI(ai_type)


class AI:
    AI_TYPE_CAREFULLY = 0
    AI_TYPE_NORMAL = 1
    AI_TYPE_AGGRESSIVE = 2

    def __init__(self, ai_type):
        self.__ai_type = ai_type

    def make_move(self, game, player):
        pass
