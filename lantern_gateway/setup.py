from catkin_pkg.python_setup import generate_distutils_setup
from setuptools import setup

setup_args = generate_distutils_setup(
    packages=['gateway'],
    package_dir={'': 'src'},
    install_requires=['tornado']
)

setup(**setup_args)