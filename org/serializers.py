from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer as BaseRegisterSerializer
from dj_rest_auth.serializers import PasswordResetSerializer as BasePasswordResetSerializer, UserDetailsSerializer
from dj_rest_auth.serializers import LoginSerializer as BaseLoginSerializer
from dj_rest_auth.serializers import AllAuthPasswordResetForm
from allauth.account.forms import default_token_generator
from rest_flex_fields import FlexFieldsModelSerializer
from allauth.account.utils import user_pk_to_url_str
from allauth.account.adapter import get_adapter

from django.conf import settings
from .models import Organization, OrganizationAPIKey
from django.utils import timezone

class LoginSerializer(BaseLoginSerializer):
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

class RegisterSerializer(BaseRegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'first_name': self.validated_data.get('first_name'),
            'last_name': self.validated_data.get('last_name')
        })
        return data

class PasswordResetForm(AllAuthPasswordResetForm):
    def save(self, request, **kwargs):
        current_site = settings.FRONTEND_URL
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator', default_token_generator)
        for user in self.users:
            temp_key = token_generator.make_token(user)
            url = settings.FRONTEND_URL + f"/auth/reset-password/{user_pk_to_url_str(user)}/{temp_key}"
            context = {
                'current_site': current_site,
                'user': user,
                'password_reset_url': url,
                'request': request,
            }
            get_adapter(request).send_mail('account/email/password_reset_key', email, context)
        return self.cleaned_data['email']

class PasswordResetSerializer(BasePasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        return PasswordResetForm


class APIKeySerializer(FlexFieldsModelSerializer):
    created_by = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        date = timezone.localtime(obj.created)
        return date.strftime("%d/%m/%Y %Hh%M")

    def get_created_by(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else ''
    class Meta:
        model = OrganizationAPIKey
        exclude = ('expiry_date', 'hashed_key',)

class OrganizationSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"
        expandable_fields = {
            'members' : ('org.UserSerializer', {'many': True, 'read_only':True}),
            'api_keys': (APIKeySerializer, {'many': True, 'read_only':True}),
        }

class UserSerializer(UserDetailsSerializer):
    is_superuser = serializers.BooleanField(read_only=True)
    org = OrganizationSerializer(read_only=True, source="organization")
    org_id = serializers.PrimaryKeyRelatedField(write_only=False, allow_null=True, queryset=Organization.objects.all(), source='organization')

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('is_superuser', 'org', 'org_id', 'id')