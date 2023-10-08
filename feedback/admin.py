from django.contrib import admin
from .models import Feedback, Question, AnswerChoice, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    can_delete = False
    fields = ["question_text", "choice", "text"]
    readonly_fields = ["question_text", "choice", "text"]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("created_at",)
    inlines = [AnswerInline]


class AnswerChoiceInline(admin.TabularInline):
    model = AnswerChoice

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "type", "allow_comment", "order")
    search_fields = ("text",)
    list_editable = ("order", "allow_comment")
    inlines = [AnswerChoiceInline]


