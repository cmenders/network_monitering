from django.shortcuts import render
from rest_framework import viewsets
from .models import CapturedPacket, Alert
# from .serializers import CapturedPacketSerializer, AlertSerializer
from django.http import JsonResponse
from django.core.management import call_command
import threading
import socket

capture_thread = None

def start_capture(request):
    global capture_thread
    if not capture_thread or not capture_thread.is_alive():
        capture_thread = threading.Thread(target=call_command, args=('capture_packets',))
        capture_thread.start()
    return JsonResponse({'status': 'capture started'})

def stop_capture(request):
    global capture_thread
    if capture_thread and capture_thread.is_alive():
        capture_thread.do_run = False  # Set a flag to stop the thread
        capture_thread.join()
    return JsonResponse({'status': 'capture stopped'})

def get_packets(request):
    packets = CapturedPacket.objects.order_by('-timestamp')[:100]  # limit to the latest 100 packets
    packet_data = [{
        'timestamp': str(packet.timestamp),
        'src_ip': packet.src_ip,
        'dst_ip': packet.dst_ip,
        'protocol': packet.protocol,
        'src_port': packet.src_port,
        'dst_port': packet.dst_port,
        'details': packet.details
    } for packet in packets]
    return JsonResponse(packet_data, safe=False)

import logging

logger = logging.getLogger(__name__)

def get_alerts(request):
    logger.info('get_alerts called')
    alerts = Alert.objects.order_by('-timestamp')[:50]  # limit to the latest 100 alerts
    alert_data = [{
        'message': alert.message,
        'count': alert.count,
        'timestamp': str(alert.timestamp)
    } for alert in alerts]
    return JsonResponse(alert_data, safe=False)

def get_hostname_counts(request):
    logger.info('get_hostname_counts called')
    packets = CapturedPacket.objects.all()
    hostname_counts = {}
    for packet in packets:
        try:
            hostname = socket.gethostbyaddr(packet.dst_ip)[0]
        except socket.herror:
            hostname = packet.dst_ip

        if hostname in hostname_counts:
            hostname_counts[hostname]['count'] += 1
            hostname_counts[hostname]['latest_timestamp'] = packet.timestamp
        else:
            hostname_counts[hostname] = {
                'hostname': hostname,
                'count': 1,
                'latest_timestamp': packet.timestamp
            }

    sorted_hostname_counts = sorted(hostname_counts.values(), key=lambda x: x['latest_timestamp'], reverse=True)

    hostname_data = [{
        'hostname': entry['hostname'],
        'count': entry['count'],
        'latest_timestamp': str(entry['latest_timestamp'])
    } for entry in sorted_hostname_counts]

    return JsonResponse(hostname_data, safe=False)

# def get_alerts(request):
#     alerts = Alert.objects.order_by('-timestamp')[:100]  # limit to the latest 100 alerts
#     alert_data = [{
#         'message': alert.message,
#         'count': alert.count,
#         'timestamp': str(alert.timestamp)
#     } for alert in alerts]
#     return JsonResponse(alert_data, safe=False)

# def get_hostname_counts(request):
#     packets = CapturedPacket.objects.all()
#     hostname_counts = {}
#     for packet in packets:
#         try:
#             hostname = socket.gethostbyaddr(packet.dst_ip)[0]
#         except socket.herror:
#             hostname = packet.dst_ip

#         if hostname in hostname_counts:
#             hostname_counts[hostname]['count'] += 1
#             hostname_counts[hostname]['latest_timestamp'] = packet.timestamp
#         else:
#             hostname_counts[hostname] = {
#                 'hostname': hostname,
#                 'count': 1,
#                 'latest_timestamp': packet.timestamp
#             }

#     sorted_hostname_counts = sorted(hostname_counts.values(), key=lambda x: x['latest_timestamp'], reverse=True)

#     hostname_data = [{
#         'hostname': entry['hostname'],
#         'count': entry['count'],
#         'latest_timestamp': str(entry['latest_timestamp'])
#     } for entry in sorted_hostname_counts]

#     return JsonResponse(hostname_data, safe=False)

# class CapturedPacketViewSet(viewsets.ModelViewSet):
#     queryset = CapturedPacket.objects.all()
#     serializer_class = CapturedPacketSerializer

# class AlertViewSet(viewsets.ModelViewSet):
#     queryset = Alert.objects.all()
#     serializer_class = AlertSerializer
