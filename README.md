Python X Window Manager
=======================

Setup
-----

### Virtual Environment

This is the best way to have the code setup on your systme without it
interfering with your system python.

Start by making a virtual environment and activate it.

```bash
$ python -m venv ${PATH_TO_VIRTUAL_ENV}
$ ${PATH_TO_VIRTUAL_ENV}/bin/activate
```

You can test that you are in the virtual environment with `which python` and
`which pip` and ensure that are in your virtual environment's path.

### Installing the package

Next clone this repo to wherever you want and cd into the directory

```bash
$ git clone https://github.com/zamlz/pyxwm.git
$ cd pyxwm
```

Now you need to install the package. It will also install all the necessary
dependencies as well.
Make sure you are in the root of the git repository (the
folder which has the `setup.py` file in it).

To install to your site-packages, use

```bash
$ pip install .
```

To install in develop mode, use

```bash
$ pip install -e .
```

### Writing the Window Manager Script

Now you'll need to write a python script that uses this package. Luckily we
have a test script thats already available as `examples/run.py`. To set this
up, you'll need to figure out how you can enable other window managers.

### Running the Window Manager

If you use the program startx, you can edit your `xinitrc` file to have the
following line at the very end. Essentially we will be starting a python
instance that runs the script from the previous section. __Make sure you
use your virtual environment's python binary if you are using a virtual
environment here!__

```bash
exec ${PATH_TO_PYTHON_BIN} ${PROJECT_PATH/examples/run.py
```

Important Resources
-------------------

[https://tronche.com/gui/x/xlib/](https://tronche.com/gui/x/xlib/)

[http://python-xlib.sourceforge.net/doc/html/index.html](http://python-xlib.sourceforge.net/doc/html/index.html)
