import random
from .questionitem import QuestionItem

ITEMTERMINATOR = 'XXX'


class QuestionDB:
    def __init__(self, dbfilepath):
        self._items = []
        with open(dbfilepath) as dbfile:
            while True:
                hint = dbfile.readline().strip()
                if hint == '':
                    break

                lines = []
                while True:
                    line = dbfile.readline().strip()
                    if line == ITEMTERMINATOR:
                        break
                    lines.append(line)

                self._items.append(dict(hint=hint, lines=lines))

    def pick_one(self):
        return QuestionItem(**random.choice(self._items))
