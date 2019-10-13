
import time
from Xlib import X, XK
from Xlib.display import Display, colormap

from xwm.core.keys import str_to_keysym

# This WM takes full utilization of single thread.
# end result is usually that cpu fans go to full
# blast. In the primary loop, we add a sleep
# command so that the looping isn't at full
# blast. TUNE THIS VALUE WITH CAUTION.
# TODO: There must be a better way of handling this
# issue
REFRESH_RATE=0.01

class XwmSession(object):

    def __init__(self):

        self.window_list = []

        self.display = Display()
        self.colormap = self.display.screen().default_colormap
        self.root = self.display.screen().root
        self.width = self.root.get_geometry().width
        self.height = self.root.get_geometry().height

        self.current_event = None
        self.active_window = None

        self.root.change_attributes(event_mask=X.SubstructureRedirectMask)

    def run(self):
        try:
            while True:
                self.update_focus()
                map(self.window_update, self.window_list)
                self.handle_events()
                time.sleep(REFRESH_RATE)
        except KeyboardInterrupt:
            self.close_display()

    def update_focus(self):
        # Primitive focus method that focuses whatever is on the pointer
        window = self.display.screen().root.query_pointer().child
        if window != 0:
            self.active_window = window

    def window_update(self, window):
        border = "#ffffff" if window is self.active_window else "#000000"
        border_color = self.colormap.alloc_named_color(border).pixel
        window.configure(border_width=4)
        window.change_attributes(None, border_pixel=border_color)
        self.display.sync()

    def handle_events(self):
        # handle events
        # Why are these events blacklisted?
        ignored_events = [3, 33, 34, 23]
        if self.display.pending_events() == 0:
            return

        self.current_event = self.display.next_event()

        if self.current_event.type == X.MapRequest:
            self.handle_map()

        elif self.current_event.type == X.KeyPress:
            self.handle_key_press()

        elif self.current_event.type in ignored_events:
            pass

        else:
            pass

    def handle_map(self):
        # I'm guessing this maps a new window perhaps?
        self.window_list.append(self.current_event.window)
        self.active_window = self.current_event.window
        self.active_window_name = self.current_event.window.get_wm_name()
        self.current_event.window.map()

    def add_keybinds(self, kb):
        self.keybinds = {}
        mod = X.Mod1Mask
        for key, v in kb.items():
            # Modifier is hardcoded in instead being taken from KeyBinder
            code = self.display.keysym_to_keycode(str_to_keysym[key])
            self.root.grab_key(code, mod, 1, X.GrabModeAsync, X.GrabModeAsync)
            self.keybinds[code] = kb[key]

    def handle_key_press(self):
        try:
            self.keybinds[self.current_event.detail](self)
        except KeyError:
            print("unable to process key press")
        except:
            print("something when wrong with keyfunc")

def close_display(self):
        self.display.close()
