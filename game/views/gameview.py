import pyglet
from pyglet.gl import glBlendFunc, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA

from .. import resources
from ..questionitem import CHANCES, symbol_range, SubmitStatus


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


class GameView:
    TILE_WIDTH = resources.symbol_tile['A'].width
    TILE_HEIGHT = resources.symbol_tile['A'].height
    TILE_SPACING_X = 5
    TILE_SPACING_Y = 5
    TILE_STRIDE_X = TILE_WIDTH + TILE_SPACING_X
    TILE_STRIDE_Y = TILE_HEIGHT + TILE_SPACING_Y
    CARD_CONTENT_HEIGHT = 500

    def __init__(self, state, win_width, win_height):
        self.win_width = win_width
        self.win_height = win_height
        self.state = state

        self.game_batch = pyglet.graphics.Batch()
        self.bg = resources.bg_image
        self.card = resources.card_image
        self.wrongs_card = resources.wrongs_card

        self.notification = None
        self.hint = None
        self.score_text = None
        self.symbol_tiles = {}
        self.wrongs = []

        self.reset()

    def reset(self):
        self.state.reset()
        self.init_next_item()
        self.init_score_text()

    @property
    def card_pt(self):
        return (self.win_height - self.card.height) // 2

    def init_symbol_tiles(self):
        if self.symbol_tiles:
            for tile in self.symbol_tiles.values():
                tile.delete()
            self.symbol_tiles = {}

        n_lines = len(self.state.item.symbol_state)
        lines_height = (n_lines * self.TILE_HEIGHT +
                        (n_lines - 1) * self.TILE_SPACING_Y)
        y_base = (self.CARD_CONTENT_HEIGHT + self.card_pt -
                  (self.CARD_CONTENT_HEIGHT - lines_height) // 2)

        for j, line in enumerate(self.state.item.symbol_state):
            line_width = (len(line) * self.TILE_WIDTH +
                          (len(line) - 1) * self.TILE_SPACING_X)
            x_offset = self.card_pt + (self.card.width - line_width) // 2
            y = y_base - (j + 1) * self.TILE_STRIDE_Y

            for i, s in enumerate(line):
                if s.symbol == ' ':
                    continue

                x = x_offset + i * self.TILE_STRIDE_X

                tile_sprite = TileSprite(x=x, y=y, uid=s.id, symbol=s.symbol,
                                         is_closed=s.is_char,
                                         batch=self.game_batch)

                self.symbol_tiles[s.id] = tile_sprite

    def init_hint(self):
        if self.hint is None:
            self.hint = pyglet.text.Label(
                text='',
                font_name='Roboto Mono',
                font_size=16,
                batch=self.game_batch,
                anchor_x='center',
                anchor_y='center',
            )
        self.hint.text = self.state.item.hint
        self.hint.x = self.card_pt + self.card.width // 2
        self.hint.y = (self.card_pt + self.CARD_CONTENT_HEIGHT +
                       (self.card.height -
                        self.CARD_CONTENT_HEIGHT) // 2)

    def init_wrongs(self):
        if not self.wrongs:
            for i in range(CHANCES):
                wrong = WrongSprite(
                    x=self.win_width - self.wrongs_card.width,
                    y=((self.win_height - self.wrongs_card.height) // 2 +
                       i * resources.wrong_symbol_on.height),
                    batch=self.game_batch,
                )
                self.wrongs.append(wrong)

            self.wrongs.reverse()

        for wrong in self.wrongs:
            wrong.switch_off()

    def init_score_text(self):
        if self.score_text is None:
            self.score_text = pyglet.text.Label(
                text='',
                anchor_x='right',
                anchor_y='top',
                batch=self.game_batch,
                font_name='Roboto Mono',
                font_size=26,
            )

            self.score_text.x = self.win_width - 20
            self.score_text.y = self.win_height - 20

        self.score_text.text = str(self.state.score)

    def init_next_item(self):
        self.state.load_new_item()
        self.init_symbol_tiles()
        self.init_hint()
        self.init_wrongs()

    def update_symbol_tiles(self):
        for line in self.state.item.symbol_state:
            for s in line:
                if not s.is_char or not s.status:
                    continue
                self.symbol_tiles[s.id].open()

    def update_wrongs(self):
        wrongs = self.state.item.wrongs
        if wrongs > len(self.wrongs):
            return
        self.wrongs[wrongs - 1].switch_on()

    def close_notification(self):
        self.notification.delete()
        self.notification = None

    def show_notification(self, text):
        if self.notification is not None:
            self.close_notification()

        notif = pyglet.text.Label(
            text=text,
            anchor_x='right',
            anchor_y='bottom',
            font_name='Roboto Mono',
            font_size=16,
            batch=self.game_batch,
        )
        notif.x = self.win_width - 20
        notif.y = 20
        self.notification = notif

    def handle_game_key_press(self, symbol, modifier):
        if self.state.item.is_finished:
            if symbol == pyglet.window.key.ENTER:
                self.close_notification()
                self.init_next_item()
            else:
                return

        if self.state.gameover:
            if symbol == pyglet.window.key.ENTER:
                self.close_notification()
                self.reset()
                # pyglet.app.exit()
            else:
                return

        c = chr(symbol).upper()

        if ord(c) in symbol_range():
            response = self.state.submit_char(c)

            if response == SubmitStatus.SUCCESS:
                self.state.increment_score()
                self.score_text.text = str(self.state.score)
                self.update_symbol_tiles()

                if self.state.item.is_finished:
                    self.show_notification(
                        'Great job! Press Enter to continue...')

            elif response == SubmitStatus.FAILED:
                self.update_wrongs()

                if self.state.gameover:
                    self.show_notification(
                        'Too Bad. Press Enter to exit...')

    def draw(self):
        self.bg.blit(0, 0)

        # RESOURCE: Blending PNG transparency
        # https://stackoverflow.com/a/46048254
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.card.blit(self.card_pt, self.card_pt)

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.wrongs_card.blit(
            self.win_width - self.wrongs_card.width,
            (self.win_height - self.wrongs_card.height) // 2,
        )

        wrongs = self.state.item.wrongs
        if wrongs > 0:
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            resources.hangman_image[wrongs - 1].blit(673, 95)

        self.game_batch.draw()
