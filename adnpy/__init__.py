"""
App.net API library
"""
__version__ = '0.1'
__author__ = 'Alex Kessinger'
__license__ = 'MIT'

from adnpy.models import User, Post, Message, Interaction, Channel, App
from adnpy.api import API
from adnpy.cursor import Cursor


# Global, unauthenticated instance of API
api = API()

__all__ = [User, Post, Message, Interaction, Channel, App, API, Cursor, api]

def debug(enable=True, level=1):

    import httplib
    httplib.HTTPConnection.debuglevel = level

