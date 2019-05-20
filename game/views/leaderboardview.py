import pyglet

from .. import resources


class LeaderBoardView:
    def __init__(self, state, win_width, win_height):
        self.win_width = win_width
        self.win_height = win_height
        self.state = state
        self.batch = pyglet.graphics.Batch()

        self.scores = pyglet.text.Label(
            text='Yeah\nhoo\nHoor',
            multiline=True,
            width=500,
            font_name='Roboto Mono',
            anchor_x='center',
            anchor_y='center',
            align='center',
            font_size=14,
            x=self.win_width // 2,
            y=330,
            color=(0, 0, 0, 255),
            batch=self.batch,
        )

        self.label = pyglet.text.Label(
            text='TOP 15 Scores',
            font_name='Roboto Mono',
            font_size=16,
            anchor_x='center',
            anchor_y='center',
            x=self.win_width // 2,
            y=588,
            batch=self.batch,
        )

        self.prompt = pyglet.text.Label(
            text='Press Esc to exit...',
            font_name='Roboto Mono',
            font_size=16,
            anchor_x='right',
            anchor_y='bottom',
            x=self.win_width - 20,
            y=20,
            batch=self.batch,
        )

    def draw(self):
        resources.leaderboard_bg.blit(0, 0)
        self.batch.draw()

    def before_route_enter(self, *args, **kwargs):
        s = ''
        cnt = 0
        limit = min(15, len(self.state.scores))
        for score_item in self.state.scores:
            if cnt == limit:
                break

            dots = 45 - len(score_item.name) - len(str(score_item.score))
            s += score_item.name
            s += '.' * dots
            s += str(score_item.score)

            if cnt < limit - 1:
                s += '\n'

            cnt += 1

        self.scores.text = s
