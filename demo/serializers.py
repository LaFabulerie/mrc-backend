from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from .models import *
from core.serializers import  ItemSerializer, RoomSerializer, DigitalUseSerializer


class ScenarioUseChoiceStepSerializer(FlexFieldsModelSerializer):
    use = DigitalUseSerializer(read_only=True, fields=['id', 'title'])

    class Meta:
        model = ScenarioUseChoiceStep
        exclude = ('item_step',)

        expandable_fields = {
            'use': (DigitalUseSerializer, {'read_only': True}),
        }


class ScenarioItemChoiceStepSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True, fields=['id', 'name'])
    uses = ScenarioUseChoiceStepSerializer(many=True, read_only=True)

    class Meta:
        model = ScenarioItemChoiceStep
        exclude = ('room_step',)

class ScenarioRoomChoiceStepSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True, fields=['id', 'name'])
    items = ScenarioItemChoiceStepSerializer(many=True, read_only=True)

    class Meta:
        model = ScenarioRoomChoiceStep
        exclude = ('scenario',)


class ScenarioSerializer(serializers.ModelSerializer):
    rooms = ScenarioRoomChoiceStepSerializer(many=True, read_only=True)

    class Meta:
        model = Scenario
        fields = '__all__'
