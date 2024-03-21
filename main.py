from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("rectangles")
        self.setGeometry(300, 300, 500, 500)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


def application():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    application()
