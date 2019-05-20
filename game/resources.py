import pyglet
from itertools import chain
from .questionitem import QuestionItem

pyglet.resource.path = ['resources']
pyglet.resource.add_font('Roboto-Medium.ttf')
pyglet.resource.add_font('RobotoMono-Medium.ttf')
pyglet.resource.reindex()

bg_image = pyglet.resource.image('background.png')
card_image = pyglet.resource.image('card.png')

symbol_tile = {}

for i in QuestionItem.symbol_range():
    c = chr(i)
    symbol_tile[c] = pyglet.resource.image(f'{c}.png')

SYMBOL_TO_NAME = {
    '!': 'EXCLAMATION',
    '@': 'AT',
    '#': 'HASH',
    '$': 'DOLLAR',
    '%': 'PERCENT',
    '^': 'HAT',
    '&': 'AND',
    '*': 'ASTERISK',
    '(': 'PAR_OPEN',
    ')': 'PAR_CLOSE',
    '-': 'DASH',
    '_': 'UNDERSCORE',
    '+': 'PLUS',
    '=': 'EQUALS',
    '{': 'BRACE_OPEN',
    '}': 'BRACE_CLOSE',
    '[': 'BAR_OPEN',
    ']': 'BAR_CLOSE',
    ':': 'COLON',
    ';': 'SEMICOLON',
    '"': 'STRAIGHT_QUOTE',
    '“': 'QUOTE_OPEN',
    '”': 'QUOTE_CLOSE',
    "'": 'STRAIGHT_SINGLE_QUOTE',
    '‘': 'SINGLE_QUOTE_OPEN',
    '’': 'SINGLE_QUOTE_CLOSE',
    '|': 'BAR',
    '\\': 'BACKSLASH',
    '<': 'GT',
    '>': 'LT',
    ',': 'COMMA',
    '.': 'PERIOD',
    '?': 'QUESTION',
    '/': 'SLASH',
}

for symbol, name in SYMBOL_TO_NAME.items():
    symbol_tile[symbol] = pyglet.resource.image(f'{name}.png')

blank_tile_image = pyglet.resource.image('BLANK.png')
