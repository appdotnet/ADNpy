
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