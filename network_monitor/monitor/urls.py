from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CapturedPacketViewSet, AlertViewSet

router = DefaultRouter()
router.register(r'packets', CapturedPacketViewSet)
router.register(r'alerts', AlertViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
