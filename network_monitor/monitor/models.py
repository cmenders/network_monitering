# network_monitor/monitor/models.py
from django.db import models

class CapturedPacket(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    src_ip = models.CharField(max_length=15)
    dst_ip = models.CharField(max_length=15)
    protocol = models.CharField(max_length=10)
    src_port = models.IntegerField(null=True, blank=True)
    dst_port = models.IntegerField(null=True, blank=True)
    details = models.TextField()

class Alert(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()