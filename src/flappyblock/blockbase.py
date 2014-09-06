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
