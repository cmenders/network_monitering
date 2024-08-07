from django.shortcuts import render
from rest_framework import viewsets
from .models import CapturedPacket, Alert
from .serializers import CapturedPacketSerializer, AlertSerializer
from django.http import JsonResponse
from django.core.management import call_command
import threading

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
        capture_thread.do_run = False  # Example: Set a flag to stop the thread
        capture_thread.join()
    return JsonResponse({'status': 'capture stopped'})
    
class CapturedPacketViewSet(viewsets.ModelViewSet):
    queryset = CapturedPacket.objects.all()
    serializer_class = CapturedPacketSerializer

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer