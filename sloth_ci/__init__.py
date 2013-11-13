"""
*******
Sloth
*******

**Sloth** is a lightweight CI script to perform push-based actions.

The repo is at `bitbucket.org/moigagoo/configs <https://bitbucket.org/moigagoo/configs>`_.
"""

__title__ = 'sloth-ci'
__version__ = '0.3.2'
__author__ = 'Konstantin Molchanov'
__license__ = 'MIT'

from .sloth import Sloth
from .api import main
