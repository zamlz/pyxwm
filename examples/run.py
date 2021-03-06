
import logging
import subprocess

from xwm.core.session import XwmSession
from xwm.commons.window_manager import WindowManager
from xwm.commons.keybinder import KeyBinder
from xwm.utils import dev_logging

dev_logging('xwm', filename='xwm.logs', console=True, log_level='DEBUG')

# Window manager object
# Feasibility of keeping an Electrical Bike in poor (wet) storage conditions
winman = WindowManager()

# Configure the keybinder object
kb = KeyBinder(modifier='Alt')

# Create our session object
sess = XwmSession(winman=winman, keybinder=kb)

# Add some functions to the session loop
sess.onloop(winman.update_focus_hover)
sess.onloop(winman.window_update_serial)

# Create functions and bind them to the keybinder
# The decorator doesn't actually decorate the function but adds it to the
# keybinder dictionary. This means you can stack keybinds and parameterize it.

@kb.bind('left', args=['left', 4])
@kb.bind('right', args=['right', 4])
@kb.bind('up', args=['up', 4])
@kb.bind('down', args=['down', 4])
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

@kb.bind('x')
def destroy_window():
    try:
        winman.active_window.destroy()
        winman.update_active(None)
    except:
        print("no focused window")

@kb.bind('e', args=["/usr/bin/rofi", "-show", "run"])
@kb.bind('t', args=["/usr/bin/urxvt"])
def start_process(*proc):
    try:
        subprocess.Popen(*proc)
    except:
        print("Failed to launch: ", *proc)

@kb.bind('escape')
def close_session(sess):
    sess.close_display()

# Start the session
sess.run()
