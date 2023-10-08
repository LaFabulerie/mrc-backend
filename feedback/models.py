from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Feedback(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Feedback du {}".format(self.created_at.strftime("%d/%m/%Y à %Hh%M"))
    
    class Meta:
        ordering = ("-created_at",)


class Question(models.Model):
    text = models.CharField(max_length=500)
    type = models.CharField(max_length=10, choices=(
        ('text', 'Réponse libre'),
        ('radio', 'Choix unique'),
        ('checkbox', 'Choix multiple'),
    ))
    allow_comment = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ("order",)


class AnswerChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=200)


class Answer(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)
    question_text = models.CharField(max_length=500, blank=True, null=True)
    choice = models.CharField(max_length=500, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=Answer)
def save_answer(sender, instance, **kwargs):
    if instance.question and not instance.question_text:
        instance.question_text = instance.question.text
        instance.save()

