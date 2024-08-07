from rest_framework import serializers
from .models import CapturedPacket, Alert

class CapturedPacketSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapturedPacket
        fields = '__all__'

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'