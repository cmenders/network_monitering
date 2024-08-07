import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class PacketConsumer(AsyncWebsocketConsumer):
    alerts = {}
    hostname_counts = {}

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
        hostname = packet['hostname']

        if hostname in self.hostname_counts:
            self.hostname_counts[hostname]['count'] += 1
            self.hostname_counts[hostname]['latest_timestamp'] = packet['timestamp']
        else:
            self.hostname_counts[hostname] = {
                'hostname': hostname,
                'count': 1,
                'latest_timestamp': packet['timestamp']
            }

        sorted_hostname_counts = sorted(self.hostname_counts.values(), key=lambda x: x['latest_timestamp'], reverse=True)

        await self.send(text_data=json.dumps({
            'type': 'hostname_counts',
            'hostname_counts': sorted_hostname_counts
        }))
        logger.info(f"Sent hostname counts: {sorted_hostname_counts}")

    async def send_alert(self, event):
        src_ip = event['alert']['src_ip']
        dst_ip = event['alert']['dst_ip']
        alert_key = f"{src_ip} -> {dst_ip}"

        if alert_key in self.alerts:
            self.alerts[alert_key]['count'] += 1
            self.alerts[alert_key]['timestamp'] = event['alert']['timestamp']
        else:
            self.alerts[alert_key] = {
                'message': f"SYN packet detected: {src_ip} -> {dst_ip}",
                'count': 1,
                'timestamp': event['alert']['timestamp']
            }

        sorted_alerts = sorted(self.alerts.values(), key=lambda x: x['timestamp'], reverse=True)

        await self.send(text_data=json.dumps({
            'type': 'alerts',
            'alerts': sorted_alerts
        }))
        logger.info(f"Sent alerts: {sorted_alerts}")