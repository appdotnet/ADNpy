import adnpy


# Get an access token from the App.net website and paste it here.
adnpy.api.add_authorization_token('your access token here')

builder = adnpy.recipes.BroadcastMessageBuilder()

builder.channel_id = 24204  # Get this channel ID from the web publisher tools
builder.headline = 'Hello world!'
builder.text = 'Here is a [link](http://www.google.com) for my text body.'
builder.parse_markdown_links = True
builder.read_more_link = 'http://www.example.com'
# Path to a file:
# builder.photo = 'true_map06.jpg'

builder.send()
