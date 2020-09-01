import sys

if sys.argv[1] == "--gui":
    from . import _gui
    _gui.run()
else:
    pass
