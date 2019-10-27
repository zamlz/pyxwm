
from Xlib.display import Display

class WindowManager(object):

    def __init__(self):
        self._window_list = []
        self._active_window = None
        self._active_name = ''
        # Do not use a display object here! Try to remove any trace of Xorg
        # from this
        self.display = Display()
        self.colormap = self.display.screen().default_colormap

    def update_active(self, window):
        if window not in self._window_list and window is not None:
            print("Trying to set a window as active that isn't in list")
        else:
            self._active_window = window
            self._active_name = window.get_wm_name()

    @property
    def active(self):
        return self._active_window, self._active_window_name

    def update_focus(self, window):
        if window != 0:
            self.update_active(window)

    def window_update_serial(self):
        for window in self._window_list:
            self.window_update(window)

    def window_update_parallel(self):
        raise NotImplementedError

    def window_update(self, window):
        #raise NotImplementedError
        border = "#ffffff" if window is self.active else "#000000"
        border_color = self.colormap.alloc_named_color(border).pixel
        window.configure(border_width=4)
        window.change_attributes(None, border_pixel=border_color)
        self.display.sync()

    def spawn(self, window, name, active=False):
        self._window_list.append(window)
        if active is True:
            self._active_window = window
            self._active_name = name
        return window


