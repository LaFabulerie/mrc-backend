from autoslug import AutoSlugField
from autoslug.settings import slugify
from django.db import models


class Parameter(models.Model):
    PARAMETER_CATEGORY = (
        ("B", "Booléen"),
        ("I", "Entier"),
        ("S", "Chaine de caractères"),
        ("D", "Décimal"),
    )

    name = models.CharField(max_length=500)
    slug = AutoSlugField(populate_from="name", unique=True, always_update=True)
    category = models.CharField(max_length=1, choices=PARAMETER_CATEGORY)
    bool_value = models.BooleanField(default=False)
    int_value = models.IntegerField(blank=True, null=True)
    str_value = models.CharField(max_length=500, blank=True, null=True)
    dec_value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    @property
    def value(self):
        if self.category == "B":
            return self.bool_value
        if self.category == "I":
            return self.int_value
        if self.category == "S":
            return self.str_value
        if self.category == "D":
            return self.dec_value
        return None

    def __str__(self):
        return f"{self.name} ({self.value})"

    class Meta:
        verbose_name = 'Paramètre'


def get_parameter(parameter):
    try:
        return Parameter.objects.filter(slug=slugify(parameter)).first().value
    except AttributeError:
        return None
