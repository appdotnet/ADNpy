import os

import adnpy
from adnpy.stream import Stream, StreamListener
from adnpy.utils import get_app_access_token

client_id = os.environ.get('ADN_TEST_APP_CLIENT_ID')
client_secret = os.environ.get('ADN_TEST_CLIENT_SECRET')

app_access_token, token = get_app_access_token(client_id, client_secret)

# Define a stream
stream_def = {
    "object_types": [
        "post"
    ],
    "type": "long_poll",
    "key": "post_stream"
}

# Create a stream
class MyStreamListener(StreamListener):
    def on_post(self, post, meta):
        if meta.is_deleted:
            return

        print post.text

my_api = adnpy.API.build_api(access_token=app_access_token)
stream  = Stream(my_api, stream_def, MyStreamListener)

stream.start()