import os
import time
import unittest

from config import AdnpyTestCase

test_post_id = 1

"""Unit tests"""
class AdnpyModelTests(AdnpyTestCase):

    def test_post(self):
        text = u'Testing posts indvidually'
        post, meta = self.api.create_post(data={'text': text})
        post.star()
        post.unstar()
        post.delete()
        post, meta = self.api.get_post(1)
        post.repost()
        post.unrepost()

    def test_user(self):
        new_display_name = u'tester %s' % (time.time())
        user, meta = self.api.get_user('me')

        user.name = new_display_name
        user.update_user()
        self.assertEquals(user.name, new_display_name)

        user, meta = self.api.get_user(3)
        user.follow_user()
        user.unfollow_user()

        user.mute_user()
        user.unmute_user()

        user.block_user()
        user.unblock_user()


if __name__ == '__main__':
    unittest.main()
