from enum import Enum, auto
from itertools import chain
from random import randint

import pyglet
from pyglet.gl import glEnable, GL_BLEND

from game import resources
from game.questionitem import SubmitStatus, CHANCES, symbol_range
from game.state import State, Screen
from game.views.gameview import GameView
from game.views.scoreview import ScoreView
from game.views.leaderboardview import LeaderBoardView


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
    def __init__(self):
        super(MainWindow, self).__init__(1280, 720)

        self.state = State()

        self.game_view = GameView(self.state, self.width, self.height)
        self.score_view = ScoreView(self.state, self.width, self.height)
        self.leaderboard_view = LeaderBoardView(
            self.state, self.width, self.height)

        self.state.router.add_mapping(Screen.GAME, self.game_view)
        self.state.router.add_mapping(Screen.SCORE, self.score_view)
        self.state.router.add_mapping(
            Screen.LEADERBOARD, self.leaderboard_view)

        self.state.router.push(Screen.GAME)

    def on_key_press(self, symbol, modifier):
        if symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()

        if self.state.router.route == Screen.GAME:
            self.game_view.handle_game_key_press(symbol, modifier)
        elif self.state.router.route == Screen.SCORE:
            self.score_view.handle_key_press(symbol, modifier)

    def on_text(self, text):
        if self.state.router.route == Screen.SCORE:
            self.score_view.handle_text(text)

    def on_draw(self):
        self.clear()

        # RESOURCE: Blending PNG transparency
        # https://stackoverflow.com/a/46048254
        glEnable(GL_BLEND)

        if self.state.router.route == Screen.GAME:
            self.game_view.draw()
        elif self.state.router.route == Screen.SCORE:
            self.score_view.draw()
        elif self.state.router.route == Screen.LEADERBOARD:
            self.leaderboard_view.draw()


if __name__ == '__main__':
    x = MainWindow()
    pyglet.app.run()
