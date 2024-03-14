import os
from distutils.core import setup

# horrible airplane solution
modules = [
    x[:-3]
    for x in os.listdir('C:/users/malen/desktop/python/indolent/indolent')
    if x.endswith('.py') and x != 'setup.py' and x != '__init__.py'
]
setup(
    name='indolent',
    version='1.0',
    py_modules=modules,
)
