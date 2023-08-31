import time

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .mqtt import client as mqtt_client
import json
from django.conf import settings
import time
class ScenarioViewSet(ModelViewSet):
    model = Scenario
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['get'])
    def run(self, request, pk=None):
        scenario = self.get_object()

        mqtt_client.publish("mrc/mode", json.dumps({
            "mode": 'primary',
            "uniqueId": settings.SECRET_KEY,
            "type": 'RESP',
            "value": 'OK'
        }))
        mqtt_client.publish("mrc/nav", json.dumps({
            "url": ['map']
        }))
        time.sleep(1)

        for i, room_step in enumerate(scenario.room_steps.all()):
            print("-> GO TO", room_step.room.name)
            mqtt_client.publish("mrc/nav", json.dumps({
                "url": ['room', room_step.room.slug, str(room_step.room.uuid)],
            }))
            time.sleep(1)
            for j, item_step in enumerate(room_step.item_steps.all()):
                print("--> GO TO ITEM", item_step.item.name)
                for k, use_step in enumerate(item_step.use_steps.all()):
                    print("---> CHOOSE USE", use_step.use.title)
                    if k == item_step.use_steps.count() - 1:
                        print("-> GO TO", room_step.room.name)
                    else:
                        print("-> GO TO ITEM", item_step.item.name)
            print("-> GO TO MAP\n")
            mqtt_client.publish("mrc/nav", json.dumps({
                "url": ['map']
            }))


        return Response({'status': 'ok'}, status=status.HTTP_200_OK)
