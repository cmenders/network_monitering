from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import start_capture, stop_capture, get_packets, get_alerts, get_hostname_counts #, CapturedPacketViewSet, AlertViewSet

# router = DefaultRouter()
# router.register(r'packets', CapturedPacketViewSet)
# router.register(r'alerts', AlertViewSet)

urlpatterns = [
    path('start_capture/', start_capture, name='start_capture'),
    path('stop_capture/', stop_capture, name='stop_capture'),
    path('get_packets/', get_packets, name='get_packets'),
    path('get_alerts/', get_alerts, name='get_alerts'),
    path('get_hostname_counts/', get_hostname_counts, name='get_hostname_counts'),
    # path('', include(router.urls)),
]