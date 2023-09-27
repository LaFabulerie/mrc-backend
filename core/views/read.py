from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from taggit.models import Tag
from core.models import Room, DigitalUse, DigitalService, Item
from core.serializers import RoomSerializer, DigitalUseSerializer, DigitalServiceSerializer, ItemSerializer
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from core.permissions import IsLocalAccess
from org.permissions import HasOrganizationAPIKey



class RoomReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsLocalAccess | HasOrganizationAPIKey | IsAuthenticated| AllowAny]
    lookup_field = 'uuid'

    def crossed_garden(self, path):
        for room in path:
            if room.slug == "jardin":
                return True
        return False
        

    @action(detail=False, methods=['get'])
    def distance(self, request):
        from_room_uuid = request.GET.get('from', None)
        to_room_uuid = request.GET.get('to', None)

        start_room = self.get_queryset().get(uuid=from_room_uuid)
        end_room = self.get_queryset().get(uuid=to_room_uuid)
        
        fw_path = []
        bw_path = []

        current_room = start_room
        while current_room.uuid != end_room.uuid:
            fw_path.append(current_room)
            current_room = current_room.previous_room.first()
        fw_path.append(end_room)
        
        current_room = start_room
        while current_room.uuid != end_room.uuid:
            bw_path.append(current_room)
            current_room = current_room.next_room
        bw_path.append(end_room)

        resp = {
            'uuid': end_room.uuid,
            'slug': end_room.slug,
            'distance' : 0
        }

        if self.crossed_garden(fw_path):
            resp["distance"] = -len(bw_path)
        
        if self.crossed_garden(bw_path):
            resp["distance"] = len(fw_path)

        
        return Response(resp)
    


class ItemReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsLocalAccess | HasOrganizationAPIKey | IsAuthenticated]
    lookup_field = 'uuid'


class DigitalUseReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = DigitalUse.objects.all()
    serializer_class = DigitalUseSerializer
    permission_classes = [IsLocalAccess | HasOrganizationAPIKey | IsAuthenticated]
    lookup_field = 'uuid'

class DigitalServiceReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = DigitalService.objects.all()
    serializer_class = DigitalServiceSerializer
    permission_classes = [IsLocalAccess | HasOrganizationAPIKey | IsAuthenticated]

class TagApiView(APIView):
    def get(self, request, format=None):
        tags = Tag.objects.exclude(name="").values_list('name', flat=True)
        return Response(tags)

