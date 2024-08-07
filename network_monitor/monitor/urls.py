from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CapturedPacketViewSet, AlertViewSet, start_capture

router = DefaultRouter()
router.register(r'packets', CapturedPacketViewSet)
router.register(r'alerts', AlertViewSet)

urlpatterns = [
    path('start_capture/', start_capture, name='start_capture'),
    path('', include(router.urls)),
]
