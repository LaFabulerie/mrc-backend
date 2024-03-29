from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_api_key.models import AbstractAPIKey

import uuid

class User(AbstractUser):
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')


class Organization(models.Model):
    name = models.CharField(max_length=128)
    uuid = models.UUIDField(default = uuid.uuid4, editable = False, unique=True)

    def __str__(self):
        return self.name

class OrganizationAPIKey(AbstractAPIKey):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="api_keys",)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_keys", null=True, blank=True)