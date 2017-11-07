import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QPushButton, QAction
from PyQt5.QtGui import QPainter
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon

from level import Level
from game import Game
from CentralWidget import CentralWidget
from Scoreboard import Scoreboard
from ScoringWindow import ScoringWindow


class Visualization(QMainWindow):
    def __init__(self, file_names):
        super().__init__()
        self.file_names = file_names
        all_levels = []
        for f in file_names:
            all_levels.append(Level(f))
        self.game = Game(all_levels, 5, 'game1')
        self.height = 768
        self.width = 1366

        self.scoreboard = Scoreboard()
        self.score_window = ScoringWindow(self.scoreboard, self, self.game.game_type)
        self.central_widget = CentralWidget(self, self.game, self.height, self.width, self.score_window, self.scoreboard)
        self.setGeometry(0, 25, self.central_widget.size_window[0], self.central_widget.size_window[1])
        self.setCentralWidget(self.central_widget)

        newAction = QAction(QIcon('new.png'), '&New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New document')
        newAction.triggered.connect(self.new_game)

        scores = QAction(QIcon('new.png'), '&Table scores', self)
        scores.setShortcut('Ctrl+S')
        scores.setStatusTip('Show scores table')
        scores.triggered.connect(self.show_scores)

        # Create menu bar and add action
        menuBar = self.menuBar()
        file_menu = menuBar.addMenu('&Game')
        file_menu.addAction(newAction)
        score_menu = menuBar.addMenu('&Scores')
        score_menu.addAction(scores)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.score_window = ScoringWindow(self.scoreboard, self, self.game.game_type)
        self.setGeometry(0, 25, self.central_widget.size_window[0], self.central_widget.size_window[1])
        self.setCentralWidget(self.central_widget)
        qp.end()

    def new_game(self):
        all_levels = []
        for f in self.file_names:
            all_levels.append(Level(f))
        self.game = Game(all_levels, 5, 'game1')
        self.central_widget = CentralWidget(self, self.game, self.height, self.width, self.score_window, self.scoreboard)

    def show_scores(self):
        self.score_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Visualization(["level2.txt", "level1.txt"])
    ex.show()
    sys.exit(app.exec_())
