from django.db import models
from core.models import Room, Item, DigitalUse


class Scenario(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    intro_video = models.FileField(upload_to='videos/scenarii/', blank=True, null=True)

    class Meta:
        verbose_name = 'Scénario'
        verbose_name_plural = 'Scénarii'


class ScenarioRoomChoiceStep(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='room_steps')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.scenario.name} - {self.room.name}"

    class Meta:
        verbose_name = 'Choix de pièce'
        verbose_name_plural = 'Choix de pièce'


class ScenarioItemChoiceStep(models.Model):
    room_step = models.ForeignKey(ScenarioRoomChoiceStep, on_delete=models.CASCADE, related_name='item_steps')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos/scenarii/', blank=True, null=True)

    class Meta:
        verbose_name = 'Choix d\'objet'
        verbose_name_plural = 'Choix d\'objet'


class ScenarioUseChoiceStep(models.Model):
    item_step = models.ForeignKey(ScenarioItemChoiceStep, on_delete=models.CASCADE, related_name='use_steps')
    use = models.ForeignKey(DigitalUse, on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos/scenarii/', blank=True, null=True)

    class Meta:
        verbose_name = 'Choix d\'usage'
        verbose_name_plural = 'Choix d\'usage'



