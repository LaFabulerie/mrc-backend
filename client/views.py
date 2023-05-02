from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from org.models import Organization
from .serializers import RemoteAccessSerializer
from .models import RemoteAccess
from core.models import *
from org.models import Organization
import requests

class RemoteAccessViewSet(viewsets.ModelViewSet):
    queryset = RemoteAccess.objects.all()
    serializer_class = RemoteAccessSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        remote_access = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        remote_access.api_key_prefix = remote_access.api_key.split('.')[0]
        if RemoteAccess.objects.filter(default=True).count() == 0:
            remote_access.default = True
        remote_access.save()
        
        resp = requests.get(f"{remote_access.server_url}/api/orgs/me/", headers={'Authorization': 'Api-Key ' + remote_access.api_key})
        data = resp.json()
        area = Area.objects.filter(uuid=data['area']['uuid']).first()
        if not area:
            area = Area.objects.create(**data['area'])
        del data['areaId']
        data["area"] = area
        organization = Organization.objects.filter(uuid=data['uuid']).first()
        if not organization:
            organization = Organization.objects.create(**data)

        remote_access.org = organization
        remote_access.area = area
        remote_access.save()

        return Response({'msg' : 'Accès enregistré avec succés.'}, status=status.HTTP_201_CREATED, headers=headers)
    

    @action(detail=True, methods=['get'])
    def synchronize(self, request, pk=None):
        remote_access = self.get_object()
        params = "expand=items,items.room,services,services.area&omit=slug,id,items.slug,items.id,items.room.items,items.room.id,items.room.slug,services.id,services.slug,services.use"
        resp = requests.get(f"{remote_access.server_url}/api/digital-uses/?{params}", headers={'Authorization': 'Api-Key ' + remote_access.api_key})

        if(resp.status_code == 200):
            digital_uses = resp.json()
            for digital_use in digital_uses:
                use_obj = DigitalUse.objects.filter(uuid=digital_use['uuid']).first()
                if not use_obj:
                    use_obj = DigitalUse.objects.create(
                        uuid=digital_use['uuid'],
                        title=digital_use['title'],
                        description=digital_use['description'],
                    )
                
                use_obj.tags.set(digital_use['tags'], clear=True)
                
                for item in digital_use['items']:
                    room = Room.objects.filter(uuid=item['room']['uuid']).first()
                    if not room:
                        room = Room.objects.create(**item['room'])
                    item['room'] = room
                    _item = Item.objects.filter(uuid=item['uuid']).first()
                    if not _item:
                        _item = Item.objects.create(**item)
                    use_obj.items.add(_item)
                
                for service in digital_use['services']:
                    area = Area.objects.filter(uuid=service['area']['uuid']).first()
                    if not area:
                        area = Area.objects.create(
                            uuid=service['area']['uuid'],
                            name=service['area']['name'],
                        )
                    _service = DigitalService.objects.filter(uuid=service['uuid']).first()
                    if not _service:
                        _service = DigitalService.objects.create(
                            uuid=service['uuid'],
                            title=service['title'],
                            description=service['description'],
                            area=area,
                            url=service['url'],
                            use=use_obj,
                        )
            return Response({'msg' : 'Synchronisation effectuée avec succés.'}, status=status.HTTP_200_OK)
        

        return Response({'msg' : 'Une erreur est survenue lors de la synchronisation.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class MqttViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def publish(self, request):
        from .mqtt import client as mqtt_client
        mqtt_client.publish(**request.data)
        return Response(status=status.HTTP_200_OK)
