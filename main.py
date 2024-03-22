from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import Qt, QRect, QSize, QPoint

import sys


class ConnectionButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.size = 15
        posX = int((parent.width - self.size) / 2)
        posY = int((parent.height - self.size) / 2)
        self.setGeometry(posX, posY, self.size, self.size)


class RectWidget(QWidget):
    def __init__(self, parent=None, pos=QPoint(50, 50)):
        super().__init__(parent)
        self.linkedRectWidgets = []
        self.width = 100
        self.height = 50
        self.lastMousePosition = None

        self.connectionBtn = ConnectionButton(self)
        posX = int(pos.x() - self.width / 2)
        posY = int(pos.y() - self.height / 2)
        self.setGeometry(QRect(QPoint(posX, posY), QSize(self.width, self.height)))
        self.connectionBtn.clicked.connect(lambda: parent.handleConnection(self))

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor('red'))

    def mousePressEvent(self, event):
        if event.buttons() != Qt.MouseButton.LeftButton:
            return
        self.lastMousePosition = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.MouseButton.LeftButton or self.lastMousePosition is None:
            return

        delta = event.globalPosition().toPoint() - self.lastMousePosition
        rect = QRect(self.pos() + delta, QSize(self.width, self.height))
        if self.parent().hasRectCollisions(self, rect):
            return
        self.lastMousePosition = event.globalPosition().toPoint()
        self.move(self.pos() + delta)
        self.parent().update()

    def mouseReleaseEvent(self, event):
        self.lastMousePosition = None


class Scene(QWidget):
    def __init__(self):
        super().__init__()
        self.connectWidget = None

    def addRect(self, pos):
        size = QSize(100, 50)
        rect = QRect(pos, size)
        if self.hasRectCollisions(None, rect):
            return
        RectWidget(self, pos)

    def hasRectCollisions(self, targetWidget, targetRect):
        hasWindowCollision = not self.rect().contains(targetRect)
        if hasWindowCollision:
            return True
        rects = self.findChildren(RectWidget)
        hasRectCollision = any((not targetWidget or rect != targetWidget) and rect.geometry().intersects(targetRect) for rect in rects)
        return hasRectCollision

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor('black'))
        pen.setWidth(5)
        painter.setPen(pen)

        painter.fillRect(self.rect(), QColor('lightBlue'))
        self.drawLines(painter)

    def drawLines(self, painter):
        for rect in self.findChildren(RectWidget):
            for linkedRect in rect.linkedRectWidgets:
                painter.drawLine(rect.geometry().center(), linkedRect.geometry().center())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.connectWidget = None

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.connectWidget = None
            self.addRect(event.pos())

    def handleConnection(self, targetWidget):
        if not self.connectWidget:
            self.connectWidget = targetWidget
            return

        if self.connectWidget == targetWidget:
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
