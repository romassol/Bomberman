from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QApplication, QInputDialog


class WhatName(QInputDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.lbl = QLabel(self)
        qle = QLineEdit(self)

        qle.move(60, 100)
        self.lbl.move(60, 40)

        qle.textChanged[str].connect(self.onChanged)

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Введите ваше имя')
        # self.show()

    def onChanged(self, name):
        self.lbl.setText(name)
        self.lbl.adjustSize()