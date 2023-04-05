from rest_framework import serializers
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from rest_flex_fields import FlexFieldsModelSerializer
from .models import *

class ZoneSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Zone
        fields = "__all__"


class DigitalServiceSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = DigitalService
        fields = "__all__"
        expandable_fields = {
            'uses': ('core.DigitalUseSerializer', {'many': True, 'read_only':True}),
            'zone': ZoneSerializer,
        }
              

class DigitalUseSerializer(TaggitSerializer, FlexFieldsModelSerializer):
    tags = TagListSerializerField()
    item_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Item.objects.all(), source='items')
    class Meta:
        model = DigitalUse
        fields = ('id', 'title', 'slug', 'description', 'services', 'items', 'tags', 'item_ids')
        expandable_fields = {
            'services': (DigitalServiceSerializer, {'many': True, 'read_only':True}),
            'items': ('core.ItemSerializer', {'many': True, 'read_only':True}),
        }

class ItemSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Item
        fields = "__all__"
        expandable_fields = {
          'uses': (DigitalUseSerializer, {'many': True, 'read_only':True}),
          'room': ('core.RoomSerializer', {'many': False, 'read_only':True}),
        }


class RoomSerializer(FlexFieldsModelSerializer):
    
    class Meta:
        model = Room
        fields = ('id', 'name', 'slug', 'description', 'video', 'items')
        expandable_fields = {
            'items': (ItemSerializer, {'many': True, 'read_only':True}), 
        }