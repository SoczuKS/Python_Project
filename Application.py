import sys

from PySide6.QtWidgets import QApplication

from Game import Game
from Window import Window


class Application:
    def __init__(self):
        self.__game = Game()
        self.__qt_app = QApplication(sys.argv)
        self.__window = Window()
        self.__window.connect_fold_button(self.__fold_button_clicked)
        self.__window.connect_raise_button(self.__raise_button_clicked)
        self.__window.connect_allin_button(self.__allin_button_clicked)
        self.__window.connect_call_check_button(self.__call_check_button_clicked)

    def run(self):
        self.__window.show()
        self.__start_game()
        sys.exit(self.__qt_app.exec())

    def __fold_button_clicked(self):
        self.__game.fold()

    def __raise_button_clicked(self):
        value = self.__window.get_raise_value()
        self.__game.raise_bet(value)

    def __allin_button_clicked(self):
        self.__game.all_in()

    def __call_check_button_clicked(self):
        self.__game.call_check()

    def __start_game(self):
        self.__game.start(self.__window.get_players_table(), self.__window.get_community_cards_table(), self.__window.get_deal_pot_label())
