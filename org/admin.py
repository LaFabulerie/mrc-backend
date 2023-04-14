from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.admin import APIKeyModelAdmin
from rest_framework.authtoken.models import TokenProxy
from .models import OrganizationAPIKey, Organization

from .models import User
admin.site.unregister(TokenProxy)
admin.site.unregister(APIKey)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass

@admin.register(OrganizationAPIKey)
class OrganizationAPIKeyModelAdmin(APIKeyModelAdmin):
    pass