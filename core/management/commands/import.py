from django.core.management.base import BaseCommand

from core.models import *

import csv

class Command(BaseCommand):
    # help = "My shiny new management command."

    # def add_arguments(self, parser):
    #     parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
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
                
                clean_tags = tags.replace('#', '').split('\n')
                
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
                
                