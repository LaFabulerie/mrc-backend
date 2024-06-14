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
    video = models.CharField(max_length=500, blank=True, null=True, editable=False)
    main_color = models.CharField(verbose_name="Couleur principale", max_length=15, blank=True, null=True)

    # light_pin = models.IntegerField(verbose_name="Numéro de la broche du ruban LED", null=True, blank=True)

    # position = models.IntegerField(verbose_name="Position", default=0)

    next_room = models.ForeignKey('self', verbose_name="Pièce suivante", blank=True, null=True, on_delete=models.SET_NULL, related_name='previous_room')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Pièce'


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
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(verbose_name="Nom", max_length=500)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)
    image = models.CharField(max_length=500, blank=True, null=True, editable=False)
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


class DigitalUse(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4, editable = False, unique=True)
    title = models.CharField(max_length=500)
    slug = AutoSlugField(populate_from='title', unique=True)
    description = models.TextField(blank=True, null=True)
    items = models.ManyToManyField(Item, blank=True, related_name='uses')
    tags = TaggableManager(blank=True)

    def __str__(self):
        return f"[{','.join([item.room.name +' - '+item.name for item in self.items.all()])}] {self.title}"

    class Meta:
        verbose_name = 'Usage numérique'
        verbose_name_plural = 'Usages numériques'


class DigitalService(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=500)
    slug = AutoSlugField(populate_from='title', unique=True)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    scope = models.CharField(max_length=500, blank=True, null=True)
    use = models.ForeignKey(DigitalUse, blank=True, null=True, on_delete=models.CASCADE, related_name='services')
    contact = models.TextField(blank=True, null=True)
    ordre = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Service numérique'
        verbose_name_plural = 'Services numériques'


class Contribution(models.Model):
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE, related_name='contributions')
    use = models.ForeignKey(DigitalUse, blank=True, null=True, on_delete=models.CASCADE, related_name='contributions')
    usage_title = models.CharField(max_length=500, blank=True, null=True)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=500)
    scope = models.CharField(max_length=500)
    contact = models.TextField(blank=True, null=True)
    commune = models.CharField(max_length=500, blank=True, null=True)
    tags = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.use is not None:
            return f"{self.use.title} - {self.title}"
        return f"{self.usage_title} - {self.title}"

    def validate(self):
        # Création d'un nouvel usage
        if self.usage_title is not None and self.usage_title != "":
            use = DigitalUse.objects.create(
                title=self.usage_title,
                description="",
            )
            use.items.add(self.item)
        else:
            use = self.use

        # Gestion des tags
        if self.tags is not None:
            for tag in self.tags.split(","):
                use.tags.add(tag.strip())

        # Création du service
        DigitalService.objects.create(
            title=self.title,
            description=self.description,
            url=self.url,
            scope=self.scope,
            use=use,
            contact=self.contact,
        )

        # Suppression de la contribution
        self.delete()

    class Meta:
        verbose_name = 'Contribution'
        verbose_name_plural = 'Contributions'
