import random

import pipe

class PairPipes:

    def __init__(self, pipe_w, hole_size, field_w, field_h):
        self.pipe_half = pipe_w / 2.
        self.hole_size = hole_size
        self.pipe_center = field_w + pipe_w / 2.
        self.field_h = field_h
        
        self.topPipe    = pipe.Pipe()
        self.bottomPipe = pipe.Pipe()
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
