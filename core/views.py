from rest_framework import viewsets
from .models import Room
from .serializers import RoomSerializer
class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer