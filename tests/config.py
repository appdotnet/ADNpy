import os
from unittest import TestCase

from httreplay import start_replay, stop_replay, filter_headers_key

from adnpy.api import API

username = os.environ.get('ADN_USERNAME', 'adnpy')
access_token = os.environ.get('ADN_TEST_ACCESS_TOKEN')
client_id = os.environ.get('ADN_TEST_APP_CLIENT_ID')
client_secret = os.environ.get('ADN_TEST_CLIENT_SECRET')

# This is for travis
access_token_part_a = os.environ.get('ADN_TEST_ACCESS_TOKEN_A')
access_token_part_b = os.environ.get('ADN_TEST_ACCESS_TOKEN_B')
if access_token_part_a and access_token_part_b:
    access_token = access_token_part_a + access_token_part_b

use_replay = os.environ.get('USE_REPLAY', 'False') == 'True'


class AdnpyTestCase(TestCase):

    def setUp(self):
        self.api = API.build_api()
        self.username = username
        if access_token:
            self.api.add_authorization_token(access_token)

        self.client_id = client_id
        self.client_secret = client_secret

        if use_replay:
            start_replay('tests/data/record.json', headers_key=filter_headers_key(['Authorization']))

    def tearDown(self):
        if use_replay:
            stop_replay()
