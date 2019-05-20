from enum import Enum, auto
from random import randint

import pyglet
from pyglet.gl import *

from game.state import State
from game.questionitem import SubmitStatus, CHANCES
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
        self._g_uid = uid

        if not is_closed:
            self.open()

    def open(self):
        self.image = self.g_symbol_image

    @property
    def g_uid(self):
        return self._g_uid


class WrongSprite(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(WrongSprite, self).__init__(
            img=resources.wrong_symbol_off, *args, **kwargs)

    def switch_on(self):
        self.image = resources.wrong_symbol_on

    def switch_off(self):
        self.image = resources.wrong_symbol_off


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
        LEADERBOARD = auto()

    def __init__(self):
        super(MainWindow, self).__init__(1280, 720)

        self.g_screen = self.Screen.GAME

        self.g_init_game_vars()

    @property
    def g_card_pt(self):
        return (self.height - self.g_card.height) // 2

    def g_init_symbol_tiles(self):
        self.g_symbol_tiles = {}

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

                self.g_symbol_tiles[s.id] = tile_sprite

    def g_init_hint(self):
        self.g_hint = pyglet.text.Label(
            text=self.g_state.item.hint,
            font_name='RobotoMono Medium',
            font_size=16,
            batch=self.g_game_batch,
            anchor_x='center',
            anchor_y='center',
        )
        self.g_hint.x = self.g_card_pt + self.g_card.width // 2
        self.g_hint.y = (self.g_card_pt + self.CARD_CONTENT_HEIGHT +
                         (self.g_card.height -
                          self.CARD_CONTENT_HEIGHT) // 2)

    def g_init_wrongs(self):
        self.g_wrongs = []
        for i in range(CHANCES):
            wrong = WrongSprite(
                x=self.width - self.g_wrongs_card.width,
                y=((self.height - self.g_wrongs_card.height) // 2 +
                   i * resources.wrong_symbol_on.height),
                batch=self.g_game_batch,
            )
            self.g_wrongs.append(wrong)

    def g_init_score_text(self):
        self.g_score_text = pyglet.text.Label(
            text=str(self.g_state.score),
            anchor_x='right',
            anchor_y='top',
            batch=self.g_game_batch,
            font_name='RobotoMono Medium',
            font_size=26,
        )

        self.g_score_text.x = self.width - 20
        self.g_score_text.y = self.height - 20

    def g_init_game_vars(self):
        self.g_game_batch = pyglet.graphics.Batch()
        self.g_bg = resources.bg_image
        self.g_card = resources.card_image
        self.g_wrongs_card = resources.wrongs_card

        self.g_state = State()
        self.g_state.reset()

        self.g_state.load_new_item()
        self.g_init_symbol_tiles()
        self.g_init_hint()
        self.g_init_wrongs()
        self.g_init_score_text()

    def g_draw_game_screen(self):
        self.g_bg.blit(0, 0)

        # Blending PNG transparency
        # https://stackoverflow.com/a/46048254
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.g_card.blit(self.g_card_pt, self.g_card_pt)

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.g_wrongs_card.blit(
            self.width - self.g_wrongs_card.width,
            (self.height - self.g_wrongs_card.height) // 2,
        )

        self.g_game_batch.draw()

    def on_draw(self):
        self.clear()

        # Blending PNG transparency
        # https://stackoverflow.com/a/46048254
        glEnable(GL_BLEND)

        if self.g_screen == self.Screen.GAME:
            self.g_draw_game_screen()


if __name__ == '__main__':
    x = MainWindow()
    pyglet.app.run()
