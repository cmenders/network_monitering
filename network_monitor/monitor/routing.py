from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/packets/', consumers.PacketConsumer.as_asgi()),
]
