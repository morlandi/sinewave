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
