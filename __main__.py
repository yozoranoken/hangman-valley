from enum import Enum, auto
from random import randint

import pyglet
from pyglet.gl import glEnable, GL_BLEND

from game import resources
from game.questionitem import SubmitStatus, CHANCES, symbol_range
from game.state import State
from game.views.gameview import GameView


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


class MainWindow(pyglet.window.Window):
    class Screen(Enum):
        GAME = auto()
        LEADERBOARD = auto()

    def __init__(self):
        super(MainWindow, self).__init__(1280, 720)

        self.g_screen = self.Screen.GAME
        self.state = State()

        self.game_view = GameView(self.state, self.width, self.height)

    def on_key_press(self, symbol, modifier):
        if symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()

        if self.g_screen == self.Screen.GAME:
            self.game_view.handle_game_key_press(symbol, modifier)

    def on_draw(self):
        self.clear()

        # RESOURCE: Blending PNG transparency
        # https://stackoverflow.com/a/46048254
        glEnable(GL_BLEND)

        if self.g_screen == self.Screen.GAME:
            self.game_view.draw()


if __name__ == '__main__':
    x = MainWindow()
    pyglet.app.run()
