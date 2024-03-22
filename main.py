import json
import random
import sys

from PyQt6.QtCore import Qt, QRect, QSize, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QMouseEvent
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton


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


class Scene(QWidget):
    def __init__(self, config):
        super().__init__()
        self.connectWidget = None
        self.config = config

    def addRect(self, pos):
        size = QSize(self.config['rectWidth'], self.config['rectHeight'])
        testRect = QRect(pos, size)
        if self.hasRectCollisions(None, testRect):
            return
        newWidget = RectWidget(self, pos, self.config)
        newWidget.movementSignal.connect(self.handleMovementSignal)
        newWidget.connectionSignal.connect(self.handleConnection)

    def handleMovementSignal(self, rectWidget, event):
        eventPosition = event.globalPosition().toPoint()
        delta = eventPosition - rectWidget.lastMousePosition
        testRect = QRect(rectWidget.pos() + delta, QSize(rectWidget.width, rectWidget.height))
        if self.hasRectCollisions(rectWidget, testRect):
            return
        rectWidget.handleMove(eventPosition, delta)
        self.update()

    def hasRectCollisions(self, testWidget, testRect):
        hasWindowCollision = not self.rect().contains(testRect)
        if hasWindowCollision:
            return True

        rectWidgets = self.findChildren(RectWidget)
        return any(
            (not testWidget or rectWidget != testWidget)
            and rectWidget.geometry().intersects(testRect) for rectWidget in rectWidgets)

    def drawLines(self, painter):
        for rectWidget in self.findChildren(RectWidget):
            for linkedRect in rectWidget.linkedRectWidgets:
                painter.drawLine(rectWidget.geometry().center(), linkedRect.geometry().center())

    def handleConnection(self, targetWidget):
        if not self.connectWidget or self.connectWidget == targetWidget:
            self.connectWidget = targetWidget
            return

        connectHasTarget = targetWidget in self.connectWidget.linkedRectWidgets
        targetHasConnect = self.connectWidget in targetWidget.linkedRectWidgets

        if connectHasTarget:
            self.connectWidget.linkedRectWidgets.remove(targetWidget)
        elif targetHasConnect:
            targetWidget.linkedRectWidgets.remove(self.connectWidget)
        else:
            self.connectWidget.linkedRectWidgets.append(targetWidget)

        self.connectWidget = None
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor(self.config['connectorColor']))
        pen.setWidth(self.config['connectorWidth'])
        painter.setPen(pen)

        painter.fillRect(self.rect(), QColor(self.config['sceneBackground']))
        self.drawLines(painter)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.connectWidget = None

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.connectWidget = None
            self.addRect(event.pos())


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
