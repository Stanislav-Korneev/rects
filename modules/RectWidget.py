import random

from PyQt6.QtCore import Qt, QRect, QSize, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QMouseEvent
from PyQt6.QtWidgets import QWidget, QPushButton


class RectWidget(QWidget):
    movementSignal = pyqtSignal(object, QMouseEvent)
    connectionSignal = pyqtSignal(object)

    def __init__(self, parent=None, pos=QPoint(50, 50), config=None):
        super().__init__(parent)
        self.config = config
        self.width = config['rectWidth']
        self.height = config['rectHeight']
        self.color = random.choice(config['rectColors'])
        self.linkedRectWidgets = []
        self.lastMousePosition = None

        self.createConnectionButton()
        self.positionSelf(pos)
        self.show()

    def createConnectionButton(self):
        connectionBtn = QPushButton(self)
        connectionBtnSize = self.config['connectionButtonSize']
        btnPosX = int((self.width - connectionBtnSize) / 2)
        btnPosY = int((self.height - connectionBtnSize) / 2)
        connectionBtn.setGeometry(btnPosX, btnPosY, connectionBtnSize, connectionBtnSize)
        connectionBtn.clicked.connect(lambda: self.connectionSignal.emit(self))
        connectionBtn.show()

    def positionSelf(self, pos):
        posX = int(pos.x() - self.width / 2)
        posY = int(pos.y() - self.height / 2)
        self.setGeometry(QRect(QPoint(posX, posY), QSize(self.width, self.height)))

    def handleMove(self, eventPosition, delta):
        self.lastMousePosition = eventPosition
        self.move(self.pos() + delta)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(self.color))

    def mousePressEvent(self, event):
        if event.buttons() != Qt.MouseButton.LeftButton:
            return
        self.lastMousePosition = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.MouseButton.LeftButton or self.lastMousePosition is None:
            return

        self.movementSignal.emit(self, event)

    def mouseReleaseEvent(self, event):
        self.lastMousePosition = None
