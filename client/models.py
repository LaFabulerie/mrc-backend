from django.db import models
from django.dispatch import receiver
from org.models import Organization
from core.models import Area

class RemoteAccess(models.Model):
    name = models.CharField(max_length=255)
    server_url = models.URLField()
    api_key = models.CharField(max_length=255)
    api_key_prefix = models.CharField(max_length=255, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    default = models.BooleanField(default=False)
    org = models.ForeignKey(Organization, on_delete=models.SET_NULL, related_name='+', null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, related_name='+', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Accès distant'
        verbose_name_plural = 'Accès distants'

@receiver(models.signals.post_save, sender=RemoteAccess)
def fill_api_key_prefix(sender, instance, created, **kwargs):
    if instance.default:
        RemoteAccess.objects.exclude(id=instance.id).update(default=False)

@receiver(models.signals.post_delete, sender=RemoteAccess)
def set_default(sender, instance, **kwargs):
    if instance.default:
        obj = RemoteAccess.objects.first()
        if obj:
            obj.default = True
            obj.save()