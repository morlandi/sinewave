#!/usr/bin/env python3
import redis
import signal
import time
import sys


def main():

    redis_url = 'redis://localhost:6379/0'
    channel = 'sinewave'

    connection = redis.StrictRedis.from_url(redis_url, decode_responses=True)

    pubsub = connection.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(channel)

    # get_message() uses the system's 'select' module to quickly poll the connection's socket.
    # If there's data available to be read, get_message() will read it,
    # format the message and return it or pass it to a message handler.
    # If there's no data to be read, get_message() will immediately return None.

    while True:
        message = pubsub.get_message()
        if message is not None:
            print(message['data'])
        time.sleep(0.001)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda signum, frame: sys.exit(0))
    main()
