from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import OrganizationSerializer, UserSerializer
from .models import Organization, OrganizationAPIKey
from rest_framework.permissions import IsAuthenticated
from .permissions import HasOrganizationAPIKey
from rest_framework_api_key.permissions import KeyParser

User = get_user_model()

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated | HasOrganizationAPIKey]

    @action(detail=True, methods=['delete'])
    def revoke_key(self, request, pk=None):
        key_id = request.GET.get('key', None)
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

    @action(detail=False, methods=['get'])
    def me(self, request):
        key = KeyParser().get(request)
        if key:
            org_key = OrganizationAPIKey.objects.get_from_key(key)
            return Response(OrganizationSerializer(org_key.organization).data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)


    


class UserViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated | HasOrganizationAPIKey]
    queryset = User.objects.all()
    serializer_class = UserSerializer