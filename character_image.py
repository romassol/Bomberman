from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
from PyQt5.Qt import Qt


class Character_image(QPushButton):
    def __init__(self, parent, character, size_square, image):
        super().__init__(parent)
        self.character = character
        self.position = character.position
        self.set_picture(size_square, image)

    def set_picture(self, size_square, image):
        self.setGeometry(
            self.position.x * size_square,
            self.position.y * size_square,
            size_square,
            size_square
        )
        self.pixmap = QIcon(image)
        self.setIcon(self.pixmap)
        self.setIconSize(QSize(size_square, size_square))
        self.setStyleSheet("QPushButton {border:none; "
                           "background-color:transparent;}")
        self.show()
