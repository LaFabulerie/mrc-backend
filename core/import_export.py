import csv
from rest_framework.response import Response
from rest_framework import status
from core.models import DigitalService, DigitalUse, Item, Room


def export_services(fd, uuids):
    writer = csv.writer(fd)
    writer.writerow([
        "USAGE",
        "IDENTIFIANT USAGE",
        "DESCRIPTION",
        "TAGS USAGE",
        "OBJET",
        "IDENTIFIANT OBJET",
        "PIECE",
        "IDENTIFIANT PIECE",
        "TERRITOIRE",
        "TITRE SERVICE",
        "IDENTIFIANT SERVICE",
        "DESC. SERVICE",
        "URL SERVICE",
        "CONTACT SERVICE",
    ])
    digital_services = DigitalService.objects.filter(uuid__in=uuids)
    for digital_service in digital_services:
        writer.writerow([
            digital_service.use.title,
            digital_service.use.uuid,
            digital_service.use.description,
            ";".join([t.name for t in digital_service.use.tags.all()]),
            digital_service.use.items.all().first().name,
            digital_service.use.items.all().first().uuid,
            digital_service.use.items.all().first().room.name,
            digital_service.use.items.all().first().room.uuid,
            digital_service.scope,
            digital_service.title,
            digital_service.uuid,
            digital_service.description,
            digital_service.url,
            digital_service.contact,
        ])

def import_services(fb):
    reader = csv.reader(fb)
    next(reader)
    # "USAGE",
    # "IDENTIFIANT USAGE",
    # "DESCRIPTION",
    # "TAGS USAGE",
    # "OBJET",
    # "IDENTIFIANT OBJET",
    # "PIECE",
    # "IDENTIFIANT PIECE",
    # "TERRITOIRE",
    # "TITRE SERVICE",
    # "IDENTIFIANT SERVICE",
    # "DESC. SERVICE",
    # "URL SERVICE",
    # "CONTACT SERVICE",

    messages = []
    rows = []

    for row in reader:
        use_name, use_uuid, use_description, use_tags_raw,\
        item_name, item_uuid, room_name, room_uuid, scope, service_title,\
        service_uuid, service_desc, service_url, service_contact  = row

        room = Room.objects.filter(uuid=room_uuid).first()
        if not room:
            room = Room.objects.create(
                uuid=room_uuid,
                name=room_name,
            )
        item = Item.objects.filter(uuid=item_uuid).first()
        if not item:
            item = Item.objects.create(
                uuid=item_uuid,
                name=item_name,
                room=room,
            )
        use = DigitalUse.objects.filter(uuid=use_uuid).first()
        if not use:
            use = DigitalUse.objects.create(
                uuid=use_uuid,
                title=use_name,
                description=use_description
            )
            use.items.add(item)
            use.tags.add(*use_tags_raw.split(';'))

        if service_uuid:
            service = DigitalService.objects.filter(uuid=service_uuid).first()
            if service:
                service.title = service_title
                service.description = service_desc
                service.url = service_url
                service.scope = scope
                service.contact = service_contact
                service.use = use
                service.save()
            else:
                service_data = {
                    'title': service_title,
                    'description': service_desc,
                    'url': service_url,
                    'scope': scope,
                    'contact': service_contact,
                    'use': use,
                }
                if service_uuid:
                    service_data['uuid'] = service_uuid
                service = DigitalService.objects.create(**service_data)

    return Response({'status': 'ok'}, status=status.HTTP_200_OK)
