from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
from PyQt5.Qt import Qt


class IconImage(QPushButton):
    def __init__(self, parent, position, size, image):
        super().__init__(parent)
        self.position = position
        self.set_picture(size, image)

    def set_picture(self, size, image):
        self.setGeometry(
            self.position.x * size,
            self.position.y * size,
            size,
            size
        )
        self.pixmap = QIcon(image)
        self.setIcon(self.pixmap)
        self.setIconSize(QSize(size, size))
        self.setStyleSheet("QPushButton {border:none; "
                           "background-color:transparent;}")
        self.show()
