#!/usr/bin/env python3
import math
import os
import redis
import signal
import sys
import time


REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')


def main():

    connection = redis.StrictRedis.from_url(REDIS_URL)
    n = 1
    while True:

        value = 30 + int(30 * math.sin(n / 4))
        row = 'X' * value
        print('\x1b[1;36;40m' + row + '\x1b[0m')

        connection.publish('sinewave', row)

        n += 1
        time.sleep(0.05)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda signum, frame: sys.exit(0))
    main()
