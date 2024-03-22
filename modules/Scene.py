from PyQt6.QtCore import Qt, QRect, QSize, QPoint
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtWidgets import QWidget

from modules.RectWidget import RectWidget


class Scene(QWidget):
    def __init__(self, config):
        super().__init__()
        # when you click the central button of RectWidget and connectWidget == None, it gets recorded to connectWidget
        # otherwise it will use connectWidget to add/remove connection between them
        self.connectWidget = None
        self.config = config

    def nullifyConnectWidget(self):
        if not self.connectWidget:
            return
        self.connectWidget.setStyleSheet('')
        self.connectWidget = None

    def addRect(self, pos):
        size = QSize(self.config['rectWidth'], self.config['rectHeight'])
        halfRectSize = QPoint(int(self.config['rectWidth'] / 2), int(self.config['rectHeight'] / 2))
        adjustedPos = pos - halfRectSize
        # we need testRect to be sure that there's enough place for a real widget to appear
        testRect = QRect(adjustedPos, size)
        if self.hasRectCollisions(None, testRect):
            return
        newWidget = RectWidget(self, pos, self.config)
        newWidget.movementSignal.connect(self.handleMovementSignal)
        newWidget.connectionSignal.connect(self.handleConnection)

    def handleMovementSignal(self, rectWidget, event):
        # we're handling here the signal that one of the rects (rectWidget) gave us.
        # the event is QMouseEvent and contains info about cursor position
        eventPosition = event.globalPosition().toPoint()
        delta = eventPosition - rectWidget.lastMousePosition
        # we need testRect to look for possible collisions while moving the rect
        testRect = QRect(rectWidget.pos() + delta, QSize(rectWidget.width, rectWidget.height))
        if self.hasRectCollisions(rectWidget, testRect):
            return
        rectWidget.handleMove(eventPosition, delta)
        self.update()

    def hasRectCollisions(self, testWidget, testRect):
        # testWidget is the widget that wants to move
        # testRect simulates its movement, so we can check if it collides with anything while moving
        hasWindowCollision = not self.rect().contains(testRect)
        if hasWindowCollision:
            return True

        rectWidgets = self.findChildren(RectWidget)
        return any(
            (not testWidget or rectWidget != testWidget)
            and rectWidget.geometry().intersects(testRect) for rectWidget in rectWidgets)

    def drawConnections(self, painter):
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
        self.drawConnections(painter)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # if we click on scene but not on rects, we abort connection/disconnection process
            self.nullifyConnectWidget()

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            # if we click on scene but not on rects, we abort connection/disconnection process
            self.nullifyConnectWidget()
            self.addRect(event.pos())
