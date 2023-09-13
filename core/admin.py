from django.contrib import admin
from .models import *
import os
from taggit.models import Tag
from taggit.admin import TaggedItemInline

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    def image_exits(self, obj):
        if obj.image == None:
            return False
        image_path = settings.STATIC_ROOT / f"images/{obj.slug}.svg"
        return os.path.exists(image_path)
    image_exits.boolean = True
    image_exits.short_description = 'Image ok ?'
    


    list_display = ('uuid', 'name', 'slug', 'room', 'image_exits', 'light_ctrl', 'light_pin')
    list_filter = ('room',)
    list_editable = ('room', 'light_ctrl', 'light_pin')

class ItemInline(admin.TabularInline):
    model = Item
    extra = 0

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    def video_exits(self, obj):
        if obj.video == None:
            return False
        video_path = settings.STATIC_ROOT / f"videos/{obj.slug}.mp4"
        return os.path.exists(video_path)
    video_exits.boolean = True
    video_exits.short_description = 'Video ok ?'

    def get_previous_room(self, obj):
        previous_room = obj.previous_room.first()
        if previous_room:
            return previous_room.name
        return None
    get_previous_room.short_description = 'Pièce précédente'

    list_display = ('uuid', 'name', 'slug', 'main_color', 'video_exits', 'position')
    search_fields = ('name',)
    list_editable = ('main_color', 'position')
    inlines = [ItemInline]
    

@admin.register(DigitalUse)
class DigitalUseAdmin(admin.ModelAdmin):

    def items_list(self, obj):
        return ", ".join([i.name for i in obj.items.all()])
    items_list.short_description = 'Objets'
    
    def tags_list(self, obj):
        return ";".join([t.name for t in obj.tags.all()])
    tags_list.short_description = 'Tags'
    
    def service_count(self, obj):
        return obj.services.count()
    service_count.short_description = 'Nb services'

    list_display = ('title', 'uuid', 'tags_list', 'items_list', 'service_count')
    search_fields = ('title',)
    filter_horizontal = ('items',)


class DigitalServiceContactInline(admin.TabularInline):
    model = DigitalServiceContact
    extra = 0

@admin.register(DigitalService)
class DigitalServiceAdmin(admin.ModelAdmin):

    def items_list(self, obj):
        return ", ".join([i.name for i in obj.use.items.all()])

    list_display = ('title', 'uuid', 'use', 'items_list', 'area')
    search_fields = ('title', 'uuid',)
    inlines = [DigitalServiceContactInline]


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
admin.site.unregister(Tag)
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ["id", "name", "slug"]
    list_editable = ["name"]
    ordering = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}
