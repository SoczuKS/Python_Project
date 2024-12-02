import AI

class BankruptError(Exception):
    def __init__(self, message):
        self.message = message

class Player:
    __ai_player_id = 1

    def __init__(self, money, ai: bool = False):
        if ai:
            self.name = "CPU " + str(Player.__ai_player_id)
            Player.__ai_player_id += 1
            self.__ai = AI.create_ai()
        else:
            self.name = "Player"
            self.__ai = None
        self.__money = money
        self.__cards = []
        self.__folded = False
        self.__hand_value = -1
        self.__bet_pot = 0
        self.__checked = False
        self.__all_in = False

    def get_name(self):
        return self.name

    def is_ai(self):
        return self.__ai is not None

    def get_money(self):
        return self.__money

    def new_deal(self):
        self.__folded = False
        self.__all_in = False
        self.__cards = []
        self.__hand_value = -1
        self.new_bet()

    def new_bet(self):
        self.__checked = self.__all_in or self.__folded
        self.__bet_pot = 0
