import sys

from PySide6.QtWidgets import QApplication

from Game import Game
from Window import Window


class Application:
    def __init__(self):
        self.__game = None
        self.__qt_app = QApplication(sys.argv)
        self.__window = Window()
        self.__window.connect_fold_button(self.__fold_button_clicked)
        self.__window.connect_raise_button(self.__raise_button_clicked)
        self.__window.connect_allin_button(self.__allin_button_clicked)
        self.__window.connect_check_button(self.__check_button_clicked)

    def run(self):
        self.__window.show()
        self.__game = Game()
        self.__start_game()
        sys.exit(self.__qt_app.exec())

    def __fold_button_clicked(self):
        print("Fold button clicked")

    def __raise_button_clicked(self):
        print("Raise button clicked")

    def __allin_button_clicked(self):
        print("All-in button clicked")

    def __check_button_clicked(self):
        print("Check button clicked")

    def __start_game(self):
        self.__game.start(self.__window.get_players_table(), self.__window.get_community_cards_table(), self.__window.get_deal_pot_label())
