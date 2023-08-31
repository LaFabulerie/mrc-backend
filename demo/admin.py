from django.contrib import admin
from .models import *


class ScenarioRoomChoiceStepAdmin(admin.TabularInline):
    model = ScenarioRoomChoiceStep
    extra = 1


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):

    def nb_room_steps(self, obj):
        return obj.room_steps.count()
    nb_room_steps.short_description = 'Nombre de pièces'

    list_display = ('name', 'description', 'nb_room_steps')
    inlines = [ScenarioRoomChoiceStepAdmin]


class ScenarioUseChoiceStepAdmin(admin.TabularInline):
    model = ScenarioUseChoiceStep
    extra = 1


@admin.register(ScenarioItemChoiceStep)
class ScenarioItemChoiceStepAdmin(admin.ModelAdmin):

    def nb_use_steps(self, obj):
        return obj.use_steps.count()
    nb_use_steps.short_description = 'Nombre d\'usages'

    list_display = ('room_step', 'item', 'nb_use_steps')
    inlines = [ScenarioUseChoiceStepAdmin]


