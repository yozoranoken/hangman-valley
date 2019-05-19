from collections import namedtuple
from collections.abc import Sequence


class Scores(Sequence):
    ScoreItem = namedtuple('ScoreItem', ['name', 'score'])

    def __init__(self, scoresfp):
        self._sorted = False
        self._scoresfp = scoresfp
        self._read_scores(self._scoresfp)

    def _sort_scores(self):
        self._scores.sort(key=lambda x: x.score, reverse=True)
        self._sorted = True

    def _add_score(self, name, score):
        self._scores.append(self.ScoreItem(name=name, score=score))

    def _read_scores(self, scoresfp):
        self._scores = []
        with open(scoresfp) as scoresfile:
            while True:
                name = scoresfile.readline().strip()
                if name == '':
                    break
                score = int(scoresfile.readline().strip())

                self._add_score(name, score)
        self._sort_scores()

    def add_score(self, name, score):
        self._add_score(name, score)
        self._sorted = False

        with open(self._scoresfp, 'w+') as scoresfile:
            for item in self._scores:
                print(item.name, file=scoresfile)
                print(item.score, file=scoresfile)

    def __getitem__(self, index):
        if not self._sorted:
            self._sort_scores()
        return self._scores[index]

    def __len__(self):
        return len(self._scores)
