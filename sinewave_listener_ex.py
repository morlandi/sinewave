import redis
import channels.layers
from asgiref.sync import async_to_sync
from django.conf import settings

CHANNELS_DEVICE_BROADCAST_GROUP = 'ggg'


def main():
    r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

    pubsub = r.pubsub()
    pubsub.subscribe('sinewave')

    for item in pubsub.listen():
        if item['type'] == 'message':
            print(item['data'])
            broadcast_message(item['data'])


def broadcast_message(data):

    # Example:
    # > publish acqvel_broadcast '{"device_channel": "process", "device_type": "devicetest_event", "event": "start", "step": 1, "progress": 10}'

    #self.logger.log(logging.INFO, 'Broadcast process message: %s' % json.dumps(data))

    # Broadcast process message to subscribers
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        CHANNELS_DEVICE_BROADCAST_GROUP, {
            "type": 'process_notification',
            "content": data,
        })


# https://medium.com/@johngrant/django-channels-talking-to-channels-from-my-non-django-application-7dec7ceb80a8

# https://hk.saowen.com/a/5572efaa13a5fd39bb5d1d030f89df9e943e32a30e7559ad4ee6f69ddc4c87aa

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [('localhost', 6379)],
        },
    },
}


if __name__ == "__main__":

    if not settings.configured:
        settings.configure({
            'CHANNEL_LAYERS': CHANNEL_LAYERS,
        }, DEBUG=True)

    main()
