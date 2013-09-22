import os
import time
import unittest

from adnpy.cursor import cursor
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

    def test_channel(self):

        channels, meta = self.api.subscribed_channels()

        channel, meta = self.api.create_channel(data={
            'type': 'com.example.channel',
            'writers': {
                'user_ids': ['@voidfiles'],
                'immutable': False,
            }
        })

        channel_fetched, meta = self.api.get_channel(channel)
        self.assertEquals(channel.id, channel_fetched.id)


        channels, meta = self.api.get_channels(ids=channel_fetched.id)

        channels, meta = self.api.users_channels()

        num_unread, meta = self.api.num_unread_pm_channels()

        channel_update = {
            'id': channel.id,
            'writers': {
                'user_ids': [],
            }
        }

        channel, meta = self.api.update_channel(channel, data=channel_update)
        self.assertEquals(channel_update['writers']['user_ids'], channel.writers.user_ids)

        channel, meta = self.api.subscribe_channel(1383)
        channel, meta = self.api.unsubscribe_channel(1383)

        users, meta = self.api.subscribed_users(1383)
        users, meta = self.api.subscribed_user_ids(1383)

        channel_user_ids, meta = self.api.subscribed_user_ids_for_channels(ids='1383,6313')

        channel, meta = self.api.mute_channel(1383)
        channels, meta = self.api.muted_channels(1383)
        channel, meta = self.api.unmute_channel(1383)

    def test_message(self):

        message1, meta = self.api.create_message(27024, data={'text': "awesome 1"})
        message2, meta = self.api.create_message(27024, data={'text': "awesome 2"})
        message, meta = self.api.get_message(27024, message1)
        messages, meta = self.api.get_messages(ids='%s, %s' % (message1.id, message2.id))
        self.assertEquals(len(messages), 2)
        messages, meta = self.api.users_messages()
        self.assertEquals(len(messages), 2)

        message, meta = self.api.delete_message(27024, message1)
        message, meta = self.api.delete_message(27024, message2)

    def test_interactions(self):

        interactions, meta = self.api.interactions_with_user()


    def test_text_process(self):
        text, meta = self.api.text_process(data={'text': "#awesome @voidfiles"})


    def test_places(self):
        places, meta = self.api.search_places(q='krispy kreme', latitude='37.701598', longitude='-122.470093', radius='50000')

        place, meta = self.api.get_place(places[0])


    def test_token(self):
        token, meta = self.api.get_token()
        self.assertIsNotNone(token.get('user'))

    def test_config(self):
        config, meta = self.api.get_config()

    def test_explore_stream(self):
        explore_streams, meta = self.api.get_explore_streams()
        posts, meta = self.api.get_explore_stream(explore_streams[0])

    def test_cursor(self):
        iterator = cursor(self.api.posts_stream_global, count=1)
        post1 = iterator.next()
        post2 = iterator.next()
        self.assertNotEquals(post1.id, post2.id)

        iterator = cursor(self.api.get_explore_stream, 'photos')
        post1 = iterator.next()

if __name__ == '__main__':
    unittest.main()
