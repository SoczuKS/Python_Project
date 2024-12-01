import sys
from PySide6.QtWidgets import QApplication
from Window import Window


class Application:
    def __init__(self):
        self.qtApp = QApplication(sys.argv)
        self.window = Window()

    def run(self):
        self.window.show()
        sys.exit(self.qtApp.exec())