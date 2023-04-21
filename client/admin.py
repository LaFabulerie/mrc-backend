from django.contrib import admin
from django.conf import settings


if settings.CLIENT_MODE:
    from .models import RemoteAccess
    @admin.register(RemoteAccess)
    class RemoteAccessAdmin(admin.ModelAdmin):
        list_display =  ('name', 'server_url', 'api_key_prefix', 'default')