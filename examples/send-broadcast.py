import adnpy
from adnpy.recipes import BroadcastMessageBuilder


# Get an access token from the App.net website and paste it here.
api = adnpy.API.build_api(access_token='')

builder = BroadcastMessageBuilder(api)

builder.channel_id = 24204  # Get this channel ID from the web publisher tools
builder.headline = 'Hello world!'
builder.text = 'Here is a [link](http://www.google.com) for my text body.'
builder.parse_markdown_links = True
builder.read_more_link = 'http://www.example.com'
builder.photo = 'true_map06.jpg'

builder.send()
