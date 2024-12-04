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

    def connect_check_button(self, slot):
        self.ui.check_button.clicked.connect(slot)

    def connect_allin_button(self, slot):
        self.ui.allin_button.clicked.connect(slot)

    def connect_raise_button(self, slot):
        self.ui.raise_button.clicked.connect(slot)

    def __raise_value_slider_changed(self, value):
        self.ui.raise_value_label.setText(f"${value}")

    def get_players_table(self) -> QTableView:
        return self.ui.players_table
