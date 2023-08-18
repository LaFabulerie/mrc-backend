from django.core.management.base import BaseCommand

from core.models import *
from taggit.models import Tag
import csv


class Command(BaseCommand):

    def handle(self, *args, **options):
        Tag.objects.all().delete()
        
        with open('data/mrc.csv') as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader) # skip header
            for row in csv_reader:
                # 'NOM USAGE', 'IDENTIFIANT UNIQUE', 'DESCRIPTION', 'TAGS', 'NOM OBJET', 'IDENTIFIANT OBJET', 'CONTROLEUR LUMIERE OBJET', 'BROCHE LUMIERE OBJET', 'NOM PIECE', 'IDENTIFIANT PIECE', 'COULEUR', 'POSITION', 'BROCHE RUBAN LED'
                use_name, use_uuid, use_description, use_tags_raw, item_name, item_uuid, item_light_ctrl, item_light_pin, room_name, room_uuid, room_color, room_position, room_light_pin = row
                
                try:
                    room = Room.objects.get(uuid=room_uuid)
                    room.name = room_name
                    # room.main_color = room_color
                    # room.position = room_position
                    # room.light_pin = int(room_light_pin) if room_light_pin else None
                    # room.save()
                except Room.DoesNotExist:
                    room = Room.objects.create(
                        name=room_name, 
                        uuid=room_uuid,
                        main_color=room_color,
                        position=room_position,
                        light_pin=int(room_light_pin) if room_light_pin else None
                    )
                
                try:
                    item = Item.objects.get(uuid=item_uuid)
                    # item.name = item_name
                    # item.room = room
                    # item.light_ctrl = int(item_light_ctrl) if item_light_ctrl else None
                    # item.light_pin = item_light_pin
                    # item.save()
                except Item.DoesNotExist:
                    item = Item.objects.create(
                        name=item_name, 
                        room=room, 
                        uuid=item_uuid,
                        light_ctrl=int(item_light_ctrl) if item_light_ctrl else None,
                        light_pin=item_light_pin
                    )
                    
                try:
                    use = DigitalUse.objects.get(uuid=use_uuid)
                    # use.title = use_name
                    # use.description = use_description
                    # use.items.add(item)
                    # use.save()
                except DigitalUse.DoesNotExist:
                    use = DigitalUse.objects.create(title=use_name, description=use_description, uuid=use_uuid)
                    use.items.add(item)
                    use.save()
                
                clean_tags = use_tags_raw.split(';')
                use.tags.add(*clean_tags)
        
        service_purged = False
        with open('data/services.csv') as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                use_name, use_uuid, area_name, service_name, service_description, service_url = row
                
                area, created = Area.objects.get_or_create(name=area_name)
                if not created and not service_purged:
                    area.services.all().delete()
                    service_purged = True
                
                service = DigitalService.objects.create(
                    title=service_name,
                    description=service_description,
                    area=area,
                    url=service_url,
                    use=DigitalUse.objects.get(uuid=use_uuid)
                )
                