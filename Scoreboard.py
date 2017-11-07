import json
import os.path


class Scoreboard:
    def __init__(self, filename='scoreboard.txt'):
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, 'x') as f:
                json.dump({}, f)

        with open(filename) as f:
            self._scores = json.load(f, parse_int=float)

        # print(self._scores)

    def add_score(self, game_name, name, score):
        if game_name not in self._scores:
            self._scores[game_name] = []
        self._scores[game_name].append([name, score])
        with open(self.filename, 'w') as f:
            json.dump(self._scores, f)

    def get_scores(self, game_name):
        return sorted(self._scores[game_name], key=lambda x: x[1], reverse=True)
        # return self._scores[game_name]
        # """Скорборд полей с заданными параметрами"""
        # key = Scoreboard.PARAMS_SEP.join(map(str, list(size) + [bombs]))
        # return sorted(self._scores.get(key, []), key=operator.itemgetter(1))


if __name__ == '__main__':
    s = Scoreboard()
    s.add_score("game1", "Андрей", 300)
    print(s._scores)