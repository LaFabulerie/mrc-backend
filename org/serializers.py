from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer as BaseRegisterSerializer
from dj_rest_auth.serializers import PasswordResetSerializer as BasePasswordResetSerializer
from dj_rest_auth.serializers import AllAuthPasswordResetForm
from allauth.account.forms import default_token_generator
from allauth.account.utils import user_pk_to_url_str
from allauth.account.adapter import get_adapter
from django.urls import reverse
from django.conf import settings

class RegisterSerializer(BaseRegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'first_name': self.validated_data.get('first_name'),
            'last_name': self.validated_data.get('last_name')
        })
        print(data)
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