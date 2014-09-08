import key_codes

import ggraphics

import block
import pairpipes

class GameCore(object):
    """ All game logic here """

    PIPE_SPEED = 2
    BLOCK_FALLSPEED = 1
    BLOCK_JUMPSPEED = 15

    def __init__(self):
        self.graphics = ggraphics.GameGraphics()

        self.running = True
        self.playing = False
        self.score = 0
        self.best_score = 0
        self.load_bestscore()

        # game field boundaries
        self.field_top    = 0
        self.field_left   = 0
        self.field_bottom = self.graphics.screen_size[1] - self.graphics.screen_size[1] / 6.

        #
        blocksize = self.graphics.screen_size[0]/14.
        self.block = block.Block(x=self.graphics.screen_size[0] * 1/4.,
                            y=self.graphics.screen_size[1] / 2.,
                            size=blocksize,
                            fall_speed=self.BLOCK_FALLSPEED,
                            jump_speed=self.BLOCK_JUMPSPEED)

        self.pipewidth = blocksize * 2
        first_pipe = pairpipes.PairPipes(self.pipewidth,
                                blocksize*3.5,
                                self.graphics.screen_size[0],
                                self.graphics.screen_size[1] - self.graphics.screen_size[1] / 6.,
                                )
        second_pipe = pairpipes.PairPipes(self.pipewidth,
                                blocksize*3.5,
                                self.graphics.screen_size[0],
                                self.graphics.screen_size[1] - self.graphics.screen_size[1] / 6.,
                                )
        second_pipe.move(-self.pipewidth*3.5)
        self.PIPES = [first_pipe, second_pipe]

        self.graphics.canvas.bind(key_codes.EKey0, lambda: self.start_playing())

    def draw_scene(self):
        self.graphics.clear_buf()
        # (!) field_bottom var
        self.graphics.draw_gamefield()
        # draw pipes
        for pipe in self.PIPES:
            self.graphics.draw_pipe(pipe.top_coords(), pipe.bottom_coords())
        # draw players block
        self.graphics.draw_block(self.block.coords())

        if not self.playing:
            self.graphics.draw_startmenu()

        self.graphics.draw_score(unicode(self.score), unicode(self.best_score))

        

    def tick(self):
        self.draw_scene()

        if self.playing:
            self.block.move()
            self.move_pipes()
            # pass pipes
            self.check_intersection()

        self.graphics.redraw()

    def cancel(self):
        """ cancel all game flags/core loops """
        self.running = False

    def quit(self):
        """ Must be called when game ends """

        self.graphics.close_canvas()

    #
    def load_bestscore(self):
        try:
            data = open('pyFlappyBlock_score.txt', 'r')
            self.best_score = int(data.readline())
        except:
            pass

    def save_bestscore(self):
        data = open('pyFlappyBlock_score.txt', 'w')
        data.write(unicode(self.score))

    def reset_game(self):
        if self.score > self.best_score:
            self.save_bestscore()
            self.best_score = self.score
        self.score = 0
        self.block.reset()
        for pipe in self.PIPES:
            pipe.gen_pipes()
        self.PIPES[-1].move(-self.pipewidth*3.5)  

    def start_playing(self):
        self.playing = True
        self.reset_game()
        self.graphics.canvas.bind(key_codes.EKey0, lambda: None)
        self.graphics.canvas.bind(key_codes.EKey5, lambda: self.block.jump())

    def stop_playing(self):
        self.playing = False
        self.graphics.canvas.bind(key_codes.EKey0, lambda: self.start_playing())
        self.graphics.canvas.bind(key_codes.EKey5, lambda: None)

    def move_pipes(self):
        for pipe in self.PIPES:
            pipe.move(self.PIPE_SPEED)

    def check_intersection(self):
        """ Check intersection between Pipes and Block
        """
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
