from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from org.serializers import OrganizationSerializer
from core.serializers import AreaSerializer
from .models import RemoteAccess

class RemoteAccessSerializer(FlexFieldsModelSerializer):
    default = serializers.BooleanField(read_only=True)
    api_key = serializers.CharField(write_only=True)

    class Meta:
        model = RemoteAccess
        fields = '__all__'
        expandable_fields = {
            'org' : (OrganizationSerializer, {'read_only': True}),
            'area' : (AreaSerializer, {'read_only': True}),
        }