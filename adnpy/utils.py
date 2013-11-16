import json
import requests

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


def get_app_access_token(client_id, client_secret, host='account.app.net', verify_ssl=True):
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
    }

    resp = requests.post('https://%s/oauth/access_token' % host, data=data)
    resp.raise_for_status()

    return resp.json().get('access_token'), resp.json().get('token')
