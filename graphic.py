import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter
from PyQt5.Qt import Qt

from level import Level
from central_widget import Central_widget


class Visualization(QMainWindow):
    def __init__(self, file_name):
        super().__init__()
        self.level = Level(file_name)
        self.height = 768
        self.width = 1366

        self.central_widget = Central_widget(
            self,
            self.level,
            self.height,
            self.width
        )
        self.setGeometry(
            0,
            25,
            self.central_widget.size_window[0],
            self.central_widget.size_window[1]
        )
        self.setCentralWidget(self.central_widget)
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Visualization("input_test.txt")
    sys.exit(app.exec_())
