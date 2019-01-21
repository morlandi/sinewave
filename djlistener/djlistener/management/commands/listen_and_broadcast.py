import signal
import sys
import traceback
import time
import logging
import json
import channels.layers
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from redis.exceptions import ConnectionError
from django.core.management.base import BaseCommand
from django.conf import settings
from djlistener.utils import get_redis_connection


logger = logging.getLogger(__name__)


def signal_handler(signal, frame):
    sys.exit(0)


class Command(BaseCommand):
    help = 'Listen to incoming sinewaves, and broadcast to websocket clients'

    def add_arguments(self, parser):
        parser.add_argument("channel", help='pubsub channel to submit (example: "acqvel_broadcast")')

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        signal.signal(signal.SIGINT, signal_handler)
        self.logger = logger or logging.getLogger(__name__)

    def set_logger(self, verbosity):
        """
        Set logger level based on verbosity option
        """
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(module)s| %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if verbosity == 0:
            self.logger.setLevel(logging.WARN)
        elif verbosity == 1:  # default
            self.logger.setLevel(logging.INFO)
        elif verbosity > 1:
            self.logger.setLevel(logging.DEBUG)

        # verbosity 3: also enable all logging statements that reach the root logger
        if verbosity > 2:
            logging.getLogger().setLevel(logging.DEBUG)

    def handle(self, *args, **options):
        self.set_logger(options.get('verbosity'))
        self.channel = options.get('channel')
        self.logger.info('Initializing redis listener...[subscribing channel: "%s"]' % self.channel)
        self.redis = None
        self.pubsub = None
        self.loop()

    def connect(self):
        while True:
            self.logger.debug('Trying to connect to redis ...')
            try:
                self.redis = get_redis_connection()
                self.redis.ping()
            except (ConnectionError, ConnectionRefusedError):
                time.sleep(1)
            else:
                break
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(self.channel)
        self.logger.info('Connected to redis.')

    def loop(self):
        self.connect()
        while True:
            try:
                for item in self.pubsub.listen():
                    if item['type'] == 'message':
                        self.logger.debug(item)
                        #data = json.loads(item['data'].decode('utf-8'))
                        #data = json.loads(item['data'])
                        data = item['data']
                        self.broadcast_message(data)
            except ConnectionError:
                self.logger.error('Lost connections to redis.')
                self.connect()
            except Exception as e:
                self.logger.error(str(e))
                self.logger.debug(traceback.format_exc())

    def broadcast_message(self, data):
        return

        # device_channel = data.pop('device_channel')
        # device_type = data.pop('device_type')

        # if device_channel == 'process':

        #     # Example:
        #     # > publish acqvel_broadcast '{"device_channel": "process", "device_type": "devicetest_event", "event": "start", "step": 1, "progress": 10}'

        #     self.logger.log(logging.INFO, 'Broadcast process message: %s' % json.dumps(data))

        #     # Broadcast process message to subscribers
        #     channel_layer = channels.layers.get_channel_layer()
        #     async_to_sync(channel_layer.group_send)(
        #         settings.CHANNELS_DEVICE_BROADCAST_GROUP, {
        #             "type": 'process_notification',
        #             "device_channel": device_channel,
        #             "device_type": device_type,
        #             "content": data,
        #         })

        # else:
        #     level = logging.INFO if (data['id'] > 0) else logging.DEBUG
        #     self.logger.log(level, 'Broadcast device message: device_channel="%s", timestamp=%d, id=%d, command="%s", status_code=%d' % (
        #         device_channel,
        #         data['timestamp'],
        #         data['id'],
        #         data['command'],
        #         data['status_code'],
        #     ))

        #     # # Save device status snapshot
        #     # if data['id'] == 0 and data['command'] == 'status' and data['status_code'] == 0:
        #     #     key = 'device:%s:status' % device_channel
        #     #     self.redis.set(key, json.dumps(data))

        #     # Broadcast device message to subscribers
        #     channel_layer = channels.layers.get_channel_layer()
        #     async_to_sync(channel_layer.group_send)(
        #         settings.CHANNELS_DEVICE_BROADCAST_GROUP, {
        #             "type": 'device_reply',
        #             "device_channel": device_channel,
        #             "device_type": device_type,
        #             "content": data,
        #         })
