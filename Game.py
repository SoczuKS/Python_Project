import random
import time

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor
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
        self.__hand_evaluator = HandEvaluator()

        self.__stage = Game.__Stage.pre_flop
        self.__big_blind = Game.__start_big_blind
        self.__small_blind = self.__big_blind // 2
        self.__deal_pot = 0
        self.__raise_counter = 0
        self.__call_value = self.__big_blind
        self.__min_raise_value = self.__big_blind * 2
        self.__dealer_player_index = len(self.__players) - 2
        self.__small_blind_player_index = len(self.__players) - 1
        self.__big_blind_player_index = 0
        self.__next_player_index = 1
        self.__last_raiser_index = 0

    def __init_players(self):
        self.__players = []
        self.__players.append(Player(Game.__start_money, False))
        for i in range(Game.__ai_players_count):
            self.__players.append(Player(Game.__start_money, True))
        random.shuffle(self.__players)

    def __update_players_table(self):
        model = QStandardItemModel()

        model.setRowCount(len(self.__players))
        model.setColumnCount(7)
        model.setHorizontalHeaderLabels(['Name', 'Money', 'Bet', 'Card', 'Card', 'Button', 'Turn'])

        for i, player in enumerate(self.__players):
            model.setItem(i, 0, QStandardItem(player.get_name()))
            model.setItem(i, 1, QStandardItem(f"${player.get_money()}"))
            model.setItem(i, 2, QStandardItem(f"${player.get_bet_pot()}"))
            if not player.is_ai():
                cards = player.get_cards()
                card_1_item = QStandardItem(f"{cards[0]}")
                card_1_item.setForeground(QColor(cards[0].get_color()))
                card_1_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                card_2_item = QStandardItem(f"{cards[1]}")
                card_2_item.setForeground(QColor(cards[1].get_color()))
                card_2_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                model.setItem(i, 3, card_1_item)
                model.setItem(i, 4, card_2_item)
            button_str = "SB" if i == self.__small_blind_player_index else (
                "BB" if i == self.__big_blind_player_index else "")
            if i == self.__dealer_player_index:
                button_str += " D"
            model.setItem(i, 5, QStandardItem(button_str))

        self.__players_table.setModel(model)
        self.__players_table.setColumnWidth(3, 50)
        self.__players_table.setColumnWidth(4, 50)
        self.__players_table.setColumnWidth(5, 80)
        self.__players_table.setColumnWidth(6, 40)

    def __update_community_cards_table(self):
        model = QStandardItemModel()

        model.setRowCount(1)
        model.setColumnCount(5)
        model.setHorizontalHeaderLabels(['Flop', 'Flop', 'Flop', 'River', 'Turn'])

        for i, community_card in enumerate(self.__community_cards):
            model.setItem(0, i, QStandardItem(f"{community_card}"))

        self.__community_cards_table.setModel(model)

    def start(self, players_table: QTableView, community_cards_table: QTableView):
        self.__players_table = players_table
        self.__community_cards_table = community_cards_table
        self.__new_deal()

    def __new_deal(self):
        self.__deck.shuffle()
        for p in self.__players:
            p.new_deal()
        self.__draw_cards()
        self.__community_cards.clear()

        self.__stage = Game.__Stage.pre_flop
        self.__deal_pot = 0
        self.__raise_counter = 0
        self.__call_value = self.__big_blind
        self.__min_raise_value = self.__big_blind * 2
        self.__move_blinds_ahead()
        self.__last_raiser_index = self.__big_blind_player_index
        self.__next_player_index = self.__big_blind_player_index

        self.__players[self.__small_blind_player_index].bet(self.__small_blind)
        self.__players[self.__big_blind_player_index].bet(self.__big_blind)

        self.__update_players_table()
        self.__next_player()

    def __draw_cards(self):
        for i in range(2):
            for player in self.__players:
                player.add_card(self.__deck.draw_card())

    def __move_blinds_ahead(self):
        self.__small_blind_player_index = (self.__small_blind_player_index + 1) % len(self.__players)
        self.__big_blind_player_index = (self.__small_blind_player_index + 1) % len(self.__players)
        self.__dealer_player_index = self.__small_blind_player_index if len(self.__players) == 2 else (
                (self.__small_blind_player_index - 1) % len(self.__players))

    def __next_player(self, new_bet=False, everybody_all_in=False):
        if everybody_all_in:
            return

        if new_bet:
            self.__next_player_index = self.__small_blind_player_index
        else:
            self.__next_player_index = (self.__next_player_index + 1) % len(self.__players)

            if (self.__next_player_index == self.__last_raiser_index) and self.__players[
                self.__next_player_index].has_played_all_in():
                return self.__next_stage()

            if (self.__next_player_index == self.__last_raiser_index) and self.__raise_counter == Game.__max_bet_raises:
                return self.__next_stage()

        while self.__players[self.__next_player_index].has_folded() or self.__players[
            self.__next_player_index].has_played_all_in():
            self.__next_player_index = (self.__next_player_index + 1) % len(self.__players)

        # TODO: Implement player turn

    def __next_stage(self, everybody_all_in=False):
        if everybody_all_in:
            time.sleep(2)

        if self.__stage == Game.__Stage.pre_flop:
            self.__flop(everybody_all_in)
        elif self.__stage == Game.__Stage.flop:
            self.__turn(everybody_all_in)
        elif self.__stage == Game.__Stage.turn:
            self.__river(everybody_all_in)
        elif self.__stage == Game.__Stage.river:
            self.__check_winner()
            return

        if self.__everybody_all_in():
            self.__next_stage(True)

    def __flop_turn_river_common_part(self, everybody_all_in=False):
        for p in self.__players:
            self.__deal_pot += p.get_bet_pot()
            p.new_bet()

        self.__raise_counter = 0
        self.__call_value = 0
        self.__min_raise_value = self.__big_blind
        self.__last_raiser_index = -1

        self.__next_player(True, everybody_all_in)

    def __deal_community_cards(self, count):
        for i in range(count):
            self.__community_cards.append(self.__deck.draw_card())
        self.__update_community_cards_table()

    def __flop(self, everybody_all_in=False):
        self.__stage = Game.__Stage.flop
        self.__flop_turn_river_common_part(everybody_all_in)
        self.__deal_community_cards(3)

    def __turn(self, everybody_all_in=False):
        self.__stage = Game.__Stage.turn
        self.__flop_turn_river_common_part(everybody_all_in)
        self.__deal_community_cards(1)

    def __river(self, everybody_all_in=False):
        self.__stage = Game.__Stage.river
        self.__flop_turn_river_common_part(everybody_all_in)
        self.__deal_community_cards(1)

    def __check_winner(self):
        pass  # TODO

    def __everybody_all_in(self):
        return all([p.has_played_all_in() for p in self.__players])
