
from xwm.commons.window_manager import WindowManager

def test_update_active():
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

def test__spawn_window():
    """
    Tests: WindowManager.spawn
        Test if a window spawns correctly and sets it as active. We use 4 and
        'four' as the window object and window name respectively.
    """
    wm = WindowManager()
    assert wm.active == (None, '')

    wm.spawn(4, 'four', active=True)
    assert wm.active == (4, 'four')
    assert wm._window_list == [4]

    wm.spawn(5, 'five', active=True)
    assert wm.active == (5, 'five')
    assert wm._window_list == [4, 5]

    wm.spawn(6, 'six', active=False)
    assert wm.active == (5, 'five')
    assert wm._window_list == [4, 5, 6]

