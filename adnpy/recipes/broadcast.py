import os
import mimetypes

from adnpy import api as default_api


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
    """Builder class for sending messages using App.net Broadcast.

    Create, set attributes, call :meth:`send()`.

    :param api: API client to use. Most of the time, this will be `None`, meaning the
        default client, i.e., `adnpy.api`, will be used.

    """

    channel_id = None
    """App.net Channel ID for the channel where this broadcast will be sent. (Required.)"""

    headline = None
    """Broadcast headline. (Required.)"""

    text = None
    """Body text of broadcast. (Optional.)"""

    parse_markdown_links = False
    """Set when the App.net API should use Markdown syntax to extract links from :attr:`text`."""

    parse_links = False
    """Set when the App.net API should linkify URLs from :attr:`text`."""

    read_more_link = None
    """Link to original source of content, if desired.

    :note: Must be valid a ``http://`` or ``https://`` URL.

    """

    photo = None
    """:class:`~file`-like object or string containing path to image to be rendered as photo for this broadcast.

    Will be uploaded to App.net.

    """

    attachment = None
    """:class:`~file`-like object or string containing path to attachment to be sent for this broadcast.

    Will be uploaded to App.net.

    """

    def __init__(self, api=None):
        self.api = api or default_api

    def send(self):
        """Sends the broadcast message.

        :returns: tuple of (:class:`adnpy.models.Message`, :class:`adnpy.models.APIMeta`)

        """
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
