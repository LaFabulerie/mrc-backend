from django.core.management.base import BaseCommand

from core.models import *
from taggit.models import Tag
import csv
from core.import_export import import_services


class Command(BaseCommand):

    def handle(self, *args, **options):
        Tag.objects.all().delete()
        
        with open('data/mrc.csv') as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader) # skip header

            next_rooms = {}

            for row in csv_reader:
                # 'NOM USAGE', 'IDENTIFIANT UNIQUE', 'DESCRIPTION', 'TAGS', 'NOM OBJET', 'IDENTIFIANT OBJET', 'CONTROLEUR LUMIERE OBJET', 'BROCHE LUMIERE OBJET', 'NOM PIECE', 'IDENTIFIANT PIECE', 'COULEUR', 'ID PIECE SUIVANTE'
                use_name, use_uuid, use_description, use_tags_raw, item_name, item_uuid, item_light_ctrl, item_light_pin, room_name, room_uuid, room_color, next_room_uuid = row
                
                try:
                    room = Room.objects.get(uuid=room_uuid)
                except Room.DoesNotExist:
                    room = Room.objects.create(
                        name=room_name, 
                        uuid=room_uuid,
                        main_color=room_color,
                    )

                    if next_room_uuid:
                        next_rooms[room_uuid] = next_room_uuid
                
                try:
                    item = Item.objects.get(uuid=item_uuid)
                except Item.DoesNotExist:
                    item = Item.objects.create(
                        name=item_name, 
                        room=room, 
                        uuid=item_uuid,
                        light_ctrl=int(item_light_ctrl) if item_light_ctrl else None,
                        light_pin=item_light_pin
                    )
            
            for room_uuid, next_room_uuid in next_rooms.items():
                try:
                    room = Room.objects.get(uuid=room_uuid)
                    next_room = Room.objects.get(uuid=next_room_uuid)
                    room.next_room = next_room
                    room.save()
                except Room.DoesNotExist:
                    pass
        
        # with open('data/services.csv') as fd:
        #     import_services(fd)
