import time
from scapy.all import sniff, TCP, UDP, ICMP, DNS, ARP, IP
from django.core.management.base import BaseCommand
from monitor.models import CapturedPacket, Alert
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Command(BaseCommand):
    help = 'Capture network packets and store them in the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting packet capture...')
        channel_layer = get_channel_layer()

        def packet_callback(packet):
            if IP in packet:
                ip_src = packet[IP].src
                ip_dst = packet[IP].dst
                protocol = packet[IP].proto

                src_port = packet.sport if hasattr(packet, 'sport') else None
                dst_port = packet.dport if hasattr(packet, 'dport') else None
                details = str(packet.summary())

                # Save packet to database
                captured_packet = CapturedPacket.objects.create(
                    src_ip=ip_src,
                    dst_ip=ip_dst,
                    protocol=protocol,
                    src_port=src_port,
                    dst_port=dst_port,
                    details=details
                )

                # Send packet to WebSocket
                async_to_sync(channel_layer.group_send)(
                    'packets',
                    {
                        'type': 'send_packet',
                        'packet': {
                            'timestamp': str(captured_packet.timestamp),
                            'src_ip': ip_src,
                            'dst_ip': ip_dst,
                            'protocol': protocol,
                            'src_port': src_port,
                            'dst_port': dst_port,
                            'details': details
                        }
                    }
                )

                # Example alert for high volume traffic (simplified for demonstration)
                if protocol == 6 and packet[TCP].flags == 'S':
                    alert = Alert.objects.create(message=f'SYN packet detected: {ip_src} -> {ip_dst}')
                    async_to_sync(channel_layer.group_send)(
                        'packets',
                        {
                            'type': 'send_alert',
                            'alert': {
                                'timestamp': str(alert.timestamp),
                                'message': alert.message
                            }
                        }
                    )

                self.stdout.write(f'Captured packet: {ip_src} -> {ip_dst}')

        # Sniff packets
        sniff(prn=packet_callback, store=0, filter="tcp or udp or icmp or arp or port 53 or port 80 or port 443")
