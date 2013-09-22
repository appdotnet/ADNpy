import os
from unittest import TestCase

from httreplay import start_replay, stop_replay, filter_headers_key

from adnpy.api import API

username = os.environ.get('ADN_USERNAME', 'adnpy')
access_token = os.environ.get('ADN_TEST_ACCESS_TOKEN')
use_replay = os.environ.get('USE_REPLAY', True)

class AdnpyTestCase(TestCase):

    def setUp(self):
        self.api = API.build_api()
        self.username = username
        if access_token:
            self.api.add_authorization_token(access_token)

        if use_replay:

            start_replay('tests/data/record.json', headers_key=filter_headers_key(['Authorization']))

    def tearDown(self):
        if use_replay:
            stop_replay()
