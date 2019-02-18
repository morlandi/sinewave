#!/usr/bin/env python3
import argparse
import os
import redis
import signal
import sys
import time


def receive(connection, channel):

    pubsub = connection.pubsub()
    pubsub.subscribe(channel)

    for item in pubsub.listen():
        if item['type'] == 'message':
            print(item['data'])


def connect(redis_url):
    while True:
        print('Trying to connect to redis at "%s" ...' % redis_url)
        try:
            connection = redis.StrictRedis.from_url(redis_url, decode_responses=True)
            connection.ping()
        except (redis.exceptions.ConnectionError, redis.exceptions.ResponseError) as e:
            print(str(e))
            time.sleep(1)
        else:
            break
    print('Connected to redis at "%s".' % redis_url)
    return connection


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description='Receive whatever is published on specified redis channel')
    parser.add_argument('-r', '--redis-url', help='Example: "redis://[:password@]127.0.0.1:6379/0"')
    parser.add_argument('-c', '--channel', default='sinewave')
    args = parser.parse_args()

    # Retrieve redis_url for connection
    if args.redis_url:
        redis_url = args.redis_url
    else:
        redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    print('Listening to "%s" ...' % redis_url)

    # Listen for any message from specified channel§
    while True:
        try:
            connection = connect(redis_url)
            receive(connection, args.channel)
        except (redis.exceptions.ConnectionError, redis.exceptions.ResponseError):
            print('Lost connections to redis.')
        except Exception as e:
            print(str(e))
            time.sleep(1)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda signum, frame: sys.exit(0))
    main()
