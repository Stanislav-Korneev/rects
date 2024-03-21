from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtGui import QPainter, QBrush, QColor
from PyQt6.QtCore import Qt, QRect, QSize, QPoint, pyqtSignal

import sys


class ConnectionButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.size = 15
        posX = int((parent.width - self.size) / 2)
        posY = int((parent.height - self.size) / 2)
        self.setGeometry(posX, posY, self.size, self.size)
        self.show()


class RectWidget(QWidget):
    def __init__(self, parent=None, pos=QPoint(50, 50)):
        super().__init__(parent)
        self.width = 100
        self.height = 50
        self.connectionBtn = ConnectionButton(self)
        posX = int(pos.x() - self.width / 2)
        posY = int(pos.y() - self.height / 2)
        self.setGeometry(QRect(QPoint(posX, posY), QSize(self.width, self.height)))

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor('red'))


class Scene(QWidget):
    def __init__(self):
        super().__init__()
        self.rects = []

    def addRect(self, pos):
        rect = RectWidget(self, pos)
        self.rects.append(rect)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor('lightBlue'))

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.addRect(event.pos())


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
    scene = Scene()
    window.layout().addWidget(scene)

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    application()
