import json

from adnpy.models import Model

def json_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, Model):
        return obj.serialize()

    return obj

def json_encoder(data):
    if isinstance(data, Model):
        data = data.serialize()

    return json.dumps(data, default=json_handler)