import random
import time
from threading import Timer
from typing import List, Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor
from PySide6.QtWidgets import QTableView, QLabel

from Card import Card
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
        self.__players_table: Optional[QTableView] = None
        self.__community_cards_table: Optional[QTableView] = None
        self.__deal_pot_label: Optional[QLabel] = None

        self.__init_players()

        self.__deck = Deck()
        self.__community_cards: List[Card] = []
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

    def start(self, players_table: QTableView, community_cards_table: QTableView, deal_pot_label: QLabel):
        self.__players_table = players_table
        self.__community_cards_table = community_cards_table
        self.__deal_pot_label = deal_pot_label
        self.__new_deal()

    def fold(self):
        if self.__players[self.__next_player_index].is_ai():
            return
        self.__players[self.__next_player_index].fold()

        if self.__count_not_folded_players() == 1:
            self.__check_winner()
            return

        if self.__next_player_index == self.__last_raiser_index:
            self.__next_stage(self.__everybody_all_in())
        else:
            self.__next_player()

    def raise_bet(self, value, all_in=False):
        if self.__players[self.__next_player_index].is_ai() or value < self.__min_raise_value:
            return
        if not self.__raise_counter < Game.__max_bet_raises:
            return
        if not all_in and self.__players[self.__next_player_index].get_money() + self.__players[self.__next_player_index].get_bet_pot() < value:
            return

        self.__raise_counter += 1
        self.__players[self.__next_player_index].bet(value)
        self.__call_value = value
        self.__min_raise_value = value * 2

        if self.__raise_counter == Game.__max_bet_raises:
            self.__players[self.__next_player_index].check()

        self.__last_raiser_index = self.__next_player_index
        self.__next_player()

    def all_in(self):
        if self.__players[self.__next_player_index].is_ai():
            return
        self.raise_bet(self.__players[self.__next_player_index].get_money() + self.__players[self.__next_player_index].get_bet_pot(), True)

    def call_check(self):
        if self.__players[self.__next_player_index].is_ai():
            return

        if self.__call_value == self.__players[self.__next_player_index].get_bet_pot():
            if self.__next_player_index == self.__last_raiser_index:
                self.__next_stage()
                return
            self.__players[self.__next_player_index].check()

            if self.__everybody_checked():
                self.__next_stage()
            else:
                self.__next_player()
        else:
            self.__players[self.__next_player_index].bet(self.__call_value)
            if self.__everybody_all_in():
                self.__next_stage(True)
            else:
                self.__next_player()

    def __init_players(self):
        self.__players: List[Player] = []
        self.__players.append(Player(Game.__start_money, False))
        for i in range(Game.__ai_players_count):
            self.__players.append(Player(Game.__start_money, True))
        random.shuffle(self.__players)

    def __update_players_table(self):
        model = QStandardItemModel()

        model.setRowCount(len(self.__players))
        model.setColumnCount(7)
        model.setHorizontalHeaderLabels(['', 'Name', 'Money', 'Bet', 'Card', 'Card', 'Button'])

        for i, player in enumerate(self.__players):
            if i == self.__next_player_index:
                turn_item = QStandardItem("•")
                turn_item.setForeground(QColor("yellow"))
                model.setItem(i, 0, turn_item)
            model.setItem(i, 1, QStandardItem(player.get_name()))
            money_item = QStandardItem(f"${player.get_money()}")
            money_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            model.setItem(i, 2, money_item)
            bet_pot_item = QStandardItem(f"${player.get_bet_pot()}")
            bet_pot_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            model.setItem(i, 3, bet_pot_item)
            if not player.is_ai():
                cards = player.get_cards()
                card_1_item = QStandardItem(f"{cards[0]}")
                card_1_item.setForeground(QColor(cards[0].get_color()))
                card_1_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                card_2_item = QStandardItem(f"{cards[1]}")
                card_2_item.setForeground(QColor(cards[1].get_color()))
                card_2_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                model.setItem(i, 4, card_1_item)
                model.setItem(i, 5, card_2_item)
            button_str = "SB" if i == self.__small_blind_player_index else ("BB" if i == self.__big_blind_player_index else "")
            if i == self.__dealer_player_index:
                button_str += " D"
            model.setItem(i, 6, QStandardItem(button_str))

        self.__players_table.setModel(model)
        self.__players_table.setColumnWidth(0, 10)
        self.__players_table.setColumnWidth(1, 70)
        self.__players_table.setColumnWidth(2, 80)
        self.__players_table.setColumnWidth(3, 80)
        self.__players_table.setColumnWidth(4, 45)
        self.__players_table.setColumnWidth(5, 45)
        self.__players_table.setColumnWidth(6, 60)

    def __update_community_cards_table(self):
        model = QStandardItemModel()

        model.setRowCount(1)
        model.setColumnCount(5)

        for i, community_card in enumerate(self.__community_cards):
            model.setItem(0, i, QStandardItem(f"{community_card}"))

        self.__community_cards_table.setModel(model)

    def __new_deal(self):
        self.__deck.shuffle()
        for p in self.__players:
            p.new_deal()
        self.__draw_cards()
        self.__community_cards.clear()

        self.__stage = Game.__Stage.pre_flop
        self.__deal_pot = 0
        self.__deal_pot_label.setText(f"${self.__deal_pot}")
        self.__raise_counter = 0
        self.__call_value = self.__big_blind
        self.__min_raise_value = self.__big_blind * 2
        self.__move_blinds_ahead()
        self.__last_raiser_index = self.__big_blind_player_index
        self.__next_player_index = self.__big_blind_player_index

        self.__players[self.__small_blind_player_index].bet(self.__small_blind)
        self.__players[self.__big_blind_player_index].bet(self.__big_blind)

        self.__next_player()
        self.__update_players_table()
        self.__update_community_cards_table()

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

            if (self.__next_player_index == self.__last_raiser_index) and self.__players[self.__next_player_index].has_played_all_in():
                return self.__next_stage()

            if (self.__next_player_index == self.__last_raiser_index) and self.__raise_counter == Game.__max_bet_raises:
                return self.__next_stage()

        while self.__players[self.__next_player_index].has_folded() or self.__players[self.__next_player_index].has_played_all_in():
            self.__next_player_index = (self.__next_player_index + 1) % len(self.__players)

        self.__update_players_table()

        if self.__players[self.__next_player_index].is_ai():
            timer = Timer(2, self.__make_ai_move)
            timer.start()

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

        self.__deal_pot_label.setText(f"${self.__deal_pot}")
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

    def __everybody_checked(self):
        return all([p.has_checked() for p in self.__players])

    def __count_not_folded_players(self):
        return len([p for p in self.__players if not p.has_folded()])

    def __make_ai_move(self):
        self.__players[self.__next_player_index].make_ai_move(self)
