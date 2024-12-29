import AI


class BankruptError(Exception):
    def __init__(self, message):
        self.message = message


class Player:
    __ai_player_id = 1

    def __init__(self, money, ai: bool = False):
        if ai:
            self.__name = "CPU " + str(Player.__ai_player_id)
            Player.__ai_player_id += 1
            self.__ai = AI.create_ai()
        else:
            self.__name = "Player"
            self.__ai = None
        self.__money = money
        self.__cards = []
        self.__folded = False
        self.__hand_value = -1
        self.__bet_pot = 0
        self.__checked = False
        self.__all_in = False
        self.__bankrupt = False

    def get_name(self):
        return self.__name

    def is_ai(self):
        return self.__ai is not None

    def get_money(self):
        return self.__money

    def add_money(self, money):
        self.__money += money

    def get_bet_pot(self):
        return self.__bet_pot

    def get_cards(self):
        return self.__cards

    def new_deal(self):
        self.__folded = False
        self.__all_in = False
        self.__cards = []
        self.__hand_value = -1
        self.new_bet()

    def new_bet(self):
        self.__checked = self.__all_in or self.__folded
        self.__bet_pot = 0

    def add_card(self, card):
        self.__cards.append(card)

    def bet(self, value):
        diff = value - self.__bet_pot

        if diff >= self.__money:
            return self.play_all_in()

        self.__money -= diff
        self.__bet_pot += diff

    def reset_bet_pot(self):
        self.__bet_pot = 0

    def play_all_in(self):
        self.__bet_pot += self.__money
        self.__money = 0
        self.__all_in = True
        return self.__bet_pot

    def make_ai_move(self, game):
        if self.__ai:
            self.__ai.make_move(game, self)

    def has_played_all_in(self):
        return self.__all_in

    def has_folded(self):
        return self.__folded

    def check(self):
        self.__checked = True

    def has_checked(self):
        return self.__checked

    def fold(self):
        self.__folded = True
        self.__checked = True
