#!/usr/bin/env python3
import argparse
import math
import os
import redis
import signal
import sys
import time

#
#    NOTE FOR REDIS CONNECTION
#    If redis connection requires a password, proceed as follows:
#
#    1) edit `/etc/environment` to add "REDIS_URL=redis://:<password>@127.0.0.1:6379/0"
#    2) if this script is execute via supervisor, instruct it to load `/etc/environment`;
#       for example (with systemd):
#
#        $ systemctl edit --full supervisor.service
#            [Service]
#            EnvironmentFile=/etc/environment
#


def connect(redis_url):
    while True:
        print('Trying to connect to redis at "%s" ...' % redis_url)
        try:
            connection = redis.StrictRedis.from_url(redis_url)
            connection.ping()
        except (redis.exceptions.ConnectionError, redis.exceptions.ResponseError):
            time.sleep(1)
        else:
            break
    print('Connected to redis at "%s".' % redis_url)
    return connection


def loop(dt, redis_url, channel):
    n = 0
    connection = connect(redis_url)
    while True:

        try:
            value = 30 + int(30 * math.sin(n / 4))
            row = 'X' * value
            print('\x1b[1;36;40m' + row + '\x1b[0m')

            connection.publish(channel, row)

            n += 1

        except (redis.exceptions.ConnectionError, redis.exceptions.ResponseError):
            print('Lost connections to redis.')
            connection = connect(redis_url)
        except Exception as e:
            print(str(e))
            time.sleep(1)
        finally:
            time.sleep(dt)


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description='Publish a sinewave on specified redis channel')
    parser.add_argument('-r', '--redis-url', help='Example: "redis://[:password@]127.0.0.1:6379/0"')
    parser.add_argument('-c', '--channel', default='sinewave')
    parser.add_argument('-s', '--sleep_time', type=int, default=100, help="expressed in [ms]; default = 10")
    args = parser.parse_args()

    # Retrieve redis_url for connection
    if args.redis_url:
        redis_url = args.redis_url
    else:
        redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

    loop(float(args.sleep_time) / 1000.0, redis_url, args.channel)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda signum, frame: sys.exit(0))
    main()
