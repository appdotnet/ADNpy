.. _api_reference:

*************
API Reference
*************

This page contains some basic documentation for the ADNPy API

.. module:: adnpy.api

:mod:`adnpy.api` --- App.net API
================================
.. autoclass:: API

User Methods
============

A User is the central object of the App.net APIs. User objects have usernames, follow other users, and post content for their followers.
`See User Developer Docs <http://developers.app.net/docs/resources/user/>`_.

.. automethod:: adnpy.api.API.get_user
.. automethod:: adnpy.api.API.get_users
.. automethod:: adnpy.api.API.delete_post
.. automethod:: adnpy.api.API.update_user
.. automethod:: adnpy.api.API.patch_user
.. automethod:: adnpy.api.API.update_avatar
.. automethod:: adnpy.api.API.update_cover
.. automethod:: adnpy.api.API.follow_user
.. automethod:: adnpy.api.API.unfollow_user
.. automethod:: adnpy.api.API.mute_user
.. automethod:: adnpy.api.API.unmute_user
.. automethod:: adnpy.api.API.block_user
.. automethod:: adnpy.api.API.unblock_user
.. automethod:: adnpy.api.API.user_search
.. automethod:: adnpy.api.API.users_following
.. automethod:: adnpy.api.API.users_followers
.. automethod:: adnpy.api.API.users_following_ids
.. automethod:: adnpy.api.API.users_followers_ids
.. automethod:: adnpy.api.API.users_muted_users
.. automethod:: adnpy.api.API.users_muted_users_ids
.. automethod:: adnpy.api.API.users_blocked_users
.. automethod:: adnpy.api.API.users_blocked_user_ids
.. automethod:: adnpy.api.API.users_reposted_post
.. automethod:: adnpy.api.API.users_starred_post


Post Methods
============

A Post is the other central object utilized by the App.net Stream API.
`See Post Developer Docs <http://developers.app.net/docs/resources/post/>`_.

.. automethod:: adnpy.api.API.create_post
.. automethod:: adnpy.api.API.get_post
.. automethod:: adnpy.api.API.delete_post
.. automethod:: adnpy.api.API.repost_post
.. automethod:: adnpy.api.API.unrepost_post
.. automethod:: adnpy.api.API.star_post
.. automethod:: adnpy.api.API.unstar_post
.. automethod:: adnpy.api.API.get_posts
.. automethod:: adnpy.api.API.users_posts
.. automethod:: adnpy.api.API.users_starred_posts
.. automethod:: adnpy.api.API.users_mentioned_posts
.. automethod:: adnpy.api.API.posts_with_hashtag
.. automethod:: adnpy.api.API.posts_replies
.. automethod:: adnpy.api.API.unrepost_post
.. automethod:: adnpy.api.API.users_post_stream
.. automethod:: adnpy.api.API.users_post_stream_unified
.. automethod:: adnpy.api.API.posts_stream_global
.. automethod:: adnpy.api.API.report_post
.. automethod:: adnpy.api.API.post_search


Channel Methods
===============

A Channel is a user created stream of Messages. It controls access to the messages in the channel allowing for (among other things) public, private, and group messaging.
`See Channel Developer Docs <http://developers.app.net/docs/resources/channel/>`_.

.. automethod:: adnpy.api.API.subscribed_channels
.. automethod:: adnpy.api.API.create_channel
.. automethod:: adnpy.api.API.get_channel
.. automethod:: adnpy.api.API.get_channels
.. automethod:: adnpy.api.API.users_channels
.. automethod:: adnpy.api.API.num_unread_pm_channels
.. automethod:: adnpy.api.API.update_channel
.. automethod:: adnpy.api.API.subscribe_channel
.. automethod:: adnpy.api.API.unsubscribe_channel
.. automethod:: adnpy.api.API.subscribed_users
.. automethod:: adnpy.api.API.subscribed_user_ids
.. automethod:: adnpy.api.API.subscribed_user_ids_for_channels
.. automethod:: adnpy.api.API.mute_channel
.. automethod:: adnpy.api.API.unmute_channel
.. automethod:: adnpy.api.API.muted_channels


Message Methods
===============

A Message is very similar to a Post but 1) it doesn’t have to be public and 2) it will be delivered to an arbitrary set of users (not just the users who follow the Message creator).
`See Message Developer Docs <http://developers.app.net/docs/resources/message/>`_.

.. automethod:: adnpy.api.API.get_channel_messages
.. automethod:: adnpy.api.API.create_message
.. automethod:: adnpy.api.API.get_message
.. automethod:: adnpy.api.API.get_messages
.. automethod:: adnpy.api.API.users_messages
.. automethod:: adnpy.api.API.delete_message


File Methods
===============

A file is uploaded by a User and hosted by App.net.
`See File Developer Docs <http://developers.app.net/docs/resources/file/>`_.

.. automethod:: adnpy.api.API.create_file
.. automethod:: adnpy.api.API.update_file
.. automethod:: adnpy.api.API.set_file_content
.. automethod:: adnpy.api.API.get_file_content
.. automethod:: adnpy.api.API.create_custom_derived_file
.. automethod:: adnpy.api.API.set_custom_derived_file_content
.. automethod:: adnpy.api.API.get_custom_derived_file_content
.. automethod:: adnpy.api.API.get_file
.. automethod:: adnpy.api.API.get_files
.. automethod:: adnpy.api.API.delete_file
.. automethod:: adnpy.api.API.get_my_files


Interaction Methods
===================

Interactions are objects that represent users taking certain actions on App.net.
`See Interaction Developer Docs <http://developers.app.net/docs/resources/interaction/>`_.

.. automethod:: adnpy.api.API.interactions_with_user


Text Process Methods
====================

When a request is made to create a Post or Message, or update a User profile description, the provided body text is processed for entities. You can use this endpoint to test how App.net will parse text for entities as well as render text as html.
`See Text Process Developer Docs <http://developers.app.net/docs/resources/text-processor/>`_.

.. automethod:: adnpy.api.API.text_process


Token Methods
=============

Returns info about the current OAuth access token. If the token is a user token the response will include a User object.
`See Token Developer Docs <http://developers.app.net/docs/resources/token/>`_.

.. automethod:: adnpy.api.API.get_token


Config Methods
==============

.. automethod:: adnpy.api.API.get_config


Place Methods
=============

Place objects represent physical locations which can be given a name and associated with a latitude and longitude somewhere on Earth.
`See Place Developer Docs <http://developers.app.net/docs/resources/place/>`_.

.. automethod:: adnpy.api.API.get_place
.. automethod:: adnpy.api.API.search_places


Explore Streams
===============

An Explore Stream is a subset of all public posts flowing through App.net’s Global Stream. These Explore Streams are defined by App.net to provide developers and users new ways to discover posts.
`See Explore Streams Developer Docs <http://developers.app.net/docs/resources/explore/>`_.

.. automethod:: adnpy.api.API.get_explore_streams
.. automethod:: adnpy.api.API.get_explore_stream


Config Method
=============

The Configuration object contains variables which define the current behavior of the App.net platform.
`See Config Developer Docs <http://developers.app.net/docs/resources/config/>`_.

.. automethod:: adnpy.api.API.get_config

