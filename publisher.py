#!/usr/bin/env python3
import math
import redis
import signal
import sys
import time


def main():

    redis_url = 'redis://localhost:6379/0'
    channel = 'sinewave'

    connection = redis.StrictRedis.from_url(redis_url)
    n = 1
    while True:

        value = 30 + int(30 * math.sin(n / 4))
        row = 'P' * value
        print('\x1b[1;36;40m' + row + '\x1b[0m')

        connection.publish(channel, row)

        n += 1
        time.sleep(0.1)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda signum, frame: sys.exit(0))
    main()
