# monitor/consumers.py
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class PacketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("WebSocket connected")
        await self.channel_layer.group_add('packets', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected: {close_code}")
        await self.channel_layer.group_discard('packets', self.channel_name)

    async def receive(self, text_data):
        logger.info(f"WebSocket received data: {text_data}")

    async def send_packet(self, event):
        packet = event['packet']
        logger.info(f"Sending packet: {packet}")  # Log sent packet
        await self.send(text_data=json.dumps({
            'type': 'packet',
            'packet': packet
        }))

    async def send_alert(self, event):
        alert = event['alert']
        logger.info(f"Sending alert: {alert}")  # Log sent alert
        await self.send(text_data=json.dumps({
            'type': 'alert',
            'alert': alert
        }))
