from Windows import GeneralSettigns
from PyQt5.QtWidgets import *
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gs = GeneralSettigns()
    gs.show()
    sys.exit(app.exec())