#!/usr/bin/env python3
import math
import os
#import redis
import socket
import signal
import sys
import time


#REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
HOST = "127.0.0.1"
PORT = 6379
CHANNEL = 'sinewave'


# Redis Protocol specification
# ----------------------------

# https://redis.io/topics/protocol

#
# Run this:
#
# redis-cli -p 7777 PUBLISH sinewave XXXXXXXX
#
# while:
#
# nc -l 7777 (or # nc -l -p 7777 ???)
#
# Result:
#
# *3
# $7
# PUBLISH
# $8
# sinewave
# $8
# XXXXXXXX


#
# References:
#
# - `Quick, write me a Redis client <https://medium.com/concerning-pharo/quick-write-me-a-redis-client-5fbe4ddfb13d>`_
# - `An Arduino library for Redis that works on ESP8266 <https://www.arduinolibraries.info/libraries/redis-for-esp8266>`_
#


def main():

    #connection = redis.StrictRedis.from_url(REDIS_URL)
    s = socket.socket()
    s.connect((HOST, PORT))

    n = 1
    while True:

        value = 30 + int(30 * math.sin(n / 4))
        row = 'R' * value
        print('\x1b[1;36;40m' + row + '\x1b[0m')

        #connection.publish('sinewave', row)

        # > PUBLISH channel message
        message = row
        #print('> publish %s %s' % (channel, message))
        command = "*3\r\n$7\r\nPUBLISH\r\n$%d\r\n%s\r\n$%d\r\n%s\r\n" % (
            len(CHANNEL),
            CHANNEL,
            len(message),
            message
        )
        #print(command)
        s.send(command.encode('utf-8'))
        response = s.recv(256)
        #print(response)

        n += 1
        time.sleep(0.1)

    s.close()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda signum, frame: sys.exit(0))
    main()
