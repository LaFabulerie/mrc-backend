import csv
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from taggit.models import Tag
from core.models import Room, DigitalUse, DigitalService, Item, Contribution
from core.serializers import RoomSerializer, DigitalUseSerializer, DigitalServiceSerializer, ItemSerializer, ContributionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from core.permissions import IsLocalAccess
from org.permissions import HasOrganizationAPIKey
import sys

from core.import_export import export_services


class RoomReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]
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
        bw_path = []

        current_room = start_room
        while current_room.uuid != end_room.uuid:
            fw_path.append(current_room)
            current_room = current_room.previous_room.first()
        fw_path.pop(0)
        fw_path.append(end_room)

        current_room = start_room
        while current_room.uuid != end_room.uuid:
            bw_path.append(current_room)
            current_room = current_room.next_room
        bw_path.pop(0)
        bw_path.append(end_room)


        d1 = sys.maxsize
        d2 = sys.maxsize

        if not self.crossed_garden(fw_path):
            d1 = len(fw_path)

        if not self.crossed_garden(bw_path):
            d2 = -len(bw_path)

        resp['distance'] = d1 if abs(d1) < abs(d2) else d2

        return Response(resp)



class ItemReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]
    lookup_field = 'uuid'


class DigitalUseReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = DigitalUse.objects.all()
    serializer_class = DigitalUseSerializer
    permission_classes = [AllowAny]
    lookup_field = 'uuid'

class DigitalServiceReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = DigitalService.objects.all()
    serializer_class = DigitalServiceSerializer
    permission_classes = [AllowAny]

class ContributionReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer
    permission_classes = [IsLocalAccess | HasOrganizationAPIKey | IsAuthenticated]

class TagApiView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        tags = Tag.objects.exclude(name="").values_list('name', flat=True)
        return Response(tags)


class ExportDigitalServiceApiView(APIView):
    permission_classes = [IsLocalAccess | HasOrganizationAPIKey | IsAuthenticated]
    def post(self, request, format=None):
        uuids = request.data['uuids']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        export_services(response, uuids)
        return response
