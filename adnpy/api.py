import json
import re
import requests

from adnpy.models import SimpleValueModel, Model, APIModel, Post, User


class AdnError(Exception):
    def __init__(self, api_response):
        super(AdnError, self).__init__(api_response.meta.error_message)
        self.response = api_response
        self.error_id = api_response.meta.get('error_id')
        self.error_slug = api_response.meta.get('error_slug')

    def __str__(self):
        return "%s error_id: %s error_slug: %s" % (super(AdnError, self).__str__(), self.error_id, self.error_slug)

class AdnAPIException(AdnError):
    pass

class AdnAuthAPIException(AdnError):
    pass


class AdnRateLimitAPIException(AdnError):
    pass


class AdnInsufficientStorageException(AdnError):
    pass


class AdnPermissionDenied(AdnError):
    pass


class AdnMissing(AdnError):
    pass


PAGINATION_PARAMS = [
    'since_id',
    'before_id',
    'count',
]


POST_PARAMS =  [
    'include_muted',
    'include_deleted',
    'include_directed_posts',
    'include_machine',
    'include_starred_by',
    'include_reposters',
    'include_annotations',
    'include_post_annotations',
    'include_user_annotations',
    'include_html',
]

USER_PARAMS = [
    'include_annotations',
    'include_user_annotations',
    'include_html',
]

USER_SEARCH_PARAMS = [
    'q',
    'count',
]


POST_SEARCH_PARAMS = [
    'index',
    'order',
    'query',
    'text',
    'hashtags',
    'links',
    'link_domains',
    'mentions',
    'leading_mentions',
    'annotation_types',
    'attachment_types',
    'crosspost_url',
    'crosspost_domain',
    'place_id',
    'is_reply',
    'is_directed',
    'has_location',
    'has_checkin',
    'is_crosspost',
    'has_attachment',
    'has_oembed_photo',
    'has_oembed_video',
    'has_oembed_html5video',
    'has_oembed_rich',
    'language',
    'client_id',
    'creator_id',
    'reply_to',
    'thread_id',
]

def json_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, Model):
        return obj.serialize()

    return obj


class API(requests.Session):

    @classmethod
    def build_api(cls, api_root='https://alpha-api.app.net/stream/0', access_token=None):
        api = cls()
        api.api_root = api_root
        if access_token:
            api.add_authorization_token(access_token)

        return api

    def request(self, method, url, *args, **kwargs):
        if url:
            url =  self.api_root + url

        response = super(API, self).request(method, url, *args, **kwargs)

        response = APIModel.from_string(response.content, self)

        if response.meta.code == 401:
            raise AdnAuthAPIException(response)

        if response.meta.code == 403:
            raise AdnPermissionDenied(response)

        if response.meta.code == 404:
            raise AdnMissing(response)

        if response.meta.code == 429:
            raise AdnRateLimitAPIException(response)

        if response.meta.code == 507:
            raise AdnInsufficientStorageException(response)

        if response.meta.code != 200:
            raise AdnAPIException(response)

        return response

    def add_authorization_token(self, token):
        self.headers.update({
            'Authorization': 'Bearer %s' % (token),
        })

    def request_json(self, method, *args, **kwargs):
        kwargs.setdefault('headers', dict())
        kwargs['headers'].update({'Content-Type': 'application/json'})
        if kwargs.get('data'):
            if isinstance(kwargs.get('data'), Model):
                kwargs['data'] = kwargs['data'].serialize()

            kwargs['data'] = json.dumps(kwargs['data'], default=json_handler)

        return self.request(method, *args, **kwargs)

    def post_json(self, *args, **kwargs):
        return self.request_json('post', *args, **kwargs)

    def put_json(self, *args, **kwargs):
        return self.request_json('put', *args, **kwargs)


re_path_template = re.compile('{\w+}')


def identity(data, meta):
    return data, meta


def bind_api_method(func_name, path, payload_type=None, payload_list=False, allowed_params=None, method='GET', require_auth=True, content_type='JSON', processor=identity):
    allowed_params = allowed_params or []

    def run(self, *args, **kwargs):
        parameters = {}
        for key, val in kwargs.items():
            if key in allowed_params:
                parameters[key] = kwargs.pop(key)

        proccessed_path = path
        path_args = re_path_template.findall(path)
        for variable in path_args:
            args = list(args)
            try:
                value = args.pop(0)
            except IndexError:
                raise Exception('Not enough positional arguments expects: %s' % (path_args))

            value = unicode(getattr(value, 'id', value))
            proccessed_path = proccessed_path.replace(variable, value)
        resp_method = self.request
        if method in ('POST', 'PUT', 'PATCH') and content_type == 'JSON' and kwargs.get('data'):
            resp_method = self.request_json

        resp = resp_method(method, proccessed_path, params=parameters, **kwargs)
        if payload_list:
            resp.data = [payload_type.from_response_data(x, api=self) for x in resp.data]
        else:
            resp.data = payload_type.from_response_data(resp.data, api=self)

        return processor(resp.data, resp.meta)

    setattr(API, func_name, run)

# Post methods

bind_api_method('write_post', '/posts', payload_type=Post, method='POST',
                allowed_params=POST_PARAMS,
                require_auth=True)

bind_api_method('get_post', '/posts/{post_id}', payload_type=Post,
                allowed_params=POST_PARAMS,
                require_auth=False)

bind_api_method('delete_post', '/posts/{post_id}', payload_type=Post, method='DELETE',
                allowed_params=POST_PARAMS,
                require_auth=True)

bind_api_method('repost_post', '/posts/{post_id}/repost', payload_type=Post, method='POST',
                allowed_params=POST_PARAMS,
                require_auth=True)

