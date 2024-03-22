import json
import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from modules.Scene import Scene
from modules.MainWindow import MainWindow


def application():
    with open('config.json', 'r') as file:
        config = json.loads(file.read())

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icons/rect_icon.png'))
    window = MainWindow(config)
    scene = Scene(config)
    window.layout().addWidget(scene)

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    application()
