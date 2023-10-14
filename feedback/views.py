from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsLocalAccess
from org.permissions import HasOrganizationAPIKey

from .models import Feedback, Question, Answer, AnswerChoice
from .serializers import FeedbackSerializer, QuestionSerializer, AnswerSerializer, AnswerChoiceSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()
    permission_classes = [IsLocalAccess | HasOrganizationAPIKey | IsAuthenticated]


class AnswerChoiceViewset(viewsets.ModelViewSet):
    serializer_class = AnswerChoiceSerializer
    queryset = AnswerChoice.objects.all()
    permission_classes = [IsLocalAccess | HasOrganizationAPIKey | IsAuthenticated]

class QuestionViewset(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [IsLocalAccess | HasOrganizationAPIKey | IsAuthenticated]

class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = [IsLocalAccess | HasOrganizationAPIKey | IsAuthenticated]