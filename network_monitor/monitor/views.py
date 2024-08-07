from django.shortcuts import render
from rest_framework import viewsets
from .models import CapturedPacket, Alert
from .serializers import CapturedPacketSerializer, AlertSerializer

class CapturedPacketViewSet(viewsets.ModelViewSet):
    queryset = CapturedPacket.objects.all()
    serializer_class = CapturedPacketSerializer

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer