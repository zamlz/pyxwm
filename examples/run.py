
# This is a test file that shouldn't be really used.

import subprocess
from xwm.core.session import XwmSession
from xwm.commons.window_manager import WindowManager
from xwm.commons.keybinder import KeyBinder, KeyFunc

# Window manager object
winman = WindowManager()

# Create our session object
sess = XwmSession(winman=winman)

sess.onloop(winman.update_focus_hover)
sess.onloop(winman.window_update_serial)

def move_window(direction, delta):
    try:
        w = winman.active_window
        if direction is "left":
            w.configure(x = w.get_geometry().x - delta)
        if direction is "right":
            w.configure(x = w.get_geometry().x + delta)
        if direction is "up":
            w.configure(y = w.get_geometry().y - delta)
        if direction is "down":
            w.configure(y = w.get_geometry().y + delta)
        else:
            print("invalid direction")
    except AttributeError:
        print("no focused window")

def destroy_window():
    try:
        winman.active_window.destroy()
        winman.update_active(None)
    except:
        print("no focused window")

def start_process(sess, *proc):
    try:
        subprocess.Popen(*proc)
    except:
        print("Failed to launch: ", *proc)

def close_session(sess):
    sess.close_display()

# Configure the keybinder object
kb = KeyBinder(modifier='Alt')
kb['left'] = KeyFunc(move_window, args=['left', 4])
kb['right'] = KeyFunc(move_window, args=['right', 4])
kb['up'] = KeyFunc(move_window, args=['up', 4])
kb['down'] = KeyFunc(move_window, args=['down', 4])
kb['t'] = KeyFunc(start_process, args=["/usr/bin/urxvt"])
kb['e'] = KeyFunc(start_process, args=["/usr/bin/rofi", "-show", "run"])
kb['x'] = KeyFunc(destroy_window)
kb['escape'] = KeyFunc(close_session)

# Add the keybinds to the session
sess.add_keybinds(kb)

# Start the session
sess.run()
