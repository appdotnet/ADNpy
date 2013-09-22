import os
import time
import unittest

from config import AdnpyTestCase

test_post_id = 1

"""Unit tests"""
class AdnpyAPITests(AdnpyTestCase):

    def test_posts_stream_global(self):
        self.api.posts_stream_global()

    def test_post(self):
        text = u'awesome'
        post, meta = self.api.write_post(data={'text': text})
        self.assertEquals(post.text, text)

        post, meta = self.api.get_post(post)

        post, meta = self.api.delete_post(post)
        post, meta = self.api.write_post(data={'text': text})
        post, meta = post.delete()

        post, meta = self.api.repost_post(1)
        post, meta = self.api.unrepost_post(1)

        post, meta = self.api.star_post(1)
        post, meta = self.api.unstar_post(1)

        posts, meta = self.api.get_posts(ids='1,2,3')
        self.assertEquals(len(posts), 3)

        posts, meta = self.api.users_posts(3)

        posts, meta = self.api.users_starred_posts(3)
        posts, meta = self.api.users_mentioned_posts(3)

        posts, meta = self.api.posts_with_hashtag('awesome')

        posts, meta = self.api.posts_with_hashtag(1)

        posts, meta = self.api.users_post_stream()
        posts, meta = self.api.users_post_stream_unified()

        posts, meta = self.api.posts_stream_global()

        # post, meta = self.api.report_post(1)

        posts, meta = self.api.post_search(text='awesome')


    def test_user(self):
        display_name = u'tester %s' % (time.time())
        user, meta = self.api.get_user('me')
        self.assertEquals(self.username, user.username)
        old_name = user.name
        user.name = display_name
        cwd = os.path.dirname(__file__)
        del user.description['entities']
        user, meta = self.api.update_user('me', data=user)
        self.assertEquals(display_name, user.name)

        user, meta = self.api.patch_user('me', data={'name': old_name})
        self.assertEquals(old_name, user.name)

        users, meta = self.api.get_users(ids='1,2,3')
        self.assertEquals(len(users), 3)

        # XXX: Need to figure out how I can record, and replay these calls, but they work

        #avatar = open(cwd + '/data/avatar.png')
        #user, meta = self.api.update_avatar('me', files={'avatar': avatar})

        #cover = open(cwd + '/data/cover.png')
        #user, meta = self.api.update_cover('me', files={'cover': cover})

        user, meta = self.api.follow_user(3)
        user, meta = self.api.unfollow_user(3)

        user, meta = self.api.mute_user(3)
        user, meta = self.api.unmute_user(3)

        user, meta = self.api.block_user(3)
        user, meta = self.api.unblock_user(3)

        users, meta = self.api.user_search(q='@voidfiles')

        users, meta = self.api.users_following(3)
        users, meta = self.api.users_followers(3)

        users, meta = self.api.users_following_ids(3)
        users, meta = self.api.users_followers_ids(3)

        users, meta = self.api.users_muted_users('me')
        users, meta = self.api.users_muted_users_ids('me')

        users, meta = self.api.users_blocked_users('me')

        # Add in testing for app access tokens
        #users, meta = self.api.users_blocked_users_ids('me')

        users, meta = self.api.users_reposted_post(1)
        users, meta = self.api.users_starred_post(1)


if __name__ == '__main__':
    unittest.main()
