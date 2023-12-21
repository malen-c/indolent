import os
from distutils.core import setup

# horrible airplane solution
modules = [x.strip('.py') for x in os.listdir('C:/users/malen/desktop/python/indolent/indolent') if x != 'seutp.py' and x != '__init__.py']
setup(name='indolent',
      version='1.0',
      py_modules=modules,
      )
