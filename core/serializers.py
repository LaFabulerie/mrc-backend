from rest_framework import serializers
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from rest_flex_fields import FlexFieldsModelSerializer
from .models import *

class AreaSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"


class DigitalServiceSerializer(FlexFieldsModelSerializer):
    use_id = serializers.PrimaryKeyRelatedField(write_only=False, queryset=DigitalUse.objects.all(), source='use')
    area_id = serializers.PrimaryKeyRelatedField(write_only=False, queryset=Area.objects.all(), source='area')
    
    class Meta:
        model = DigitalService
        fields = "__all__"
        expandable_fields = {
            'use': ('core.DigitalUseSerializer', {'read_only':True}),
            'area': ('core.AreaSerializer', {'read_only':True}),
        }
              

class DigitalUseSerializer(TaggitSerializer, FlexFieldsModelSerializer):
    tags = TagListSerializerField()
    item_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Item.objects.all(), source='items')
    class Meta:
        model = DigitalUse
        fields = ('id', 'title', 'slug', 'description', 'services', 'items', 'tags', 'item_ids', 'uuid')
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
        fields = ('id', 'name', 'slug', 'video', 'items', 'uuid', 'main_color', 'position', 'light_pin')
        expandable_fields = {
            'items': (ItemSerializer, {'many': True, 'read_only':True}), 
        }