from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtWidgets import QWidget

from modules.RectWidget import RectWidget


class Scene(QWidget):
    def __init__(self, config):
        super().__init__()
        self.connectWidget = None
        self.config = config

    def nullifyConnectWidget(self):
        if not self.connectWidget:
            return
        self.connectWidget.setStyleSheet('')
        self.connectWidget = None

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

        self.nullifyConnectWidget()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor(self.config['connectorColor']))
        pen.setWidth(self.config['connectorWidth'])
        painter.setPen(pen)

        if self.connectWidget:
            self.connectWidget.setStyleSheet(self.config['connectionButtonActiveStyle'])

        painter.fillRect(self.rect(), QColor(self.config['sceneBackground']))
        self.drawLines(painter)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.nullifyConnectWidget()

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.nullifyConnectWidget()
            self.addRect(event.pos())
