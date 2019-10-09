
from setuptools import setup, find_packages

with open('requirements.txt', 'r') as req_file:
    required_packages = [ pkg.rstrip() for pkg in req_file ]

setup(
    name='pyxwm',
    version='0.0.1',
    description='Python X Window Manager',
    author='Amlesh Sivanantham',
    author_email='samlesh@gmail.com',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=required_packages
)
