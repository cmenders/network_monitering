from django.db import models

class CapturedPacket(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    src_ip = models.CharField(max_length=15)
    dst_ip = models.CharField(max_length=15)
    protocol = models.IntegerField()
    src_port = models.IntegerField(null=True, blank=True)
    dst_port = models.IntegerField(null=True, blank=True)
    details = models.TextField()

class Alert(models.Model):
    message = models.CharField(max_length=255)
    count = models.IntegerField(default=1)  
    timestamp = models.DateTimeField(auto_now_add=True)