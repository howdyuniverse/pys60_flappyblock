import appuifw
import graphics

class GraphicsBase(object):
    """ Base functionality for graphics """

    def __init__(self, bg_color=(0, 0, 0)):
        """ Constructor
            Args:
                bg_color (tuple): RGB color
        """
        self.bg_color = bg_color
        #
        self.old_body = appuifw.app.body
        self.canvas = appuifw.Canvas(redraw_callback=self.redraw)
        self.screen_size = self.canvas.size
        self.buf = graphics.Draw(self.canvas)
        appuifw.app.body = self.canvas

    def clear_buf(self):
        self.buf.clear(self.bg_color)

    def redraw(self, rect=()):
        if not self.buf:
            self.canvas.blit(self.buf)

    def close_canvas(self):
        """ Return old body and destroy drawing objects """

        appuifw.app.body = self.old_body
        self.canvas = None
        self.buf = None


class GameGraphics(GraphicsBase):
    """ All drawing logic here """

    PIPE_COLOR = (26,175,93)
    SKY_COLOR = (209,228,244)
    GROUND_COLOR = (206,177,113)
    BLOCK_COLOR = (237,186,0)

    def __init__(self):
        GraphicsBase.__init__(self, bg_color=self.SKY_COLOR)
        self.field_bottom = self.screen_size[1] - self.screen_size[1] / 6.

    def draw_gamefield(self):
        self.buf.rectangle((0, self.field_bottom,
                        self.screen_size[0], self.screen_size[1]),
                        outline=None, fill=self.GROUND_COLOR)

    def draw_startmenu(self):
        self.buf.text((self.screen_size[0] * 1 / 5.5, self.field_bottom + 30),
                    unicode(u"Press 0 to start"),
                    0x000000,
                    font=(u'Nokia Sans S60', 24))

    def draw_score(self, score, best_score):
        self.buf.text((5, 25),
                    u"%s/%s" % (score, best_score),
                    0x000000,
                    font=(u'Series 60 ZDigi', 24))

    def draw_pipe(self, top_coords, btm_coords):
            self.buf.rectangle(top_coords, outline=None, fill=self.PIPE_COLOR)
            self.buf.rectangle(btm_coords, outline=None, fill=self.PIPE_COLOR)

    def draw_block(self, coords):
        self.buf.rectangle(coords, outline=None, fill=self.BLOCK_COLOR)
