from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.admin import APIKeyModelAdmin
from rest_framework.authtoken.models import TokenProxy
from allauth.socialaccount.models import SocialApp, SocialToken, SocialAccount
from .models import OrganizationAPIKey, Organization, User

admin.site.unregister(TokenProxy)
admin.site.unregister(APIKey)
admin.site.unregister(Group)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = [s for s in BaseUserAdmin.fieldsets]
    fieldsets.append(('Organization', {'fields': ('organization',)}))

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass

@admin.register(OrganizationAPIKey)
class OrganizationAPIKeyModelAdmin(APIKeyModelAdmin):
    pass