from django.db import models
from autoslug import AutoSlugField
from taggit.managers import TaggableManager

def room_video_path(instance, filename):
    return f"{instance.slug}/videos/{filename}"

class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to=room_video_path, blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Pièce'
        

def item_image_path(instance, filename):
    return f"{instance.slug}/images/{filename}"


class Item(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    room = models.ForeignKey(Room, blank=True, null=True, on_delete=models.SET_NULL, related_name='items')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Objet'


class DigitalUse(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True)
    description = models.TextField(blank=True, null=True)
    items = models.ManyToManyField(Item, blank=True, related_name='uses')
    tags = TaggableManager(blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Usage numérique'
        verbose_name_plural = 'Usages numériques'   
    

class Zone(models.Model):
    name = models.CharField(max_length=255)
    

class DigitalService(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    uses = models.ManyToManyField(DigitalUse, blank=True, related_name='services') 
    zone = models.ForeignKey(Zone, blank=True, null=True, on_delete=models.SET_NULL, related_name='services')
    
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