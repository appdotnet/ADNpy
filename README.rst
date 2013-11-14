ADNpy: App.net API for Python
=============================

.. image:: https://badge.fury.io/py/adnpy.png
    :target: http://badge.fury.io/py/adnpy

.. image:: https://travis-ci.org/appdotnet/ADNpy.png?branch=master
    :target: https://travis-ci.org/appdotnet/ADNpy


ADNpy aims to be an easy to use python library for interacting with the `App.net API <https://developers.app.net>`_.

Installation
------------

To install Requests, simply:

.. code-block:: bash

    $ pip install adnpy

Documentation
-------------

Documentation is available at http://adnpy.readthedocs.org/.

Quick Start
-----------

You are going to need an access token. If you do not already have one first `create an app`_, then generate an access token for your app.

.. code-block:: python

    import adnpy
    adnpy.api.add_authorization_token(<Access Token Here>)

    # Create a post
    post, meta = adnpy.api.create_post(text='Hello, App.net from adnpy.')

    # Take a look at recent checkins
    posts, meta = adnpy.api.get_explore_stream('checkins')
    for post in posts:
      print post

    # You can even paginate through checkins using the cursor
    # Using the cursor will obey rate limits, and theoretically
    # allow you to page through the entire stream.
    for post in adnpy.cursor(adnpy.api.get_explore_stream, 'checkins'):
        print post

.. _create an app: https://account.app.net/developer/apps/
