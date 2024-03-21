from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen
from PyQt6.QtCore import Qt, QRect, QSize, QPoint, pyqtSignal, QLine

import sys


class ConnectionLine(QWidget):
    def __init__(self, parent=None, widget1=None, widget2=None):
        super().__init__(parent)
        self.startWidget = widget1
        self.endWidget = widget2
        self.startPoint = widget1.geometry().center()
        self.endPoint = widget2.geometry().center()


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

        self.connectionBtn = ConnectionButton(self)
        posX = int(pos.x() - self.width / 2)
        posY = int(pos.y() - self.height / 2)
        self.setGeometry(QRect(QPoint(posX, posY), QSize(self.width, self.height)))
        self.connectionBtn.clicked.connect(lambda: parent.handleConnection(self))

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor('red'))


class Scene(QWidget):
    def __init__(self):
        super().__init__()
        self.connectWidget = None

    def addRect(self, pos):
        RectWidget(self, pos)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor('lightBlue'))
        pen = QPen(QColor('black'))
        pen.setWidth(5)
        painter.setPen(pen)

        self.drawLines(painter)

    def drawLines(self, painter):
        lines = self.findChildren(ConnectionLine)
        for line in lines:
            painter.drawLine(line.startPoint, line.endPoint)

    def deleteLine(self, widget1, widget2):
        lines = self.findChildren(ConnectionLine)
        for line in lines:
            if (line.startWidget == widget1 and line.endWidget == widget2) \
                    or (line.startWidget == widget2 and line.endWidget == widget1):
                line.deleteLater()
                self.update()

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

        if connectHasTarget or targetHasConnect:
            self.deleteLine(self.connectWidget, targetWidget)
            if connectHasTarget:
                self.connectWidget.linkedRectWidgets.remove(targetWidget)
            if targetHasConnect:
                targetWidget.linkedRectWidgets.remove(self.connectWidget)
            self.connectWidget = None
            return

        ConnectionLine(self, self.connectWidget, targetWidget)
        self.update()
        self.connectWidget.linkedRectWidgets.append(targetWidget)
        self.connectWidget = None


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
