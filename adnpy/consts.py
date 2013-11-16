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


CHANNEL_PARAMS = [
    'channel_types',
    'include_marker',
    'include_read',
    'include_recent_message',
    'include_annotations',
    'include_user_annotations',
    'include_message_annotations',
]


MESSAGE_PARAMS = [
    'include_muted',
    'include_deleted',
    'include_machine',
    'include_annotations',
    'include_message_annotations',
    'include_user_annotations',
    'include_html',
]


FILE_PARAMS = [
    'file_types',
    'include_incomplete',
    'include_private',
    'include_annotations',
    'include_file_annotations',
    'include_user_annotations',
]


PLACE_SEARCH_PARAMS = [
    'latitude',
    'longitude',
    'q',
    'radius',
    'count',
    'remove_closed',
    'altitude',
    'horizontal_accuracy',
    'vertical_accuracy',
]

APP_STREAM_PARAMS = [
    'key',
]