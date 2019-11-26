"""
TODO:
+ Remove the use of the Display object here. There should be no use of any
  Xorg server specific objects. Currently being used in update_focus_hover()
  and window_ypdate().
"""

from Xlib.display import Display
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class WindowManager(object):

    def __init__(self):
        logger.info("initializing window manager")
        self._window_list = []
        self._active_window = None
        self._active_name = ''

        # Xorg Objects
        self.display = Display()
        self.colormap = self.display.screen().default_colormap

    def update_active(self, window, name=''):
        if window not in self._window_list and window is not None:
            logger.error("Trying to set a window as active that isn't in list")
        elif window is self._active_window:
            logger.debug("Window is already active. Doing nothing.")
        else:
            logger.info(f"Setting active window: {window} {name}")
            self._active_window = window
            self._active_name = name

    @property
    def active(self):
        return self._active_window, self._active_name

    def update_focus(self, window, name=''):
        logger.debug(f"Updating focus to window: {window} {name}")
        if window != 0:
            self.update_active(window, name)

    def update_focus_hover(self):
        logger.debug(f"Updating focus to hovered window")
        window = self.display.screen().root.query_pointer().child
        logger.debug("WINDOW: " + repr(window))
        self.update_focus(window)

    def window_update_serial(self):
        for window in self._window_list:
            self.window_update(window)

    def window_update_parallel(self):
        raise NotImplementedError

    def window_update(self, window):
        #raise NotImplementedError
        border = "#ffffff" if window is self.active[0] else "#000000"
        border_color = self.colormap.alloc_named_color(border).pixel
        window.configure(border_width=4)
        window.change_attributes(None, border_pixel=border_color)
        self.display.sync()

    def spawn(self, window, name, active=False):
        logger.info(f"Spawning new window: {window} {name}")
        logger.debug(self._window_list)
        self._window_list.append(window)
        logger.debug(self._window_list)
        if active is True:
            self.update_active(window)
        return window


