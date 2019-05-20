from enum import Enum, auto
from random import randint

import pyglet

from game.state import State
from game.questionitem import SubmitStatus
from game import resources


def run_cli_mode():
    state = State()

    state.reset()
    while not state.gameover:
        state.load_new_item()
        while True:
            print(f'Score: {state.score}')
            state.item.log_state()

            if state.is_end_game:
                break

            c = input('Enter char:').strip()
            response = state.submit_char(c)

            if response == SubmitStatus.SUCCESS:
                state.increment_score()
            print('=================')


class TileSprite(pyglet.sprite.Sprite):
    def __init__(self, uid, symbol, is_closed=True, *args, **kwargs):
        super(TileSprite, self).__init__(
            img=resources.blank_tile_image, *args, **kwargs)

        self.g_symbol_image = resources.symbol_tile[symbol]
        self.g_uid = uid

        if not is_closed:
            self.open()

    def open(self):
        self.image = self.g_symbol_image


class MainWindow(pyglet.window.Window):
    TILE_WIDTH = resources.symbol_tile['A'].width
    TILE_HEIGHT = resources.symbol_tile['A'].height
    TILE_SPACING_X = 5
    TILE_SPACING_Y = 5
    TILE_STRIDE_X = TILE_WIDTH + TILE_SPACING_X
    TILE_STRIDE_Y = TILE_HEIGHT + TILE_SPACING_Y
    CARD_CONTENT_HEIGHT = 500

    class Screen(Enum):
        GAME = auto()

    def __init__(self):
        super(MainWindow, self).__init__(1280, 720)

        self.g_screen = self.Screen.GAME

        self.g_init_game_vars()

    @property
    def g_card_pt(self):
        return (self.height - self.g_card.height) // 2

    def g_init_symbol_tiles(self, symbol_tiles):
        n_lines = len(self.g_state.item.symbol_state)
        lines_height = (n_lines * self.TILE_HEIGHT +
                        (n_lines - 1) * self.TILE_SPACING_Y)
        y_base = (self.CARD_CONTENT_HEIGHT + self.g_card_pt -
                  (self.CARD_CONTENT_HEIGHT - lines_height) // 2)

        for j, line in enumerate(self.g_state.item.symbol_state):
            line_width = (len(line) * self.TILE_WIDTH +
                          (len(line) - 1) * self.TILE_SPACING_X)
            x_offset = self.g_card_pt + (self.g_card.width - line_width) // 2
            y = y_base - (j + 1) * self.TILE_STRIDE_Y

            for i, s in enumerate(line):
                if s.symbol == ' ':
                    continue

                x = x_offset + i * self.TILE_STRIDE_X

                tile_sprite = TileSprite(x=x, y=y, uid=s.id, symbol=s.symbol,
                                         is_closed=s.is_char,
                                         batch=self.g_game_batch)

                symbol_tiles[s.id] = tile_sprite

    def g_init_game_vars(self):
        self.g_game_batch = pyglet.graphics.Batch()
        self.g_bg = resources.bg_image
        self.g_card = resources.card_image

        self.g_state = State()
        self.g_state.reset()
        self.g_state.load_new_item()

        self.g_symbol_tiles = {}
        self.g_init_symbol_tiles(self.g_symbol_tiles)

    def draw_game_screen(self):
        self.g_bg.blit(0, 0)
        self.g_card.blit(self.g_card_pt, self.g_card_pt)
        self.g_game_batch.draw()

    def on_draw(self):
        self.clear()

        if self.g_screen == self.Screen.GAME:
            self.draw_game_screen()


if __name__ == '__main__':
    x = MainWindow()
    pyglet.app.run()
