from rest_framework import viewsets
from .models import Room, DigitalUse
from .serializers import RoomSerializer, DigitalUseSerializer
class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class DigitalUseViewSet(viewsets.ModelViewSet):
    queryset = DigitalUse.objects.all()
    serializer_class = DigitalUseSerializer