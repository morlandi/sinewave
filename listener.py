#!/usr/bin/env python3
import os
import sys
import signal
import redis
import argparse


def receive(connection):

    pubsub = connection.pubsub()
    pubsub.subscribe('sinewave')

    for item in pubsub.listen():
        if item['type'] == 'message':
            print(item['data'])


def main():
    parser = argparse.ArgumentParser(
        description='Receive whatever is published on redis "sinewave" channel'
    )
    parser.add_argument('--connection-string', '-c', type=str, default='redis://localhost:6379/0',
        help='redis connection string; example: "redis://[:password@]127.0.0.1:6379/0"')
    args = parser.parse_args()

    REDIS_URL = os.environ.get(
        'REDIS_URL',
        args.connection_string
    )
    print('Listening to "%s" ...' % REDIS_URL)

    connection = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)
    receive(connection)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda signum, frame: sys.exit(0))
    main()
