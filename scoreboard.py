import json
import os.path


class Scoreboard:
    def __init__(self, filename='scoreboard.txt'):
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, 'x') as f:
                json.dump([], f)

        with open(filename) as f:
            self._scores = json.load(f)
            # print(self._scores)

    def add_score(self, name, score):
        self._scores.append([name, score])
        with open(self.filename, 'w') as f:
            json.dump(self._scores, f)

    def get_scores(self):
        return self._scores
