import e32
import appuifw
import graphics
import key_codes
import random

class BlockBase:

    def __init__(self, tleft_x=0, tleft_y=0, bright_x=0, bright_y=0):
        self.set_coords(tleft_x, tleft_y, bright_x, bright_y)

    def set_coords(self, tleft_x, tleft_y, bright_x, bright_y):
        self.tleft_x = tleft_x
        self.tleft_y = tleft_y
        self.bright_x = bright_x
        self.bright_y = bright_y

    def coords(self):
        return (self.tleft_x, self.tleft_y,
                self.bright_x, self.bright_y)


class Block(BlockBase):

    def __init__(self, x, y, size, fall_speed=0, jump_speed=0):
        self.FALL_SPEED = fall_speed
        self.JUMP_SPEED = jump_speed
        #
        self.start_tlx = x - size / 2.
        self.start_tly = y - size / 2.
        self.start_brx = x + size / 2.
        self.start_bry = y + size / 2.
        BlockBase.__init__(self)
        self.reset()

    def reset(self):
        self.set_coords(self.start_tlx, self.start_tly, self.start_brx, self.start_bry)
        self.velocity = 0.0

    def jump(self):
        self.velocity -= self.JUMP_SPEED

    def move(self):
        self.tleft_y  += self.velocity
        self.bright_y += self.velocity
        self.velocity += self.FALL_SPEED


class Pipe(BlockBase):

    def move(self, step):
        self.tleft_x  -= step
        self.bright_x -= step

    def overflow(self):
        if self.bright_x <= 0:
            return True
        return False


class PairPipes:

    def __init__(self, pipe_w, hole_size, field_w, field_h):
        self.pipe_half = pipe_w / 2.
        self.hole_size = hole_size
        self.pipe_center = field_w + pipe_w / 2.
        self.field_h = field_h
        
        self.topPipe    = Pipe()
        self.bottomPipe = Pipe()
        self.gen_pipes()

    def gen_pipes(self):
        self.passed = False
        self.toppipe_h = random.randint(int(self.field_h / 4.),
                                        int(self.field_h - self.field_h / 4.))
        self.topPipe.set_coords(self.pipe_center - self.pipe_half,
                                0,
                                self.pipe_center + self.pipe_half,
                                self.toppipe_h)
        self.bottomPipe.set_coords(self.pipe_center - self.pipe_half,
                                    self.toppipe_h + self.hole_size,
                                    self.pipe_center + self.pipe_half,
                                    self.field_h)

    def move(self, step):
        self.topPipe.move(step)
        self.bottomPipe.move(step)

        # check left border intersection
        if self.topPipe.overflow() and self.bottomPipe.overflow():
            # generate new pair of pipes with new hole
            self.gen_pipes()

    def is_passed(self):
        return self.passed

    def set_passed(self):
        self.passed = True

    def top_coords(self):
        return self.topPipe.coords()

    def bottom_coords(self):
        return self.bottomPipe.coords()


