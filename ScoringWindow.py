from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QApplication, QVBoxLayout, QDialogButtonBox
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from Scoreboard import Scoreboard
import operator


class ScoringWindow(QDialog):
    _TEMPLATE = """<html>
        <head>
            <style>
                table {{
                    border: 3px double black;
                    width: 100%;
                }}

                td.place {{ text-align: center; }}
                td.name {{ }}
                td.score {{ font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1 align='center'>{}</h1>
            <table>{}</table>
        </body>
    </html>"""

    _ROW_TEMPLATE = """<tr>
    <td class='place'>{}</td>
    <td class='name'>{}</td>
    <td class='score'>{}</td>
    </tr>"""

    def __init__(self, scoreboard, parent, game_name):
        super().__init__(parent)
        self.scoreboard = scoreboard

        self._viewer = QWebEngineView()

        self._btns = QDialogButtonBox(QDialogButtonBox.Ok)
        self._btns.accepted.connect(self.close)

        box_layout = QVBoxLayout()
        box_layout.addWidget(self._viewer)
        box_layout.addWidget(self._btns)

        self.setLayout(box_layout)
        self.setWindowTitle("Scores")
        self.prepare(game_name)

    @staticmethod
    def _make_row(place, name, score):
        return ScoringWindow._ROW_TEMPLATE.format(place, name, score)

    def show_current(self, game_name, player_name, player_scores):
        scores = self.scoreboard.get_scores(game_name)
        # scores = sorted(scores, key=lambda x: x[1], reverse=True)
        new_scores = scores[:7]
        flag = False
        for name, scores in new_scores:
            if name == player_name:
                flag = True
        if not flag:
            new_scores += [[player_name, player_scores]]

        table = ''.join(ScoringWindow._make_row(place + 1, name, new_scores)
                        for (place, (name, new_scores)) in enumerate(new_scores))

        self._viewer.setHtml(ScoringWindow._TEMPLATE.format('Таблица рекордов', table))
        self.show()

    def prepare(self, game_name):
        scores = self.scoreboard.get_scores(game_name)
        scores = sorted(scores, key=lambda x: (-x[1], x[0]))
        # scores = sorted(scores, key=operator.itemgetter(0, 1))

        table = ''.join(ScoringWindow._make_row(place + 1, name, scores)
                        for (place, (name, scores)) in enumerate(scores))

        self._viewer.setHtml(ScoringWindow._TEMPLATE.format('Таблица рекордов', table))

