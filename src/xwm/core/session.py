
import time
from Xlib import X, XK
from Xlib.display import Display

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

    def __init__(self, winman=None, keybinder=None):

        self.winman = winman
        self.kb_map = keybinder
        self.current_event = None

        self.display = Display()
        self.root = self.display.screen().root
        self.width = self.root.get_geometry().width
        self.height = self.root.get_geometry().height
        self.root.change_attributes(event_mask=X.SubstructureRedirectMask)

        self.startup_ops = [self._init_keybinds]
        self.loop_ops = [self._handle_events]

    def startup(self, method):
        self.startup_ops.append(method)
        return method

    def onloop(self, method):
        self.loop_ops.append(method)
        return method

    def run(self):
        try:
            for func in self.startup_ops:
                func()
            while True:
                time.sleep(REFRESH_RATE)
                for func in self.loop_ops:
                    func()
        except KeyboardInterrupt:
            self.close_display()

    def _handle_events(self):
        # handle events
        # Why are these events blacklisted?
        ignored_events = [3, 33, 34, 23]
        if self.display.pending_events() == 0:
            return

        self.current_event = self.display.next_event()

        if self.current_event.type == X.MapRequest:
            self._handle_map()

        elif self.current_event.type == X.KeyPress:
            self._handle_key_press()

        elif self.current_event.type in ignored_events:
            pass

        else:
            pass

    def _handle_map(self):
        window = self.current_event.window
        self.winman.spawn(window, window.get_wm_name(), active=True)
        window.map()

    def _init_keybinds(self):
        self.keybinds = {}
        mod = X.Mod1Mask
        for key, v in self.kb_map.items():
            # Modifier is hardcoded in instead being taken from KeyBinder
            code = self.display.keysym_to_keycode(str_to_keysym[key])
            self.root.grab_key(code, mod, 1, X.GrabModeAsync, X.GrabModeAsync)
            self.keybinds[code] = self.kb_map[key]

    def _handle_key_press(self):
        try:
            self.keybinds[self.current_event.detail]()
        except KeyError:
            print("unable to process key press")
        except:
            print("something when wrong with keyfunc")

    def close_display(self):
        self.display.close()
