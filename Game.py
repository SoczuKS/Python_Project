import random

from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QTableView

from Deck import Deck
from HandEvaluator import HandEvaluator
from Player import Player

class Game:
    __ai_players_count = 3
    __start_money = 2000
    __max_bet_raises = 3
    __start_big_blind = 20

    class __Stage:
        pre_flop = 0
        flop = 1
        turn = 2
        river = 3

    def __init__(self):
        self.__players_table = None
        self.__community_cards_table = None
        self.__init_players()
        self.__deck = Deck()
        self.__community_cards = []
        self.__stage = Game.__Stage.pre_flop
        self.__big_blind = Game.__start_big_blind
        self.__small_blind = self.__big_blind // 2
        self.__started = False
        self.__deal_started = False
        self.__deal_pot = 0
        self.__raise_counter = 0
        self.__call_value = self.__big_blind
        self.__min_raise_value = self.__big_blind * 2
        self.__dealer_player_index = -2
        self.__small_blind_player_index = -1
        self.__big_blind_player_index = 0
        self.__next_player_index = 1
        self.__last_raiser_index = 0
        self.__hand_evaluator = HandEvaluator()

    def __init_players(self):
        self.__players = []
        self.__players.append(Player(Game.__start_money, False))
        for i in range(Game.__ai_players_count):
            self.__players.append(Player(Game.__start_money, True))
        random.shuffle(self.__players)

    def __update_players_table(self):
        model = QStandardItemModel()

        model.setRowCount(len(self.__players))
        model.setColumnCount(5)
        model.setHorizontalHeaderLabels(['Name', 'Money', 'Bet', 'Hand', 'Button'])

        for i, player in enumerate(self.__players):
            model.setItem(i, 0, QStandardItem(player.get_name()))
            model.setItem(i, 1, QStandardItem(f"{player.get_money()}"))
            model.setItem(i, 2, QStandardItem(f"{player.get_bet_pot()}"))
            if not player.is_ai():
                cards = player.get_cards()
                model.setItem(i, 3, QStandardItem(f"{cards[0]} {cards[1]}"))
            model.setItem(i, 4, QStandardItem("D" if i == self.__dealer_player_index else ""))

        self.__players_table.setModel(model)

    def __update_community_cards_table(self):
        pass # TODO:

    def start(self, players_table: QTableView, community_cards_table: QTableView):
        self.__players_table = players_table
        self.__community_cards_table = community_cards_table
        self.__new_deal()

    def __new_deal(self):
        self.__deck.shuffle()
        self.__draw_cards()
        self.__update_players_table()

    def __draw_cards(self):
        for i in range(2):
            for player in self.__players:
                player.add_card(self.__deck.draw_card())
