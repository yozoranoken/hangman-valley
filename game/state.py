import os
from .questiondb import QuestionDB
from .scores import Scores

DIRNAME = os.path.dirname(os.path.abspath(__file__))
DBFILEPATH = os.path.join(DIRNAME, '..', 'db.txt')
SCORESFILEPATH = os.path.join(DIRNAME, '..', 'scores.txt')


class State:
    db = QuestionDB(DBFILEPATH)
    scores = Scores(SCORESFILEPATH)

    def __init__(self):
        self.reset()

    @property
    def score(self):
        return self._score

    @property
    def gameover(self):
        return self._gameover

    @property
    def item(self):
        return self._item

    def reset(self):
        self._score = 0
        self._gameover = False

    def submit_char(self, c):
        status = self._item.submit_char(c)
        self._gameover = self._item.is_failed
        return status

    def load_new_item(self):
        self._item = self.db.pick_one()

    def increment_score(self):
        self._score += 1

    @property
    def is_end_game(self):
        return self._gameover or self._item.is_finished
