.. _getting_started:


***************
Getting started
***************

Introduction
============

ADNPy aims to be an easy-to-use Python client for the App.net API. To get
started, you'll need an access token, which you can get by `creating an app
<https://account.app.net/developer/apps/>`_ on App.net and clicking the
"Generate a user token" link.

The Obligatory Hello World Example
==================================

.. code-block :: python

   import adnpy

   # Add an access token to authorize access to your account
   adnpy.api.add_authorization_token('your access token here')

   # Create a post
   post, meta = adnpy.api.create_post(data={'text': 'Hello World'})

This example creates a simple post on your App.net Stream.

Recipes
=======

Recipes are simple ways to use the App.net API which shield you from having to
learn about resources, entities, annotations, and all of that -- find out more
on the :ref:`recipes` page.

API
===

The API class provides methods for each App.net endpoint. To find more information
about each method, check out the :ref:`api_reference`.

Models
======

API calls normally return APIModel objects. There's an APIModel for each common
`App.net resource <http://developers.app.net/docs/resources/>`_, like Post,
User, and Channel. APIModels are essentially just subclasses of `dict`, with
extra syntacical sugar allowing you to access information via dot notation or
normal dict methods::

   # given a post object
   print post.text
   print post.get('text')
   print post.get('user', None)

Each model can also preform certain API calls customized to the current
model instance::

   post.delete()

For more information about models, please see the :ref:`model_reference`.
