.. _getting_started:


***************
Getting started
***************

Introduction
============

ADNPy aims to be a seemless integration with the App.net API. To get started
you should make sure you have an access token. If you don't have an
App.net developer account, you can use `dev-lite <http://dev-lite.jonathonduerig.com/>`_ to generate a token
just for your user account.

Obligatory, Hello World
=======================

.. code-block :: python

   import adnpy


   adnpy.api.add_authorization_token('<Your Access Token Here>')   
   posts, meta = adnpy.api.users_post_stream()
   for post in posts:
       print post.text

In this example, you are fetching the last 20 posts created by the
authenticated user, and then iterating over them to print them out.


API
===

The API class provides methods for each App.net endpoint. To find more information
about each method checkout the 
:ref:`api_reference`. 

Models
======

API calls normally return APIModels. There is an APIModel for common
entities like Posts, Users, and Channels. APIModels are basically just
special dict objects. You can access information using dot notation or use
normal dict methods::

   # given a post object
   print post.text
   print post.get('text')
   print post.get('user', None)

Each model can also preform certain API calls customized to the current
model instance::

   post.delete()

For more information about models please see :ref:`model_reference`..
