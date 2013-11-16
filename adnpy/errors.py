
class AdnError(Exception):
    pass


class AdnAPIException(AdnError):
    def __init__(self, api_response):
        super(AdnAPIException, self).__init__(api_response.meta.error_message)
        self.response = api_response
        self.error_id = api_response.meta.get('error_id')
        self.error_slug = api_response.meta.get('error_slug')

    def __str__(self):
        return "%s error_id: %s error_slug: %s" % (super(AdnAPIException, self).__str__(), self.error_id, self.error_slug)


class AdnAuthAPIException(AdnAPIException):
    pass


class AdnRateLimitAPIException(AdnAPIException):
    pass


class AdnInsufficientStorageException(AdnAPIException):
    pass


class AdnPermissionDenied(AdnAPIException):
    pass


class AdnMissing(AdnAPIException):
    pass