bind_api_method('unrepost_post', '/posts/{post_id}/repost', payload_type=Post, method='DELETE',
                allowed_params=POST_PARAMS,
                require_auth=True)

bind_api_method('star_post', '/posts/{post_id}/star', payload_type=Post, method='POST',
                allowed_params=POST_PARAMS,
                require_auth=True)

bind_api_method('unstar_post', '/posts/{post_id}/star', payload_type=Post, method='DELETE',
                allowed_params=POST_PARAMS,
                require_auth=True)

bind_api_method('get_posts', '/posts', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS + ['ids'],
                require_auth=True)

bind_api_method('users_posts', '/users/{user_id}/posts', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS,
                require_auth=True)

bind_api_method('users_starred_posts', '/users/{user_id}/stars', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS,
                require_auth=True)

bind_api_method('users_mentioned_posts', '/users/{user_id}/mentions', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS,
                require_auth=True)

bind_api_method('posts_with_hashtag', '/posts/tag/{hashtag}', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS,
                require_auth=False)

bind_api_method('posts_replies', '/posts/{post_id}/replies', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS,
                require_auth=True)

bind_api_method('users_post_stream', '/posts/stream', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS,
                require_auth=True)

bind_api_method('users_post_stream_unified', '/posts/stream/unified', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS,
                require_auth=True)

bind_api_method('posts_stream_global', '/posts/stream/global', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS,
                require_auth=False)

bind_api_method('report_post', '/posts/{post_id}/report', payload_type=Post,
                allowed_params=POST_PARAMS,
                require_auth=True)

bind_api_method('post_search', '/posts/search', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS + POST_SEARCH_PARAMS,
                require_auth=True)


# User methods

bind_api_method('get_user', '/users/{user_id}', payload_type=User,
                allowed_params=USER_PARAMS,
                require_auth=False)

bind_api_method('get_users', '/users', payload_type=User, payload_list=True,
                allowed_params=USER_PARAMS + ['ids'],
                require_auth=False)

bind_api_method('update_user', '/users/{user_id}', payload_type=User, method='PUT',
                allowed_params=USER_PARAMS,
                require_auth=True)

bind_api_method('patch_user', '/users/{user_id}', payload_type=User, method='PATCH',
                 allowed_params=USER_PARAMS,
                 require_auth=True)

bind_api_method('update_avatar', '/users/me/avatar', payload_type=User, method='POST',
                 allowed_params=USER_PARAMS,
                 require_auth=True)

bind_api_method('update_cover', '/users/me/cover', payload_type=User, method='POST',
                 allowed_params=USER_PARAMS,
                 require_auth=True)

bind_api_method('follow_user', '/users/{user_id}/follow', payload_type=User, method='POST',
                 allowed_params=USER_PARAMS,
                 require_auth=True)

bind_api_method('unfollow_user', '/users/{user_id}/follow', payload_type=User, method='DELETE',
                 allowed_params=USER_PARAMS,
                 require_auth=True)

bind_api_method('mute_user', '/users/{user_id}/mute', payload_type=User, method='POST',
                 allowed_params=USER_PARAMS,
                 require_auth=True)

bind_api_method('unmute_user', '/users/{user_id}/mute', payload_type=User, method='DELETE',
                 allowed_params=USER_PARAMS,
                 require_auth=True)


bind_api_method('block_user', '/users/{user_id}/block', payload_type=User, method='POST',
                 allowed_params=USER_PARAMS,
                 require_auth=True)

bind_api_method('unblock_user', '/users/{user_id}/block', payload_type=User, method='DELETE',
                 allowed_params=USER_PARAMS,
                 require_auth=True)

bind_api_method('user_search', '/users/search', payload_type=User, payload_list=True,
                 allowed_params=USER_PARAMS + USER_SEARCH_PARAMS,
                 require_auth=True)

bind_api_method('users_following', '/users/{user_id}/following', payload_type=User, payload_list=True,
                 allowed_params=USER_PARAMS,
                 require_auth=True)

bind_api_method('users_followers', '/users/{user_id}/followers', payload_type=User, payload_list=True,
                 allowed_params=USER_PARAMS,
                 require_auth=True)

bind_api_method('users_following_ids', '/users/{user_id}/following/ids', payload_type=SimpleValueModel, payload_list=True,
                 allowed_params=USER_PARAMS,
                 require_auth=True)

bind_api_method('users_followers_ids', '/users/{user_id}/followers/ids', payload_type=SimpleValueModel, payload_list=True,
                 allowed_params=USER_PARAMS,
                 require_auth=True)

bind_api_method('users_muted_users', '/users/{user_id}/muted', payload_type=User, payload_list=True,
                 allowed_params=USER_PARAMS,
                 require_auth=True)

bind_api_method('users_muted_users_ids', '/users/{user_id}/muted', payload_type=User, payload_list=True,
                 allowed_params=USER_PARAMS,
                 require_auth=True)

bind_api_method('users_blocked_users', '/users/{user_id}/blocked', payload_type=User, payload_list=True,
                 allowed_params=USER_PARAMS,
                 require_auth=True)

bind_api_method('users_blocked_users_ids', '/users/blocked/ids', payload_type=SimpleValueModel, payload_list=True,
                 allowed_params=USER_PARAMS + ['ids'],
                 require_auth=True)


bind_api_method('users_reposted_post', '/posts/{post_id}/reposters', payload_type=User, payload_list=True,
                 allowed_params=USER_PARAMS,
                 require_auth=True)

bind_api_method('users_starred_post', '/posts/{post_id}/stars', payload_type=User, payload_list=True,
                 allowed_params=USER_PARAMS,
                 require_auth=True)
