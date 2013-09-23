import json

from adnpy.models import APIModel

def json_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, APIModel):
        return obj.serialize()

    return obj

def json_encoder(data):
    if isinstance(data, APIModel):
        data = data.serialize()

    return json.dumps(data, default=json_handler)