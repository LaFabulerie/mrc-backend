from rest_framework import serializers
from .models import *

class DigitalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalService
        # fields = "__all__"
        exclude = ('uses',)


class DigitalUseSerializer(serializers.ModelSerializer):
    services = DigitalServiceSerializer(many=True, read_only=True)
    class Meta:
        model = DigitalUse
        # fields = "__all__"
        exclude = ('items',)

class ItemSerializer(serializers.ModelSerializer):
    uses = DigitalUseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Item
        # fields = "__all__"
        exclude = ('room',)


class RoomSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Room
        fields = "__all__"