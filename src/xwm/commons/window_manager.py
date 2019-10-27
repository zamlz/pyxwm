"""
TODO:
+ Remove the use of the Display object here. There should be no use of any
  Xorg server specific objects. Currently being used in update_focus_hover()
  and window_ypdate().
"""

from Xlib.display import Display

class WindowManager(object):

    def __init__(self):
        self._window_list = []
        self._active_window = None
        self._active_name = ''

        # Xorg Objects
        self.display = Display()
        self.colormap = self.display.screen().default_colormap

    def update_active(self, window, name=''):
        if window not in self._window_list and window is not None:
            print("Trying to set a window as active that isn't in list")
        else:
            self._active_window = window
            self._active_name = name

    @property
    def active(self):
        return self._active_window, self._active_name

    def update_focus(self, window, name=''):
        if window != 0:
            self.update_active(window, name)

    def update_focus_hover(self):
        self.update_focus(self.display.screen().root.query_pointer().child)

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
        self._window_list.append(window)
        if active is True:
            self.update_active(window)
        return window

