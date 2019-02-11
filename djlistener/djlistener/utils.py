import redis
from django.conf import settings

REDIS_CONNECTION_POOL = redis.ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)


def get_redis_connection():
    """
    Get or create a Redis connection from the pool.
    """

    # TODO: possibile alternativa (untested):
    #    connection = StrictRedis(**settings.WS4REDIS_CONNECTION)
    # See: https://github.com/jrief/django-websocket-redis/pull/213

    # rdb = redis.StrictRedis(connection_pool=REDIS_CONNECTION_POOL, decode_responses=True, charset="utf-8")
    # return rdb

    return redis.Redis(connection_pool=REDIS_CONNECTION_POOL)


def trace(*args):
    colorize = True
    text = ''
    if colorize:
        text += '\x1b[1;33;40m'
    text += ', '.join([str(arg) for arg in args])
    if colorize:
        text += '\x1b[0m'
    print(text)

