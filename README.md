# ADNpy: App.net API for Python

ADNpy aims to be a easy to use library for interacting with the [App.net API](https://developers.app.net).

[http://adnpy.readthedocs.org/](http://adnpy.readthedocs.org/)

## Installation

    pip install adnpy

You may also use Git to clone the repository from
Github and install it manually:

    git clone https://github.com/appdotnet/adnpy.git
    python setup.py install

## Quick Start

You are going to need an access_token, if you don't have a developer account on App.net you can checkout [dev-lite](http://dev-lite.jonathonduerig.com/).

```python
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
```
