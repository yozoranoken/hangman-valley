import pyglet

from .. import resources
from ..state import Screen


class ScoreView:
    def __init__(self, state, win_width, win_height):
        self.win_width = win_width
        self.win_height = win_height
        self.state = state
        self.batch = pyglet.graphics.Batch()

        self.input = pyglet.text.Label(
            text='',
            font_name='Roboto Mono',
            anchor_x='center',
            anchor_y='center',
            font_size=26,
            x=self.win_width // 2,
            y=202,
            color=(0, 0, 0, 255),
            batch=self.batch,
        )
        self.name = []
        self.score = pyglet.text.Label(
            text='',
            font_name='Roboto Mono',
            font_size=128,
            anchor_x='center',
            anchor_y='center',
            x=self.win_width // 2,
            y=400,
            color=(0, 0, 0, 255),
            batch=self.batch,
        )

        self.label = pyglet.text.Label(
            text='Submit your Score!',
            font_name='Roboto Mono',
            font_size=16,
            anchor_x='center',
            anchor_y='center',
            x=self.win_width // 2,
            y=588,
            batch=self.batch,
        )

        self.placeholder = None
        self.show_placeholder()

    def show_placeholder(self):
        self.placeholder = pyglet.text.Label(
            text='[Your name here]',
            font_name='Roboto Mono',
            anchor_x='center',
            anchor_y='center',
            font_size=26,
            x=self.win_width // 2,
            y=202,
            color=(224, 224, 224, 255),
            batch=self.batch,
        )

    def hide_placeholder(self):
        self.placeholder.delete()
        self.placeholder = None

    def update_name(self, symbol):
        if len(self.name) == 18:
            return
        self.name.append(symbol)
        self.input.text = ''.join(self.name)

    def backspace(self):
        if not self.name:
            return
        self.name.pop()
        self.input.text = ''.join(self.name)

    def handle_text(self, text):
        if self.placeholder is not None:
            self.hide_placeholder()
        self.update_name(text)

    def handle_key_press(self, symbol, modifier):
        if symbol == pyglet.window.key.BACKSPACE:
            self.backspace()
            if not self.name:
                self.show_placeholder()

        if symbol == pyglet.window.key.ENTER:
            name = ''.join(self.name).strip()
            self.state.submit_score(name)

            self.state.router.push(Screen.LEADERBOARD)

    def draw(self):
        resources.score_bg.blit(0, 0)
        self.batch.draw()

    def before_route_enter(self, *args, **kwargs):
        self.score.text = str(self.state.score)
