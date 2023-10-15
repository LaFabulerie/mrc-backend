from rest_framework import serializers
from .models import *




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
    question = QuestionSerializer(read_only=True)

    feedback_id = serializers.PrimaryKeyRelatedField(source='feedback', queryset=Feedback.objects.all(), write_only=True)
    question_id = serializers.PrimaryKeyRelatedField(source='question', queryset=Question.objects.all(), write_only=True)

    class Meta:
        model = Answer
        exclude = ['feedback']


class FeedbackSerializer(serializers.ModelSerializer):
    repr = serializers.SerializerMethodField()
    answers = AnswerSerializer(many=True, read_only=True)

    def get_repr(self, obj):
        return str(obj)
    
    class Meta:
        model = Feedback
        fields = "__all__"