from __future__ import absolute_import

"""App.net API library

.. moduleauthor:: Alex Kessinger <alex@app.net>

"""
__version__ = '0.3.7'
__author__ = 'Alex Kessinger, Bryan Berg, Mark Thurman, App.net'
__license__ = 'MIT'

from .models import User, Post, Message, Interaction, Channel, App, Token, Place
from .api import API
from .cursor import cursor

# Global, unauthenticated instance of API
api = API.build_api()

# This uses the default API client, so it must be created first
from . import recipes

__all__ = ['User', 'Post', 'Message', 'Interaction', 'Channel', 'App', 'Token', 'Place', 'API', 'api', 'cursor', 'recipes']
