from PySide6.QtWidgets import QWidget, QTableView

from window_form import Ui_MainWidget


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)
        self.ui.raise_value_slider.valueChanged.connect(self.__raise_value_slider_changed)

    def connect_fold_button(self, slot):
        self.ui.fold_button.clicked.connect(slot)

    def connect_call_check_button(self, slot):
        self.ui.call_check_button.clicked.connect(slot)

    def connect_allin_button(self, slot):
        self.ui.allin_button.clicked.connect(slot)

    def connect_raise_button(self, slot):
        self.ui.raise_button.clicked.connect(slot)

    def __raise_value_slider_changed(self, value):
        self.ui.raise_value_label.setText(f"${value}")

    def get_players_table(self) -> QTableView:
        return self.ui.players_table

    def get_community_cards_table(self) -> QTableView:
        return self.ui.community_cards_table

    def get_deal_pot_label(self):
        return self.ui.deal_pot_label

    def get_winner_label(self):
        return self.ui.winner_label

    def get_raise_value(self):
        return self.ui.raise_value_slider.value()
