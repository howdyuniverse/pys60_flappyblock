import appuifw
import e32

import gcore

class Game(object):
    """ Base game functionality for program """

    INTERVAL = 0.02

    def __init__(self, screen_mode="full"):
        """ Constructor
            Args:
                screen_mode (str): normal, large, full
        """

        appuifw.app.screen = screen_mode
        self.game_core = gcore.GameCore()
        # left menu key functions
        appuifw.app.menu = [
            (u"Exit", self.set_exit)
        ]
        self.exit_flag = False

    def set_exit(self):
        """ Breaks game loop in self.run function """

        self.game_core.cancel()
        self.exit_flag = True

    def run(self):
        """ Main game loop """

        appuifw.app.exit_key_handler = self.set_exit
        
        while not self.exit_flag:
            self.game_core.tick()
            e32.ao_sleep(self.INTERVAL)

        self.game_core.quit()
