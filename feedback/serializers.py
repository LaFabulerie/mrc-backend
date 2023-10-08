from rest_framework import serializers
from .models import *


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"

class AnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
    choices = AnswerChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):

    feedback_id = serializers.PrimaryKeyRelatedField(source='feedback', queryset=Feedback.objects.all(), write_only=True)
    question_id = serializers.PrimaryKeyRelatedField(source='question', queryset=Question.objects.all(), write_only=True)

    class Meta:
        model = Answer
        fields = ["feedback_id", "question_id", "choice", "text"]
