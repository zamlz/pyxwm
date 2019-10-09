
from setuptools import setup, find_packages

setup(
    name='pyxwm',
    version='0.0.1',
    description='Python X Window Manager',
    author='Amlesh Sivanantham',
    author_email='samlesh@gmail.com',
    package_dir={'': 'src'},
    packages=find_packages('src')
)
