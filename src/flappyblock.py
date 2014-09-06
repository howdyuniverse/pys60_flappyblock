"""
    Game Template for pys60 platform
"""
import os
import sys
import e32

# dir path where game package located
PACKAGE_LOC = "E:\\Data\\python"
if PACKAGE_LOC not in sys.path:
    sys.path.append(PACKAGE_LOC)

try:
    from flappyblock import game
    game.Game().run()
except Exception, e:
    #import appuifw
    #appuifw.note(u"Exception: %s" % (e))
    print e
