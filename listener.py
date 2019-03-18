#!/usr/bin/env python3
import redis
import signal
import time
import sys


def main():

    redis_url = 'redis://localhost:6379/0'
    channel = 'sinewave'

    connection = redis.StrictRedis.from_url(redis_url, decode_responses=True)

    pubsub = connection.pubsub(ignore_subscribe_messages=False)
    pubsub.subscribe(channel)

    # >>> pubsub.subscribe('my-first-channel', 'my-second-channel', ...)
    # >>> pubsub.psubscribe('my-*', ...)

    # listen() is a generator that blocks until a message is available.
    # Use it if your application doesn't need to do anything else but receive
    # and act on messages received from redis

    for message in pubsub.listen():
        print(message)

    # for message in pubsub.listen():
    #     if message['type'] == 'message':
    #         print(message['data'])

    # # or pass ignore_subscribe_messages=True to connection.pubsub()
    # for message in pubsub.listen():
    #     print(message['data'])


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda signum, frame: sys.exit(0))
    main()
