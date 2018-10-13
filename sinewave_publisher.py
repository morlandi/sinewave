import math, time
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

for n in range(0, 100000):
    row = (62 * 'X')[0:32 + int(30*math.sin(n/8.0))]
    r.publish('sinewave', row)
    #print(row)
    print('\x1b[1;36;40m' + row + '\x1b[0m')
    time.sleep(0.01)
