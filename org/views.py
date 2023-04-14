from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import OrganizationSerializer, UserSerializer
from .models import Organization, OrganizationAPIKey

User = get_user_model()

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    @action(detail=True, methods=['delete'])
    def revoke_key(self, request, pk=None):
        key_id = request.GET.get('key', None)
        print(key_id)
        key = self.get_object().api_keys.filter(id=key_id).first()
        if(key is not None and self.get_object().members.filter(id=request.user.id).exists()):
            key.revoked = True
            key.save()
            return Response(status=204)
        return Response(status=404)
    
    @action(detail=True, methods=['post'])
    def create_key(self, request, pk=None):
        key_name = request.data.get('name', None)
        if(key_name is not None and self.get_object().members.filter(id=request.user.id).exists()):
            key, key_value = OrganizationAPIKey.objects.create_key(name='youpi', organization=self.get_object(), created_by=request.user)
            return Response({'key': key_value}, status=201)
        return Response(status=403)


class UserViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer