from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
from django.dispatch import receiver
from autoslug import AutoSlugField
from taggit.managers import TaggableManager
import uuid
import os


class Room(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4, editable = False, unique=True)
    name = models.CharField(verbose_name="Nom", max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)
    video = models.CharField(max_length=255, blank=True, null=True, editable=False)
    main_color = models.CharField(verbose_name="Couleur principale", max_length=15, blank=True, null=True)

    # light_pin = models.IntegerField(verbose_name="Numéro de la broche du ruban LED", null=True, blank=True)

    position = models.IntegerField(verbose_name="Position", default=0)

    next_room = models.ForeignKey('self', verbose_name="Pièce suivante", blank=True, null=True, on_delete=models.SET_NULL, related_name='previous_room')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Pièce'
        ordering = ['position']


@receiver(pre_save, sender=Room)
def rename_video_file(sender, instance, **kwargs):
    old_instance = Room.objects.filter(id=instance.id).first()
    slug = slugify(instance.name)
    video_file_name = f"{settings.STATIC_URL}videos/{slug}.mp4"
    if old_instance and old_instance.video and old_instance.video != video_file_name:
        old_video_path = f"{settings.STATIC_URL}{old_instance.video.replace(settings.STATIC_URL, '/')}"
        new_video_path = f"{settings.STATIC_URL}{video_file_name.replace(settings.STATIC_URL, '/')}"
        os.rename(old_video_path, new_video_path)
    instance.video = video_file_name


class Item(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable = False, unique=True)
    name = models.CharField(verbose_name="Nom", max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)
    image = models.CharField(max_length=255, blank=True, null=True, editable=False)
    room = models.ForeignKey(Room, verbose_name="Pièce", blank=True, null=True, on_delete=models.SET_NULL, related_name='items')

    light_ctrl = models.IntegerField(verbose_name="Numéro du contrôleur de lumière", null=True, blank=True, choices=[(1, 1), (2, 2), (3, 3)])
    light_pin = models.CharField(verbose_name="Numéro de la broche de la LED", max_length=2, null=True, blank=True, choices=[
        ('AO', 'AO'),
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('A3', 'A3'),
        ('A4', 'A4'),
        ('A5', 'A5'),
        ('A6', 'A6'),
        ('A7', 'A7'),
        ('B0', 'B0'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('B3', 'B3'),
        ('B4', 'B4'),
        ('B5', 'B5'),
        ('B6', 'B6'),
        ('B7', 'B7'),
    ])

    def __str__(self):
        return f"{self.room.name} - {self.name}"
    
    class Meta:
        verbose_name = 'Objet'
        
@receiver(pre_save, sender=Item)
def rename_image_file(sender, instance, **kwargs):
    old_instance = Item.objects.filter(id=instance.id).first()
    slug = slugify(instance.name)
    image_file_name = f"{settings.STATIC_URL}images/{slug}.svg"
    if old_instance and old_instance.image and old_instance.image != image_file_name:
        old_image_path = f"{settings.STATIC_URL}{old_instance.image.replace(settings.STATIC_URL, '/')}"
        new_image_path = f"{settings.STATIC_URL}{image_file_name.replace(settings.STATIC_URL, '/')}"
        os.rename(old_image_path, new_image_path)
    instance.image = image_file_name
    print(instance.image)


class DigitalUse(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4, editable = False, unique=True)
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True)
    description = models.TextField(blank=True, null=True)
    items = models.ManyToManyField(Item, blank=True, related_name='uses')
    tags = TaggableManager(blank=True)
    
    def __str__(self):
        return f"[{','.join([item.room.name +' - '+item.name for item in self.items.all()])}] {self.title}"

    class Meta:
        verbose_name = 'Usage numérique'
        verbose_name_plural = 'Usages numériques'   
    

class Area(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Zone d\'activité'
        verbose_name_plural = 'Zones d\'activité'
    

class DigitalService(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    area = models.ForeignKey(Area, blank=True, null=True, on_delete=models.SET_NULL, related_name='services')
    use = models.ForeignKey(DigitalUse, blank=True, null=True, on_delete=models.CASCADE, related_name='services')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Service numérique'
        verbose_name_plural = 'Services numériques'
    
    
class DigitalServiceContact(models.Model):
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=50)
    service = models.ForeignKey(DigitalService, on_delete=models.CASCADE, related_name='contacts')
    
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'