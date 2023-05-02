from django.conf import settings
from rest_framework import routers
from .views import RemoteAccessViewSet, MqttViewSet


router = routers.SimpleRouter()
router.register(r'remote-accesses', RemoteAccessViewSet, basename='remote-accesses')
router.register(r'mqtt', MqttViewSet, basename='mqtt')

urlpatterns = router.urls


if settings.CLIENT_MODE:
    from . import mqtt
    mqtt.client.loop_start()