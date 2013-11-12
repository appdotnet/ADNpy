"""
.. module:: models
   :synopsis: Simple abstractions of App.net entities.

"""
import collections
from dateutil.parser import parse
import json


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except:
        return False


def is_seq_not_string(obj):
    if isinstance(obj, basestring):
        return False

    return is_iterable(obj)


class SimpleValueModel(object):
    @classmethod
    def from_response_data(cls, data, api):
        return data


class SimpleValueDictListMode(object):
    @classmethod
    def from_response_data(cls, data, api):
        return {key:[int(x) for x in val] for key, val in data}


class APIModel(dict):
    """
    The base class for all API Models.

    It has no special deserialization functionality. It is suitable for generic object.

    Instead of initializing this directly you should use the :func:`Model.from_string` class method::

        model = Model.from_string(raw_json, api)

    Or, if you already have a dict you can initialize it like so::

        model = Model.from_response_data(data, api)

    """
    def __setattr__(self, name, val):
        return self.__setitem__(name, val)

    def __getattr__(self, name):
        try:
            return self.__getitem__(name)
        except KeyError:
            raise AttributeError(name)

    def __init__(self, data=None, api=None):
        super(APIModel, self).__init__()
        self['_api'] = api
        if not data:
            return

        for k, v in data.iteritems():
            if isinstance(v, collections.Mapping):
                self[k] = APIModel(v, api)
            elif v and is_seq_not_string(v) and isinstance(v[0], collections.Mapping):
                self[k] = [APIModel(i, api) for i in v]
            else:
                self[k] = v


        annotations = self.get('annotations')
        if annotations:
            self.annotations_by_key = collections.defaultdict(list)
            for annotation in annotations:
                self.annotations_by_key[annotation.type].append(annotation.get('value', {}))

    @classmethod
    def from_string(cls, raw_json, api=None):
        """
       :param raw_json: a json response from the API
       :param api: an instance of :class:`adnpy.api.API`
       :rtype: model obj
        """
        return cls(json.loads(raw_json), api)


    @classmethod
    def from_response_data(cls, data, api=None):
        """
       :param data: a dict
       :param api: an instance of :class:`adnpy.api.API`
       :rtype: model obj
        """
        model = cls(data, api)
        return model


    def serialize(self):
        """
        Converts :class:`adnpy.models.Model` into a normal dict without references to the api
        """

        data = {}
        for k, v in self.iteritems():
            if k.startswith('_'):
              continue

            if isinstance(v, APIModel):
              data[k] = v.serialize()
            elif v and is_seq_not_string(v) and isinstance(v[0], APIModel):
              data[k] = [x.serialize() for x in v]
            else:
              data[k] = v

        return data

    def get_annotation(self, key, result_format='list'):
        """
        Is a convenience method for accessing annotations on models that have them
        """
        value = self.get('annotations_by_key', {}).get(key)
        if not value:
            return value

        if result_format == 'one':
            return value[0]

        return value

    def __unicode__(self):
        self.serialize().__unicode__()

    def __getstate__(self):
        return self.serialize()


class User(APIModel):
    """
    The User Model
    """
    @classmethod
    def from_response_data(cls, data, api=None):
        user = super(User, cls).from_response_data(data, api)
        user.id = int(user.id)
        user.created_at = parse(user.created_at)

        return user

    def update_user(self):
        """
        Save the state of the current user
        """
        # First create a copy of the current user
        user_dict = self.serialize()
        # Then delete the entities in the description field
        del user_dict['description']['entities']
        # Then upload user_dict
        user, meta = self._api.update_user('me', data=user_dict)

    def follow_user(self):
        """
        Follow this user
        """
        return self._api.follow_user(self)

    def unfollow_user(self):
        """
        Unfollow this user
        """
        return self._api.unfollow_user(self)

    def mute_user(self):
        """
        Mute this user
        """
        return self._api.mute_user(self)

    def unmute_user(self):
        """
        Unmute this user
        """
        return self._api.unmute_user(self)

    def block_user(self):
        """
        Block this user
        """
        return self._api.block_user(self)

    def unblock_user(self):
        """
        Unblock this user
        """
        return self._api.unblock_user(self)


