ADNpy: App.net API for Python
=============================

.. image:: https://badge.fury.io/py/adnpy.png
    :target: http://badge.fury.io/py/adnpy

.. image:: https://travis-ci.org/appdotnet/ADNpy.png?branch=master
    :target: https://travis-ci.org/appdotnet/ADNpy


ADNpy aims to be an easy-to-use Python library for interacting with the `App.net API <https://developers.app.net>`_.

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

In order to use ADNpy, You'll to need an access token. If you don't already have one, first `create an app`_, and then generate an access token for your app.

.. code-block:: python

    import adnpy
    adnpy.api.add_authorization_token(<Access Token Here>)

    # Create a post
    post, meta = adnpy.api.create_post(data={'text':'Hello App.net from adnpy!'})

    # Take a look at recent checkins
    posts, meta = adnpy.api.get_explore_stream('checkins')
    for post in posts:
      print post

    # You can even paginate through checkins using the cursor method.
    # Cursors will obey rate limits (by blocking until retries are
    # permitted), and will allow you to page through the entire stream.
    for post in adnpy.cursor(adnpy.api.get_explore_stream, 'checkins'):
        print post

.. _create an app: https://account.app.net/developer/apps/
