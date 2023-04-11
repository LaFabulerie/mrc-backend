from django.contrib import admin
from .models import *


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [ItemInline]
    

@admin.register(DigitalUse)
class DigitalUseAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    filter_horizontal = ('items',)


class DigitalServiceContactInline(admin.TabularInline):
    model = DigitalServiceContact
    extra = 0

@admin.register(DigitalService)
class DigitalServiceAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    inlines = [DigitalServiceContactInline]


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)