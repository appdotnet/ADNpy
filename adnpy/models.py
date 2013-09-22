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


class Model(dict):
    def __setattr__(self, name, val):
        return self.__setitem__(name, val)

    def __getattr__(self, name):
        try:
            return self.__getitem__(name)
        except KeyError:
            raise AttributeError(name)

    def __init__(self, data=None, api=None):
        super(Model, self).__init__()
        self['_api'] = api
        if not data:
            return

        for k, v in data.iteritems():
            if isinstance(v, collections.Mapping):
                self[k] = Model(v, api)
            elif v and is_seq_not_string(v) and isinstance(v[0], collections.Mapping):
                self[k] = [Model(i, api) for i in v]
            else:
                self[k] = v

    @classmethod
    def from_string(cls, raw_json, api=None):
        return cls(json.loads(raw_json), api)

    def serialize(self):
        data = {}
        for k, v in self.iteritems():
            if k.startswith('_'):
              continue

            if isinstance(v, Model):
              data[k] = v.serialize()
            elif v and is_seq_not_string(v) and isinstance(v[0], Model):
              data[k] = [x.serialize() for x in v]
            else:
              data[k] = v

        return data

    def __getstate__(self):
        return self.serialize()


class APIModel(Model):
    @classmethod
    def from_response_data(cls, data, api=None):
        model = cls(data, api)
        return model


class User(APIModel):
    @classmethod
    def from_response_data(cls, data, api=None):
        user = super(User, cls).from_response_data(data, api)
        user.id = int(user.id)
        user.created_at = parse(user.created_at)

        return user


class Post(APIModel):
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
        return self._api.delete_post(self)


class Message(APIModel):
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
    @classmethod
    def from_response_data(cls, data, api=None):
        interaction = super(Interaction, cls).from_response_data(data, api)

        api_model = User if interaction.action == 'follow' else Post

        interaction.objects = map(lambda x: api_model.from_response_data(x, api), interaction.objects)
        interaction.users = map(lambda x: User.from_response_data(x, api), interaction.users)

        interaction.event_date = parse(interaction.event_date)
        return interaction


class Channel(APIModel):
    @classmethod
    def from_response_data(cls, data, api=None):
        channel = super(Channel, cls).from_response_data(data, api)
        channel.owner = User.from_response_data(channel.owner, api)
        return channel


class App(APIModel):
    @classmethod
    def from_response_data(cls, data, api=None):
        app = super(App, cls).from_response_data(data, api)
        app.owner = User.from_response_data(app.owner, api)
        app.added_on = parse(app.added_on)
        if app.get('recommended_by'):
            app.recommended_by = [User.from_response_data(x, api) for x in app.recommended_by]

        return app