class pyFlappyBlock:

    PIPE_SPEED = 2
    BLOCK_FALLSPEED = 0.5
    BLOCL_JUMPSPEED = 7
    SLEEP = 0.001

    def __init__(self):
        self.running = True
        self.playing = False
        self.score = 0
        self.best_score = 0
        self.load_bestscore()

        appuifw.app.screen = 'full'
        #appuifw.app.orientation = 'landscape'
        appuifw.app.exit_key_handler = self.quit
        #
        self.img = None
        self.canvas = appuifw.Canvas(redraw_callback=self.handle_redraw)
        appuifw.app.body = self.canvas
        self.img = graphics.Image.new(self.canvas.size)

        # key bindings
        self.canvas.bind(key_codes.EKey0, lambda: self.start_playing())

        # game field boundaries
        self.field_top    = 0
        self.field_left   = 0
        self.field_right  = self.canvas.size[0]
        self.field_bottom = self.canvas.size[1] - self.canvas.size[1] / 6.

        #
        blocksize = self.canvas.size[0]/14.
        self.block = Block(x=self.canvas.size[0] * 1/4.,
                            y=self.canvas.size[1] / 2.,
                            size=blocksize,
                            fall_speed=pyFlappyBlock.BLOCK_FALLSPEED,
                            jump_speed=pyFlappyBlock.BLOCL_JUMPSPEED)

        

        self.pipewidth = blocksize * 2
        first_pipe = PairPipes(self.pipewidth,
                                blocksize*3.5,
                                self.canvas.size[0],
                                self.canvas.size[1] - self.canvas.size[1] / 6.,
                                )
        second_pipe = PairPipes(self.pipewidth,
                                blocksize*3.5,
                                self.canvas.size[0],
                                self.canvas.size[1] - self.canvas.size[1] / 6.,
                                )
        second_pipe.move(-self.pipewidth*3.5)
        self.PIPES = [first_pipe, second_pipe]

    def load_bestscore(self):
        try:
            data = open('pyFlappyBlock_score.txt', 'r')
            self.best_score = int(data.readline())
        except:
            pass

    def save_bestscore(self):
        data = open('pyFlappyBlock_score.txt', 'w')
        data.write(unicode(self.score))

    def handle_redraw(self, rect):
        if self.img: self.canvas.blit(self.img)

    def quit(self):
        self.running = False

    def start_playing(self):
        self.playing = True
        self.reset_game()
        self.canvas.bind(key_codes.EKey0, lambda: None)
        self.canvas.bind(key_codes.EKey5, lambda: self.block.jump())

    def stop_playing(self):
        self.playing = False
        self.canvas.bind(key_codes.EKey0, lambda: self.start_playing())
        self.canvas.bind(key_codes.EKey5, lambda: None)

    def reset_game(self):
        if self.score > self.best_score:
            self.save_bestscore()
            self.best_score = self.score
        self.score = 0
        self.block.reset()
        for pipe in self.PIPES:
            pipe.gen_pipes()
        self.PIPES[-1].move(-self.pipewidth*3.5)     

    def draw_startmenu(self):
        self.img.text((self.canvas.size[0]*1/5.5, self.field_bottom + 30),
                        unicode(u"Press 0 to start"),
                        0x000000,
                        font=(u'Nokia Sans S60', 24))

    def draw_pipes(self):
        for pipe in self.PIPES:
            # draw pipes
            self.img.rectangle(pipe.top_coords(), outline=None, fill=(26,175,93))
            self.img.rectangle(pipe.bottom_coords(), outline=None, fill=(26,175,93))

    def move_pipes(self):
        for pipe in self.PIPES:
            pipe.move(pyFlappyBlock.PIPE_SPEED)

    def check_intersection(self):
        '''
            Check intersection between Pipes and Player
        '''
        for pipe in self.PIPES:
            if not pipe.is_passed():
                # get block coords
                block_ltx, block_lty, block_rbx, block_rby = self.block.coords()
                # top pipe coords, left x and right x
                pipet_lx, pipet_rx = pipe.top_coords()[0], pipe.top_coords()[2]
                # bottom y, and top y from pipes
                pipet_by = pipe.top_coords()[3]
                pipeb_ty = pipe.bottom_coords()[1]

                # check right border of pipe and block left border
                if pipe.top_coords()[2] < block_ltx:
                    self.score += 1
                    pipe.set_passed()
                # check intercestions
                if block_rby >= self.field_bottom:
                    self.stop_playing()
                #
                if block_rbx > pipet_lx and block_rbx < pipet_rx:
                    if block_lty < pipet_by or block_rby > pipeb_ty:
                        self.stop_playing()
                if block_ltx < pipet_rx and block_rbx > pipet_rx:
                    if block_lty < pipet_by or block_rby > pipeb_ty:
                        self.stop_playing()

    def run(self):
        while self.running:
            self.img.clear((209,228,244))
            self.img.rectangle((0, self.field_bottom,
                            self.canvas.size[0], self.canvas.size[1]),
                            outline=None, fill=(206,177,113))
            self.draw_pipes()
            # draw playes block
            self.img.rectangle(self.block.coords(), outline=None, fill=(237,186,0))

            if self.playing:
                self.block.move()
                self.move_pipes()
                # pass pipes
                self.check_intersection()
            else:
                self.draw_startmenu()

            # draw player score
            self.img.text((5, 25),
                            unicode(self.score)+u"/"+unicode(self.best_score),
                            0x000000,
                            font=(u'Series 60 ZDigi', 24))
            self.handle_redraw(())
            e32.ao_sleep(pyFlappyBlock.SLEEP)


if __name__ == '__main__':
    pyFlappyBlock().run()
