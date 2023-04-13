from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room, DigitalUse, DigitalService, Area
from .serializers import RoomSerializer, DigitalUseSerializer, DigitalServiceSerializer, AreaSerializer
from taggit.models import Tag
class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class DigitalUseViewSet(viewsets.ModelViewSet):
    queryset = DigitalUse.objects.all()
    serializer_class = DigitalUseSerializer

class DigitalServiceViewSet(viewsets.ModelViewSet):
    queryset = DigitalService.objects.all()
    serializer_class = DigitalServiceSerializer
    
class TagApiView(APIView):
    
    def get(self, request, format=None):
        tags = Tag.objects.exclude(name="").values_list('name', flat=True)
        return Response(tags)

class AreaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer