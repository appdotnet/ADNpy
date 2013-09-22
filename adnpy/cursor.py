import logging
import time

from adnpy.errors import AdnRateLimitAPIException

logger = logging.getLogger(__name__)


def get_data(func, args, kwargs, sleep=None):
    try:
        data, meta = func(*args, **kwargs)
    except AdnRateLimitAPIException:
        if sleep:
            sleep = sleep * 2
        else:
            sleep = 10

        logger.debug('Hit ratelimit sleeping: %s seconds', sleep)
        time.sleep(sleep)
        return get_data(func, kwargs, sleep)

    return data, meta


def cursor(func, *args, **kwargs):

    paginate_on = kwargs.pop('paginate_on', 'min_id')
    paginate_param = kwargs.pop('paginate_param', 'before_id')
    kwargs['count'] = kwargs.pop('count', 200) 
    more = True

    while more:
        data, meta = get_data(func, args, kwargs)
        more = meta.more
        kwargs[paginate_param] = meta.get(paginate_on)
        for obj in data:
            yield obj
