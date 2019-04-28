from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from .consumers import SinewaveSyncConsumer
from .consumers import SinewaveAsyncConsumer


application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    "websocket": AllowedHostsOriginValidator(
        URLRouter([
            path("ws/sinewave/", SinewaveSyncConsumer),
        ]),
    ),
})
