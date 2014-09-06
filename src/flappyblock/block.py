import blockbase

class Block(blockbase.BlockBase):

    def __init__(self, x, y, size, fall_speed=0, jump_speed=0):
        self.FALL_SPEED = fall_speed
        self.JUMP_SPEED = jump_speed
        #
        self.start_tlx = x - size / 2.
        self.start_tly = y - size / 2.
        self.start_brx = x + size / 2.
        self.start_bry = y + size / 2.
        blockbase.BlockBase.__init__(self)
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
