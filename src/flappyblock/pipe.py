import blockbase

class Pipe(blockbase.BlockBase):

    def move(self, step):
        self.tleft_x  -= step
        self.bright_x -= step

    def overflow(self):
        if self.bright_x <= 0:
            return True
        return False
