from django.shortcuts import render
from rest_framework import viewsets
from .models import CapturedPacket, Alert
from .serializers import CapturedPacketSerializer, AlertSerializer
from django.http import JsonResponse
from django.core.management import call_command
import threading

def start_capture(request):
    threading.Thread(target=call_command, args=('capture_packets',)).start()
    return JsonResponse({'status': 'capture started'})
    
class CapturedPacketViewSet(viewsets.ModelViewSet):
    queryset = CapturedPacket.objects.all()
    serializer_class = CapturedPacketSerializer

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer