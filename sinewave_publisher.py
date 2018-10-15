import math, time
import redis
import argparse
import logging


def publish(sleep_time):

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    dt = float(sleep_time) / 1000.0

    for n in range(0, 100000):
        row = (62 * 'X')[0:32 + int(30 * math.sin(n / 8))]
        r.publish('sinewave', row)
        #print(row)
        print('\x1b[1;36;40m' + row + '\x1b[0m')
        #time.sleep(0.01)
        time.sleep(dt)


def main():

    parser = argparse.ArgumentParser(
        description='Publish a sinewave on redis "sinewave" channel'
    )
    parser.add_argument('--sleep_time', '-s', type=int, default=10, help="expressed in [ms]; default = 10")
    args = parser.parse_args()

    while True:
        publish(args.sleep_time)


if __name__ == "__main__":
    main()
