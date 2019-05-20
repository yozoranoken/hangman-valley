import os
from enum import Enum, auto

from .questiondb import QuestionDB
from .scores import Scores

DIRNAME = os.path.dirname(os.path.abspath(__file__))
DBFILEPATH = os.path.join(DIRNAME, '..', 'db.txt')
SCORESFILEPATH = os.path.join(DIRNAME, '..', 'scores.txt')


class Screen(Enum):
    GAME = auto()
    LEADERBOARD = auto()
    SCORE = auto()


class Router:
    def __init__(self):
        self._mappings = {}
        self._route = None

    def add_mapping(self, route, view):
        self._mappings[route] = view

    def push(self, route, *args, **kwargs):
        self._mappings[route].before_route_enter(*args, **kwargs)
        self._route = route

    @property
    def route(self):
        return self._route


class State:
    db = QuestionDB(DBFILEPATH)
    scores = Scores(SCORESFILEPATH)

    def __init__(self):
        self.reset()
        self._router = Router()

    @property
    def router(self):
        return self._router

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

    def submit_score(self, name):
        self.scores.add_score(name, self._score)

    @property
    def is_end_game(self):
        return self._gameover or self._item.is_finished
