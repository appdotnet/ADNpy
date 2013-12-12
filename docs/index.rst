ADNPy: App.net API for Python
=============================

ADNPy aims to be a easy to use library for interacting with the `App.net API <https://developers.app.net>`_.

Installation
--------------
::

    pip install adnpy

You may also use Git to clone the repository from
Github and install it manually::

    git clone https://github.com/appdotnet/adnpy.git
    python setup.py install

Quick Start
-----------

ADNPy aims to be an easy-to-use Python client for the App.net API. To get
started, you'll need an access token, which you can get by `creating an app
<https://account.app.net/developer/apps/>`_ on App.net and clicking the
"Generate a user token" link.

.. code-block:: python

    import adnpy

    # Set the default access token for API calls.
    adnpy.api.add_authorization_token('your access token here')

    # Send a broadcast with the BroadcastMessageBuilder recipe.
    builder = adnpy.recipes.BroadcastMessageBuilder(api)
    builder.channel_id = 24204  # Get this channel ID from the web publisher tools
    builder.headline = 'Hello World!'
    builder.text = 'Sending this from [ADNPy](https://github.com/appdotnet/ADNPy) was easy!'
    builder.parse_markdown_links = True
    builder.read_more_link = 'http://adnpy.readthedocs.org/'
    builder.send()

    # Or create a post using the API module.
    post, meta = adnpy.api.create_post(text='Hello from ADNPy!')


Reference
---------

.. toctree::
   :maxdepth: 2

   getting_started.rst
   recipes.rst
   model_reference.rst
   api_reference.rst
   streaming.rst
