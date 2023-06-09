from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from core.models import DigitalUse, DigitalService, Area
from core.serializers import DigitalUseSerializer, DigitalServiceSerializer, AreaSerializer
from rest_framework.permissions import IsAuthenticated


class DigitalUseWriteViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = DigitalUse.objects.all()
    serializer_class = DigitalUseSerializer
    permission_classes = [IsAuthenticated]

class DigitalServiceWriteViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = DigitalService.objects.all()
    serializer_class = DigitalServiceSerializer

class AreaWriteViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]