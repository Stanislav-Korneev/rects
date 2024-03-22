from PyQt6.QtWidgets import QVBoxLayout, QWidget


class MainWindow(QWidget):
    def __init__(self, config):
        super().__init__()

        self.setWindowTitle(config['windowTitle'])
        self.setFixedSize(*config['windowSize'])
        self.move(*config['windowPosition'])
        self.setContentsMargins(*config['contentsMargins'])

        layout = QVBoxLayout()
        layout.setContentsMargins(*config['contentsMargins'])
        self.setLayout(layout)
