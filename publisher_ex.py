#!/usr/bin/env python3
import argparse
import math
import os
import redis
import signal
import sys
import time
import json

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


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description='Publish a sinewave on specified redis channel')
    parser.add_argument('-r', '--redis-url', help='Example: "redis://[:password@]127.0.0.1:6379/0"')
    parser.add_argument('-c', '--channel', default='sinewave')
    parser.add_argument('-s', '--sleep_time', type=int, default=100, help="expressed in [ms]; default = 100")
    parser.add_argument('-j', '--json', action='store_true', default=False, help="Send rich data (value + timestamp)")
    args = parser.parse_args()

    # Retrieve redis_url and channel for connection
    redis_url = args.redis_url if args.redis_url else os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    channel = args.channel
    dt = float(args.sleep_time) / 1000.0

    n = 0
    connection = connect(redis_url)
    while True:

        try:
            value = 30 + int(30 * math.sin(n / 4))

            if not args.json:
                # Examples: 'XXXXXXXX'
                data = 'X' * value
            else:
                # Example: '{"timestamp": 1554441334.941386, "values": [55, 38, 3]}'
                data = json.dumps({
                    'timestamp': time.time(),
                    'values': [
                        value,
                        20 + int(20 * math.sin(n / 2)),
                        10 + int(10 * math.sin(n / 1)),
                    ],
                })
            connection.publish(channel, data)
            print('\x1b[1;36;40m' + data + '\x1b[0m')

            n += 1

        except (redis.exceptions.ConnectionError, redis.exceptions.ResponseError):
            print('Lost connections to redis.')
            connection = connect(redis_url)
        except Exception as e:
            print(str(e))
            time.sleep(1)
        finally:
            time.sleep(dt)


def connect(redis_url):
    while True:
        print('Trying to connect to redis at "%s" ...' % redis_url)
        try:
            connection = redis.StrictRedis.from_url(redis_url, decode_responses=True)
            connection.ping()
        except (redis.exceptions.ConnectionError, redis.exceptions.ResponseError):
            time.sleep(1)
        else:
            break
    print('Connected to redis at "%s".' % redis_url)
    return connection


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda signum, frame: sys.exit(0))
    main()
