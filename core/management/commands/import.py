from django.core.management.base import BaseCommand

from core.models import *
from taggit.models import Tag
import csv

class Command(BaseCommand):
    # help = "My shiny new management command."

    # def add_arguments(self, parser):
    #     parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        Tag.objects.all().delete()
        DigitalService.objects.all().delete()
        
        with open('data/usages.csv') as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                room_name, item_name, use_name, use_description, tags = row
                
                try:
                    room = Room.objects.get(name=room_name)
                except Room.DoesNotExist:
                    room = Room.objects.create(name=room_name)
                
                try:
                    item = Item.objects.get(name=item_name)
                except Item.DoesNotExist:
                    item = Item.objects.create(name=item_name, room=room)
                
                clean_tags = tags.replace('#', '').replace(' ', '').lower().split('\n')
                
                try:
                    use = DigitalUse.objects.get(title=use_name)
                    use.description = use_description
                    use.items.add(item)
                    use.tags.add(*clean_tags)
                    use.save()
                except DigitalUse.DoesNotExist:
                    use = DigitalUse.objects.create(title=use_name, description=use_description)
                    use.items.add(item)
                    use.tags.add(*clean_tags)
                
        with open('data/services.csv') as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                room_name, item_name, use_name, area_name, service_name, service_description, service_url = row
                
                if not room_name or not item_name or not use_name:
                    continue
                
                try:
                    room = Room.objects.get(name=room_name)
                except:
                    print(f"Room {room_name} does not exist")
                    
                try:
                    item = Item.objects.get(name=item_name)
                except:
                    print(f"Item {item_name} does not exist")
                    
                try:
                    use = DigitalUse.objects.get(title=use_name)
                except:
                    print(f"Use {use_name} does not exist")
                 
                if service_name:
                    service = DigitalService.objects.get_or_create(title=service_name, use=use)[0]
                    service.description = service_description
                    service.url = service_url
                    service.area = Area.objects.get_or_create(name=area_name)[0]
                    service.save()
                