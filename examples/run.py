
# This is a test file that shouldn't be really used.

import subprocess
from xwm.core.session import XwmSession
from xwm.commons import KeyBinder, KeyFunc

process_map = {
    'terminal':
    "launcher":
}

# Every function that is added as a keybind must take a session as the first
# positional argument. You are allowed to have other arguments after that
# however.

def move_window(sess, direction, delta):
    try:
        w = sess.active_window
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

def destroy_window(sess):
    try:
        sess.active_window.destroy()
        sess.window_list.remove(sess.active_window)
        sess.active_window = None
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
kb['right'] = KeyFunc(move_window, args=['right', 4]
kb['up'] = KeyFunc(move_window, args=['up', 4]
kb['down'] = KeyFunc(move_window, args=['down', 4]
kb['t'] = KeyFunc(start_process, args=["/usr/bin/urxvt"])
kb['e'] = KeyFunc(start_process, args=["/usr/bin/rofi", "-show", "run"])
kb['x'] = KeyFunc(destroy_window)
kb['escape'] = KeyFunc(close_session)

# Create our session object
sess = XwmSession()

# Add the keybinds to the session
sess.add_keybinds(kb)

# Start the session
sess.run()
