from PySide6.QtWidgets import QWidget
from window_form import Ui_Widget

class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
