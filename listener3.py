#!/usr/bin/env python3
import redis
import signal
import time
import sys


def main():

    redis_url = 'redis://localhost:6379/0'
    channel = 'sinewave'

    connection = redis.StrictRedis.from_url(redis_url, decode_responses=True)

    pubsub = connection.pubsub()
    pubsub.subscribe(channel)
    #pubsub.subscribe(sinewave=on_new_message)
    #pubsub.subscribe(**{channel: on_new_message})

    # The third option runs an event loop in a separate thread.
    # pubsub.run_in_thread() creates a new thread and starts the event loop.
    # The thread object is returned to the caller of run_in_thread().

    thread = pubsub.run_in_thread(sleep_time=0.001)

    time.sleep(5)
    thread.stop()


def on_new_message(message):
    print(message['data'])


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda signum, frame: sys.exit(0))
    main()
