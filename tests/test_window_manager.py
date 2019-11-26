
from xwm.commons.window_manager import WindowManager

def test_update_active_with_good_window():
    """
    Tests: WindowManager.update_active
        Instead of using a window object, we use 3 and 'three' as the window
        object and window name respectively. The window is 'Good' here because
        it is added to the WindowManager._window_list prior to setting the
        window as active.
    """
    wm = WindowManager()
    assert wm.active == (None, '')
    wm._window_list.append(3)
    wm.update_active(3, name='three')
    assert wm.active == (3, 'three')
