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

REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')


def connect():
    while True:
        print('Trying to connect to redis at "%s" ...' % REDIS_URL)
        try:
            connection = redis.StrictRedis.from_url(REDIS_URL)
            connection.ping()
        except (redis.exceptions.ConnectionError, redis.exceptions.ResponseError):
            time.sleep(1)
        else:
            break
    print('Connected to redis.')
    return connection


def loop(dt):
    n = 0
    connection = connect()
    while True:

        try:
            value = 30 + int(30 * math.sin(n / 4))
            row = 'X' * value
            print('\x1b[1;36;40m' + row + '\x1b[0m')

            connection.publish('sinewave', row)

            n += 1

        except (redis.exceptions.ConnectionError, redis.exceptions.ResponseError):
            print('Lost connections to redis.')
            connection = connect()
        except Exception as e:
            print(str(e))
            time.sleep(1)
        finally:
            time.sleep(dt)


def main():
    signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
    parser = argparse.ArgumentParser(
        description='Publish a sinewave on redis "sinewave" channel'
    )
    parser.add_argument('--sleep_time', '-s', type=int, default=50, help="expressed in [ms]; default = 10")
    args = parser.parse_args()
    loop(float(args.sleep_time) / 1000.0)


if __name__ == "__main__":
    main()
