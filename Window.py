from PySide6.QtWidgets import QWidget
from window_form import Ui_MainWidget

class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)
