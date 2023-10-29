from django.core.management.base import BaseCommand
from core.models import *
from core.import_export import export_services
import pandas as pd

class Command(BaseCommand):
   
    def handle(self, *args, **options):

        with open('data/services.csv', 'w', encoding="UTF-8") as fd:
            export_services(fd, DigitalService.objects.all().values_list('uuid', flat=True))
        

        rooms_df = pd.DataFrame(columns=['NOM', 'IDENTIFIANT UNIQUE', 'NOM STANDARDISÉ', 'COULEUR', 'ID PIECE SUIVANTE'])
        for room in Room.objects.all():
            rooms_df.loc[len(rooms_df)] = [room.name, room.uuid, room.slug, room.main_color, room.next_room.uuid if room.next_room else '']
        
        items_df = pd.DataFrame(columns=['NOM', 'IDENTIFIANT UNIQUE', 'NOM STANDARDISÉ', 'PIECE', 'IDENTIFIANT PIECE', 'CONTROLEUR LUMIERE', 'BROCHE LUMIERE'])
        for item in Item.objects.all():
            items_df.loc[len(items_df)] = [item.name, item.uuid, item.slug, item.room.name, item.room.uuid, item.light_ctrl, item.light_pin]
        
        uses_df = pd.DataFrame(columns=['NOM', 'IDENTIFIANT UNIQUE', 'TAGS'])
        mrc_df = pd.DataFrame(columns=['NOM USAGE', 'IDENTIFIANT UNIQUE', 'DESCRIPTION', 'TAGS', 'NOM OBJET', 'IDENTIFIANT OBJET', 'CONTROLEUR LUMIERE OBJET', 'BROCHE LUMIERE OBJET', 'NOM PIECE', 'IDENTIFIANT PIECE', 'COULEUR', 'ID PIECE SUIVANTE'])

        for use in DigitalUse.objects.all():
            uses_df.loc[len(uses_df)] = [use.title, use.uuid, ";".join([t.name for t in use.tags.all()])]
            for item in use.items.all():
                mrc_df.loc[len(mrc_df)] = [use.title, use.uuid, use.description, ";".join([t.name for t in use.tags.all()]), item.name, item.uuid, item.light_ctrl, item.light_pin, item.room.name, item.room.uuid, item.room.main_color, item.room.next_room.uuid if item.room.next_room else '']
        
        with pd.ExcelWriter('mrc.xlsx') as writer:
            rooms_df.to_excel(writer, sheet_name='DATA_PIECES', index=False)
            items_df.to_excel(writer, sheet_name='DATA_OBJETS', index=False)
            uses_df.to_excel(writer, sheet_name='DATA_USAGES', index=False)
            mrc_df.to_excel(writer, sheet_name='MRC_FULL', index=False)
        
        mrc_df.to_csv('data/mrc.csv', sep=',', index=False)

        

        
        

        
            

