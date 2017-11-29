from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem,\
    QApplication, QVBoxLayout, QDialogButtonBox
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from scoreboard import Scoreboard
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

    def __init__(self, scoreboard, parent):
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
        self.sort_and_view_scoreboard()

    @staticmethod
    def _make_row(place, name, score):
        return ScoringWindow._ROW_TEMPLATE.format(place, name, score)

    def show_current(self, player_name, player_scores):
        new_scores = self.scoreboard._scores[:7]
        current_player_in_top_of_7 = False
        for name, scores in new_scores:
            if name == player_name:
                current_player_in_top_of_7 = True
        if not current_player_in_top_of_7:
            new_scores += [[player_name, player_scores]]

        table = ''.join(ScoringWindow._make_row(place + 1, name, new_scores)
                        for (place, (name, new_scores))
                        in enumerate(new_scores))

        self._viewer.setHtml(ScoringWindow._TEMPLATE.format(
            'Таблица рекордов', table))
        self.show()

    def sort_and_view_scoreboard(self):
        scoreboard = sorted(self.scoreboard._scores,
                            key=lambda x: (-x[1], x[0]))

        table = ''.join(ScoringWindow._make_row(place + 1, name, scoreboard)
                        for (place, (name, scoreboard))
                        in enumerate(scoreboard))

        self._viewer.setHtml(ScoringWindow._TEMPLATE.format(
            'Таблица рекордов', table))
