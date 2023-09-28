from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from taggit.models import Tag
from core.models import Room, DigitalUse, DigitalService, Item
from core.serializers import RoomSerializer, DigitalUseSerializer, DigitalServiceSerializer, ItemSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from core.permissions import IsLocalAccess
from org.permissions import HasOrganizationAPIKey
import sys


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

        resp = {
            'uuid': end_room.uuid,
            'slug': end_room.slug,
            'distance' : 0
        }

        if from_room_uuid == to_room_uuid:
            return Response(resp)
        
        fw_path = []

        current_room = start_room
        while current_room.uuid != end_room.uuid:
            if(current_room.slug != "jardin"):
                fw_path.append(current_room)
            current_room = current_room.next_room
        fw_path.pop(0)
        fw_path.append(end_room)

        print(fw_path)
        
        resp['distance'] = len(fw_path)

        return Response(resp)     

    # @action(detail=False, methods=['get'])
    # def distance(self, request):
    #     from_room_uuid = request.GET.get('from', None)
    #     to_room_uuid = request.GET.get('to', None)

    #     start_room = self.get_queryset().get(uuid=from_room_uuid)
    #     end_room = self.get_queryset().get(uuid=to_room_uuid)

    #     resp = {
    #         'uuid': end_room.uuid,
    #         'slug': end_room.slug,
    #         'distance' : 0
    #     }

    #     if from_room_uuid == to_room_uuid:
    #         return Response(resp)
        
    #     fw_path = []
    #     bw_path = []

    #     current_room = start_room
    #     while current_room.uuid != end_room.uuid:
    #         fw_path.append(current_room)
    #         current_room = current_room.previous_room.first()
    #     fw_path.pop(0)
    #     fw_path.append(end_room)
        
    #     current_room = start_room
    #     while current_room.uuid != end_room.uuid:
    #         bw_path.append(current_room)
    #         current_room = current_room.next_room
    #     bw_path.pop(0)
    #     bw_path.append(end_room)

    #     d1 = sys.maxsize
    #     d2 = sys.maxsize

    #     if not self.crossed_garden(fw_path):
    #         d1 = len(fw_path)
        
    #     if not self.crossed_garden(bw_path):
    #         d2 = -len(bw_path)

    #     resp['distance'] = d1 if abs(d1) < abs(d2) else d2

    #     return Response(resp)
    


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

