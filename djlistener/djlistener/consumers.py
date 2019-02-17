import asyncio
import json
import datetime
import random
import math
import time
from channels.consumer import AsyncConsumer
from channels.consumer import SyncConsumer
from .utils import trace


class SinewaveAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        trace('websocket_connect()', event)

        # Join monitoring group
        await self.channel_layer.group_add(
            'sinewave',
            self.channel_name
        )

        await self.send({
            'type': 'websocket.accept'
        })

        # for n in range(1000):
        #     await self.send({
        #         'type': 'websocket.send',
        #         #'text': 'Hello world (%d)' % i,
        #         'text': json.dumps({
        #             'timestamp': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        #             'values': [
        #                 #int(30 * math.sin(n / 8)),
        #                 100 * math.sin(time.time() / 100),
        #                 #random.randint(0, 10),
        #             ]
        #         })
        #     })
        #     await asyncio.sleep(0.1)

    async def websocket_receive(self, event):
        trace('websocket_receive()', event)

    async def websocket_disconnect(self, event):
        trace('websocket_disconnect()', event)

    async def data_received(self, event):
        trace('data_received()', event)
        await self.send({
            'type': 'websocket.send',
            #'text': 'Hello world (%d)' % i,
            'text': json.dumps({
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                'values': [
                    len(event['content']),
                ]
            })
        })


class SinewaveSyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        trace('connect', event)
        self.send({
            'type': 'websocket.accept'
        })

        for n in range(1000):
            self.send({
                'type': 'websocket.send',
                #'text': 'Hello world (%d)' % i,
                'text': json.dumps({
                    'timestamp': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'values': [
                        #int(30 * math.sin(n / 8)),
                        100 * math.sin(time.time() / 100),
                        #random.randint(0, 10),
                    ]
                })
            })
            time.sleep(0.8)

    def websocket_receive(self, event):
        trace('receive', event)

    def websocket_disconnect(self, event):
        trace('disconnect', event)
