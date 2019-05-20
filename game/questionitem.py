from collections import namedtuple
from itertools import chain
from enum import Enum


class SubmitStatus(Enum):
    SUCCESS = 1
    FAILED = 2
    REPEAT = 3


class QuestionItem:
    CHANCES = 3
    Symbol = namedtuple('Symbol', ('id', 'symbol', 'status', 'is_char'))

    def __init__(self, hint, lines):
        self._hint = hint
        self._lines = lines
        self._wrongs = 0
        self._symbols = {}

        self._initialize_keys()

    @staticmethod
    def symbol_range():
        return chain(range(48, 58), range(65, 91))

    def _initialize_keys(self):
        line_str = ''.join(self._lines)
        line_str = line_str.replace(' ', '')
        line_str = line_str.upper()

        for i in self.symbol_range():
            c = chr(i)
            if c not in line_str or c in self._symbols.keys():
                continue
            self._symbols[c] = False

    @property
    def hint(self):
        return self._hint

    @property
    def wrongs(self):
        return self._wrongs

    @property
    def symbol_state(self):
        lines = []
        id = 0
        for line in self._lines:
            visibles = []
            for c in line:
                c = c.upper()

                is_char = True
                status = True
                if c.isspace() or ord(c) not in self.symbol_range():
                    is_char = False
                else:
                    status = self._symbols[c]

                visibles.append(self.Symbol(id=id, symbol=c, status=status,
                                            is_char=is_char))
                id += 1
            lines.append(visibles)
        return lines

    def get_line(self, index):
        s = ''
        for sym in self.symbol_state[index]:
            if sym.is_char:
                if sym.status:
                    s += sym.symbol
                else:
                    s += '•'
            else:
                s += sym.symbol
        return s

    @property
    def line_count(self):
        return len(self.symbol_state)

    @property
    def is_failed(self):
        return self._wrongs > self.CHANCES

    @property
    def is_finished(self):
        return all(self._symbols.values())

    def submit_char(self, c):
        c = c.upper()
        try:
            status = self._symbols[c]
            if not status:
                self._symbols[c] = True
                return SubmitStatus.SUCCESS
            else:
                return SubmitStatus.REPEAT
        except KeyError:
            self._wrongs += 1
            return SubmitStatus.FAILED

    def log_state(self):
        print(self._symbols)
        print(all(self._symbols.values()))
        print('Wrongs: [', end='')

        wrongs = self._wrongs
        for _ in range(self.CHANCES):
            if wrongs > 0:
                print('X', end='')
                wrongs -= 1
            else:
                print('_', end='')
        print(']')

        for line in self.symbol_state:
            for sym in line:
                if sym.is_char:
                    if sym.status:
                        print(sym.symbol, end='')
                    else:
                        print('_', end='')
                else:
                    print(sym.symbol, end='')
            print()

    def __repr__(self):
        return f'<QuestionItem: {self._hint}>\n'
