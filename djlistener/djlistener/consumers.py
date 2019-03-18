import asyncio
import json
import datetime
import random
import math
import time
from django.conf import settings
from channels.consumer import AsyncConsumer
from channels.consumer import SyncConsumer
from .utils import trace


class SinewaveAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        trace('websocket_connect()', event)

        # Join monitoring group
        await self.channel_layer.group_add(
            settings.SINEWAVE_CHANNEL_NAME,
            self.channel_name
        )

        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        trace('websocket_receive()', event)

    async def websocket_disconnect(self, event):
        trace('websocket_disconnect()', event)

        # Leave monitoring group
        await self.channel_layer.group_discard(
            settings.SINEWAVE_CHANNEL_NAME,
            self.channel_name
        )

    # async def data_received(self, event):
    #     trace('data_received()', event)
    #     await self.send({
    #         'type': 'websocket.send',
    #         'text': json.dumps({
    #             'timestamp': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
    #             'values': [
    #                 len(event['content']),
    #             ]
    #         })
    #     })

    async def data_received(self, event):
        trace('data_received()', event)

        try:
            data = json.loads(event['content'])
            data['timestamp'] = datetime.datetime.utcfromtimestamp(data['timestamp']).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        except json.decoder.JSONDecodeError as e:
            data = {
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'values': [
                    len(event['content']),
                ]
            }

        await self.send({
            'type': 'websocket.send',
            'text': json.dumps(data),
        })


class SinewaveSyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        trace('websocket_connect()', event)
        self.send({
            'type': 'websocket.accept'
        })
        self.send({
            'type': 'websocket.send',
            'text': json.dumps('hello world')
        })

    def websocket_receive(self, event):
        trace('websocket_receive()', event)

    def websocket_disconnect(self, event):
        trace('websocket_disconnect()', event)

    def data_received(self, event):
        trace('websocket_connect()', event)
