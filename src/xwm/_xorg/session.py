
import subprocess
import time
from Xlib import X, XK
from Xlib.display import Display, colormap
from collections import namedtuple

# This WM takes full utilization of single thread.
# end result is usually that cpu fans go to full
# blast. In the primary loop, we add a sleep
# command so that the looping isn't at full
# blast. TUNE THIS VALUE WITH CAUTION.
# TODO: There must be a better way of handling this
# issue
REFRESH_RATE=0.01

Keymap = namedtuple('Keymap', ['key', 'op'])

class XorgWindowManagerSession(object):

    def __init__(self):

        self.window_list = []

        self.display = Display()
        self.colormap = self.display.screen().default_colormap
        self.root = self.display.screen().root
        self.width = self.root.get_geometry().width
        self.height = self.root.get_geometry().height

        self.current_mode = None
        self.active_window = None

        self.root.change_attributes(event_mask=X.SubstructureRedirectMask)

        self.configure_keybindings()

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

        event = self.display.next_event()

        if event.type == X.MapRequest:
            self.handle_map(event)

        elif event.type == X.KeyPress:
            self.handle_key_press(event)

        elif event.type in ignored_events:
            pass

        else:
            pass

    def handle_map(self, event):
        # I'm guessing this maps a new window perhaps?
        self.window_list.append(event.window)
        self.active_window = event.window
        self.active_window_name = event.window.get_wm_name()
        event.window.map()

    def configure_keybindings(self):
        sym2code = self.display.keysym_to_keycodes
        self.kb = {}

        self.kb['left'] =   Keymap(set(c for c, _ in sym2code(XK.XK_Left)),
                                   (self.move_window, {"dir": "left"}))

        self.kb['right'] =  Keymap(set(c for c, _ in sym2code(XK.XK_Right)),
                                   (self.move_window, {"dir": "right"}))

        self.kb['up'] =     Keymap(set(c for c, _ in sym2code(XK.XK_Up)),
                                   (self.move_window, {"dir": "up"}))

        self.kb['down'] =   Keymap(set(c for c, _ in sym2code(XK.XK_Down)),
                                   (self.move_window, {"dir": "down"}))

        self.kb['close'] =  Keymap(set(c for c, _ in sym2code(XK.XK_X)),
                                   (self.destroy_window, {}))

        self.kb['t'] =      Keymap(set(c for c, _ in sym2code(XK.XK_T)),
                                   (self.run_proc, {"proc": "terminal"}))

        self.kb['e'] =      Keymap(set(c for c, _ in sym2code(XK.XK_E)),
                                   (self.run_proc, {"proc": "launcher"}))

        self.kb['r'] =      Keymap(set(c for c, _ in sym2code(XK.XK_R)),
                                   ())
        self.kb['quit'] =   Keymap(set(c for c, _ in sym2code(XK.XK_Escape)),
                                   (self.close_display, {}))

        # Adds the alt key to each of the keys
        for kb_idx, kb_keymap in self.kb.items():
            self.grab_key(kb_keymap.key, X.Mod1Mask)

    def grab_key(self, codes, modifier):
        for code in codes:
            self.root.grab_key(code, modifier, 1, X.GrabModeAsync,
                               X.GrabModeAsync)

    def handle_key_press(self, event):
        for _, keymap in self.kb.items():
            if event.detail in keymap.key:
                keymap.op[0](event, **keymap.op[1])
                return
        print("unable to process key press")

    def move_window(self, event, **user_data):
        direction = user_data['dir']
        try:
            w = self.active_window
            if direction is "left":
                w.configure(x=w.get_geometry().x-5)
            elif direction is "right":
                w.configure(x=w.get_geometry().x+5)
            elif direction is "up":
                w.configure(y=w.get_geometry().y-5)
            elif direction is "down":
                w.configure(y=w.get_geometry().y+5)
            else:
                print("invalid direction")

        except AttributeError:
            print("no focused window")

    def destroy_window(self, event):
        try:
            self.active_window.destroy()
            self.window_list.remove(self.active_window)
            self.active_window = None
        except:
            print("no focused window")

    def run_proc(self, event, proc=""):
        proc_map = {
            "terminal": ["/usr/bin/urxvt"],
            "launcher": ["/usr/bin/rofi", "-show", "run"]
        }
        try:
            subprocess.Popen(proc_map[proc])
        except BaseException as error:
            print("Failed to launch", proc)

    def close_display(self):
        self.display.close()
