from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import CapturedPacketViewSet, AlertViewSet, start_capture, stop_capture

router = DefaultRouter()
router.register(r'packets', CapturedPacketViewSet)
router.register(r'alerts', AlertViewSet)

urlpatterns = [
    path('start_capture/', start_capture, name='start_capture'),
    path('stop_capture/', stop_capture, name='stop_capture'),
    path('', include(router.urls)),
]
