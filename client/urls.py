from django.conf import settings
from rest_framework import routers
from .views import RemoteAccessViewSet, MqttViewSet


router = routers.SimpleRouter()
router.register(r'remote-accesses', RemoteAccessViewSet, basename='remote-accesses')
router.register(r'mqtt', MqttViewSet, basename='mqtt')

urlpatterns = router.urls


if settings.MODE == 'STANDALONE' and settings.MQTT_BROKER:
    from . import mqtt
    print(f"Connecting to mqtt broker at {settings.MQTT_BROKER}")
    mqtt.client.loop_start()
else:
    print("No mqtt broker configured")