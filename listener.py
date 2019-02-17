#!/usr/bin/env python3
import redis
import signal
import sys


def receive(connection, channel):

    pubsub = connection.pubsub()
    pubsub.subscribe(channel)

    for item in pubsub.listen():
        if item['type'] == 'message':
            print(item['data'])


def main():
    redis_url = 'redis://localhost:6379/0'
    print('Listening to "%s" ...' % redis_url)
    connection = redis.StrictRedis.from_url(redis_url, decode_responses=True)
    receive(connection, "sinewave")


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda signum, frame: sys.exit(0))
    main()
