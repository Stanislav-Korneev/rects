import json
import sys

from PyQt6.QtWidgets import QApplication

from Scene import Scene
from MainWindow import MainWindow


def application():
    with open('config.json', 'r') as file:
        config = json.loads(file.read())

    app = QApplication(sys.argv)
    window = MainWindow(config)
    scene = Scene(config)
    window.layout().addWidget(scene)

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    application()
