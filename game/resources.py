import pyglet
from itertools import chain
from .questionitem import symbol_range

pyglet.resource.path = ['resources']
pyglet.resource.add_font('Roboto-Medium.ttf')
pyglet.resource.add_font('RobotoMono-Medium.ttf')
pyglet.resource.reindex()

bg_image = pyglet.resource.image('background.png')
card_image = pyglet.resource.image('card.png')

symbol_tile = {}

for i in symbol_range():
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

wrong_symbol_on = pyglet.resource.image('wrong_sym_on.png')
wrong_symbol_off = pyglet.resource.image('wrong_sym_off.png')
wrongs_card = pyglet.resource.image('wrongs_card.png')

# Edited from https://image.shutterstock.com/image-vector/editable-vector-silhouette-man-hanged-260nw-39801637.jpg
hangman_image = [
    pyglet.resource.image(f'hangman_{i}.png') for i in range(1, 6)
]

score_bg = pyglet.resource.image('score_bg.png')
leaderboard_bg = pyglet.resource.image('leaderboard_bg.png')
