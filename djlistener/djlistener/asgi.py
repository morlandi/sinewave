"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

# import os
# import django
# from channels.routing import get_default_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djlistener.settings")
# django.setup()
# application = get_default_application()

import os

from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from . import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djlistener.settings')

application = ProtocolTypeRouter({

    "http": get_asgi_application(),

    "websocket": URLRouter([
        path("ws/sinewave/", consumers.SinewaveSyncConsumer.as_asgi()),
    ]),
})