class Post(APIModel):
    """
    The Post Model
    """
    @classmethod
    def from_response_data(cls, data, api=None):
        post = super(Post, cls).from_response_data(data, api)
        post.id = int(post.id)
        if 'user' in post:
            post.user = User.from_response_data(post.user, api)
        else:
            post.user = None

        post.starred_by = [User.from_response_data(u, api) for u in post.get('starred_by', [])]
        post.reposters = [User.from_response_data(u, api) for u in post.get('reposters', [])]

        post.created_at = parse(post.created_at)

        # If there is a repost object setup the avatar assets for it as well
        repost_of = post.get('repost_of')
        if repost_of:
            post.repost_of = Post.from_response_data(post.repost_of, api)

        return post

    def delete(self):
        """
        Delete this post
        """
        return self._api.delete_post(self)

    def repost(self):
        """
        Repost this post
        """
        return self._api.repost_post(self)


    def unrepost(self):
        """
        Remove repost of this post
        """
        return self._api.unrepost_post(self)

    def star(self):
        """
        Star this post
        """
        return self._api.star_post(self)


    def unstar(self):
        """
        Remove star of this post
        """
        return self._api.unstar_post(self)


class Message(APIModel):
    """
    The Message Model
    """
    @classmethod
    def from_response_data(cls, data, api=None):
        message = super(Message, cls).from_response_data(data, api)
        message.id = int(message.id)
        if 'user' in message:
            message.user = User.from_response_data(message.user, api)
        else:
            message.user = None

        message.created_at = parse(message.created_at)

        return message


class Interaction(APIModel):
    """
    The Interaction Model
    """
    @classmethod
    def from_response_data(cls, data, api=None):
        interaction = super(Interaction, cls).from_response_data(data, api)

        api_model = User if interaction.action == 'follow' else Post

        interaction.objects = map(lambda x: api_model.from_response_data(x, api), interaction.objects)
        interaction.users = map(lambda x: User.from_response_data(x, api), interaction.users)

        interaction.event_date = parse(interaction.event_date)
        return interaction


class Channel(APIModel):
    """
    The Channel Model
    """
    @classmethod
    def from_response_data(cls, data, api=None):
        channel = super(Channel, cls).from_response_data(data, api)
        channel.owner = User.from_response_data(channel.owner, api)
        return channel


class App(APIModel):
    """
    The App Model
    """
    @classmethod
    def from_response_data(cls, data, api=None):
        app = super(App, cls).from_response_data(data, api)
        app.owner = User.from_response_data(app.owner, api)
        app.added_on = parse(app.added_on)
        if app.get('recommended_by'):
            app.recommended_by = [User.from_response_data(x, api) for x in app.recommended_by]

        return app


class File(APIModel):
    """
    The File Model
    """
    @classmethod
    def from_response_data(cls, data, api=None):
        file_ = super(File, cls).from_response_data(data, api)
        if file_.get('user'):
            file_.user = User.from_response_data(file_.user)

        return file_


class Token(APIModel):
    """
    The Token Model
    """
    @classmethod
    def from_response_data(cls, data, api=None):
        token = super(Token, cls).from_response_data(data, api)
        if token.get('user'):
            token.user = User.from_response_data(token.user)

        return token


class Place(APIModel):
    """
    The Place Model
    """
    @classmethod
    def from_response_data(cls, data, api=None):
        place = super(Place, cls).from_response_data(data, api)

        return place

    @property
    def id(self):
        return self.factual_id


class ExploreStream(APIModel):
    """
    The Explore Stream Model
    """
    @classmethod
    def from_response_data(cls, data, api=None):
        explore_stream = super(ExploreStream, cls).from_response_data(data, api)

        return explore_stream

    @property
    def id(self):
        return self.slug
