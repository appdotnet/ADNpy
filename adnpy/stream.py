import json
import requests
from threading import Thread

from adnpy.models import (SimpleValueModel, Post, User, Channel, Message,
                         Token, File, StreamingMeta)


class StreamListener(object):
    """
    The StreamListener Object

    for every message type (post, star, user_follow, mute, block, stream_marker, message, channel, channel_subscription, token, file) you
    can define a on_<message_type> method to handle those messages.

    Example::

        class MyStreamListener(StreamListener):
            def on_post(self, post, meta):
                if meta.is_deleted:
                    return

                print post.text

            def on_star(self, post, user, meta):
                ...

    """
    def __init__(self, api):
        self.api = api

    def prepare_post(self, data):
        if not data:
            return tuple()

        return (
            Post.from_response_data(data, self.api),
        )

    def prepare_star(self, data):
        return (
            Post.from_response_data(data.get('post', {}), self.api),
            User.from_response_data(data.get('user', {}), self.api),
        )

    def prepare_user_follow(self, data):
        return (
            User.from_response_data(data.get('follows_user', {}), self.api),
            User.from_response_data(data.get('user', {}), self.api),
        )

    def prepare_mute(self, data):
        return (
            User.from_response_data(data.get('muted_user', {}), self.api),
            User.from_response_data(data.get('user', {}), self.api),
        )

    def prepare_block(self, data):
        return (
            User.from_response_data(data.get('blocked_user', {}), self.api),
            User.from_response_data(data.get('user', {}), self.api),
        )

    def prepare_stream_marker(self, data):
        return (
            SimpleValueModel.from_response_data(data.get('marker', {}), self.api),
            User.from_response_data(data.get('user', {}), self.api),
        )

    def prepare_message(self, data):
        return (
            Message.from_response_data(data, self.api),
        )

    def prepare_channel(self, data):
        return (
            Message.from_response_data(data, self.api),
        )

    def prepare_channel_subscription(self, data):
        return (
            Channel.from_response_data(data.get('channel', {}), self.api),
            User.from_response_data(data.get('user', {}), self.api),
        )

    def prepare_token(self, data):
        return (
            Token.from_response_data(data, self.api)
        )

    def prepare_file(self, data):
        return (
            File.from_response_data(data, self.api)
        )

    def prepare_fallback(self, data):
        return (
            SimpleValueModel.from_response_data(data, self.api)
        )

    def on_connect(self):
        """Called once connected to streaming server.

        This will be invoked once a successful response
        is received from the server. Allows the listener
        to perform some work prior to entering the read loop.
        """
        pass

    def on_data(self, raw_data):
        """Called when raw data is received from connection.

        Override this method if you wish to manually handle
        the stream data. Return False to stop stream and close connection.
        """
        data = json.loads(raw_data)

        message_type = data['meta'].get('type')
        prepare_method = 'prepare_%s' % (message_type)
        args = getattr(self, prepare_method, self.prepare_fallback)(data.get('data'))

        method_name = 'on_%s' % (message_type,)
        func = getattr(self, method_name, self.on_fallback)

        func(*args, meta=StreamingMeta.from_response_data(data.get('meta'), self.api))

    def on_fallback(self, data, meta):
        """Called when there is no specific method for handling an object type"""
        return

    def on_error(self, status_code):
        """Called when a non-200 status code is returned"""
        return False

    def on_timeout(self):
        """Called when stream connection times out"""
        return


class Stream(object):
    """
    The Stream Object

    Example::

        from adnpy.stream import Stream, StreamListener
        from adnpy.utils import get_app_access_token

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

    """
    def __init__(self, api, stream_defenition, listener_class, **options):
        self.api = api
        self.listener = listener_class(api)
        self.stream_defenition = stream_defenition
        self.running = False
        self.timeout = options.get("timeout", 600.0)
        self.retry_count = options.get("retry_count", 10)
        self.retry_time = options.get("retry_time", 10.0)
        self.snooze_time = options.get("snooze_time",  5.0)

    def _run(self):
        app_stream = None
        app_streams, meta = self.api.get_streams(key=self.stream_defenition['key'])
        if app_streams:
            app_stream = app_streams[0]

        if not app_stream:
            app_stream, meta = self.api.create_stream(data=self.stream_defenition)

        streaming_endpoint = app_stream.endpoint

        # Connect and process the stream
        error_counter = 0
        exception = None
        while self.running:
            if self.retry_count is not None and error_counter > self.retry_count:
                # quit if error count greater than retry count
                break
            try:
                resp = requests.get(streaming_endpoint, stream=True, timeout=self.timeout)
                resp.raise_for_status()
                if resp.status_code != 200:
                    if self.listener.on_error(resp.status_code) is False:
                        break
                    error_counter += 1
                    sleep(self.retry_time)
                else:
                    error_counter = 0
                    self.listener.on_connect()
                    self._read_loop(resp)
            except Exception, exception:
                # any other exception is fatal, so kill loop
                break

        # cleanup
        self.running = False

        if exception:
            raise

    def _data(self, data):
        if self.listener.on_data(data) is False:
            self.running = False

    def _read_loop(self, resp):

        while self.running:

            for line in resp.iter_lines(chunk_size=1):
                if line:
                    self._data(line)


    def start(self, async=False):
        self.running = True
        if async:
            Thread(target=self._run).start()
        else:
            self._run()

    def disconnect(self):
        if self.running is False:
            return
        self.running = False
