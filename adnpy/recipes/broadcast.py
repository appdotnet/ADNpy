import os
import mimetypes


def _upload_file(api, file_or_name):
    if isinstance(file_or_name, basestring):
        file_ = file(file_or_name, 'rb')
        filename = os.path.basename(file_or_name)
    else:
        file_ = file_or_name
        filename = os.path.basename(getattr(file_, 'name', None) or 'attachment.bin')

    mimetype, _ = mimetypes.guess_type(filename)
    mimetype = mimetype or 'application/octet-stream'
    # kind = 'image' if mimetype.startswith('image/') else 'other'

    file_data = {
        'type': 'net.app.adnpy.upload',
    }

    file_files = {
        'content': (filename, file_, mimetype),
    }

    return api.create_file(data=file_data, files=file_files)



class BroadcastMessageBuilder(object):
    def __init__(self, api):
        self.api = api
        self.channel_id = None
        self.headline = None
        self.text = None
        self.parse_markdown_links = False
        self.parse_links = False
        self.read_more_link = None
        self.photo = None
        self.attachment = None

    def send(self):
        parse_links = self.parse_links or self.parse_markdown_links

        message = {
            'annotations': [],
            'entities': {
                'parse_links': parse_links,
                'parse_markdown_links': self.parse_markdown_links,
            }
        }

        if self.photo:
            photo, photo_meta = _upload_file(self.api, self.photo)
            message['annotations'].append({
                'type': 'net.app.core.oembed',
                'value': {
                    '+net.app.core.file': {
                        'file_id': photo.id,
                        'file_token': photo.file_token,
                        'format': 'oembed',
                    }
                }
            })

        if self.attachment:
            attachment, attachment_meta = _upload_file(self.api, self.attachment)
            message['annotations'].append({
                'type': 'net.app.core.attachments',
                'value': {
                    '+net.app.core.file_list': [
                        {
                            'file_id': attachment.id,
                            'file_token': attachment.file_token,
                            'format': 'metadata',
                        }
                    ]
                }
            })

        if self.text:
            message['text'] = self.text
        else:
            message['machine_only'] = True

        if self.headline:
            message['annotations'].append({
                'type': 'net.app.core.broadcast.message.metadata',
                'value': {
                    'subject': self.headline,
                },
            })

        if self.read_more_link:
            message['annotations'].append({
                'type': 'net.app.core.crosspost',
                'value': {
                    'canonical_url': self.read_more_link,
                }
            })

        return self.api.create_message(self.channel_id, data=message)
