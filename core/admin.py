from django.contrib import admin
from .models import *
import os

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    def image_exits(self, obj):
        if obj.image == None:
            return False
        image_path = settings.MEDIA_ROOT / f"images/{obj.slug}.svg"
        return os.path.exists(image_path)
    image_exits.boolean = True
    image_exits.short_description = 'Image ok ?'

    list_display = ('uuid', 'name', 'slug', 'room', 'image_exits')
    list_filter = ('room',)

class ItemInline(admin.TabularInline):
    model = Item
    extra = 0

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    def video_exits(self, obj):
        if obj.video == None:
            return False
        video_path = settings.MEDIA_ROOT / f"videos/{obj.slug}.mp4"
        return os.path.exists(video_path)
    video_exits.boolean = True
    video_exits.short_description = 'Video ok ?'

    list_display = ('uuid', 'name', 'slug', 'main_color', 'video_exits')
    search_fields = ('name',)
    list_editable = ('main_color',)
    inlines = [ItemInline]
    

@admin.register(DigitalUse)
class DigitalUseAdmin(admin.ModelAdmin):

    def items_list(self, obj):
        return ", ".join([i.name for i in obj.items.all()])

    list_display = ('title', 'items_list')
    search_fields = ('title',)
    filter_horizontal = ('items',)


class DigitalServiceContactInline(admin.TabularInline):
    model = DigitalServiceContact
    extra = 0

@admin.register(DigitalService)
class DigitalServiceAdmin(admin.ModelAdmin):

    def items_list(self, obj):
        return ", ".join([i.name for i in obj.use.items.all()])

    list_display = ('title', 'use', 'items_list', 'area')
    search_fields = ('title',)
    inlines = [DigitalServiceContactInline]


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)