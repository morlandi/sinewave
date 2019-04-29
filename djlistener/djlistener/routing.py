from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from . import consumers


application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/sinewave/", consumers.SinewaveSyncConsumer),
    ]),
})
