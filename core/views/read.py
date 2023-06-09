from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from taggit.models import Tag
from core.models import Room, DigitalUse, DigitalService, Item
from core.serializers import RoomSerializer, DigitalUseSerializer, DigitalServiceSerializer, ItemSerializer
from org.permissions import HasOrganizationAPIKey

class RoomReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [HasOrganizationAPIKey]

class ItemReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [HasOrganizationAPIKey]
    lookup_field = 'uuid'


class DigitalUseReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = DigitalUse.objects.all()
    serializer_class = DigitalUseSerializer
    permission_classes = [HasOrganizationAPIKey]
    lookup_field = 'uuid'

class DigitalServiceReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = DigitalService.objects.all()
    serializer_class = DigitalServiceSerializer
    permission_classes = [HasOrganizationAPIKey]

class TagApiView(APIView):
    def get(self, request, format=None):
        tags = Tag.objects.exclude(name="").values_list('name', flat=True)
        return Response(tags)