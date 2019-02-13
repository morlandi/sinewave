import math
import time
import redis
import os

REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')


def main():

    connection = redis.StrictRedis.from_url(REDIS_URL)
    n = 1
    while True:

        row = (62 * 'X')[0:32 + int(30 * math.sin(n / 8))]
        print('\x1b[1;36;40m' + row + '\x1b[0m')

        connection.publish('sinewave', row)

        n += 1
        time.sleep(0.05)

if __name__ == "__main__":
    main()
