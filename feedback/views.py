from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsLocalAccess
from org.permissions import HasOrganizationAPIKey

from .models import Feedback, Question, Answer
from .serializers import FeedbackSerializer, QuestionSerializer, AnswerSerializer

class FeedbackViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()
    permission_classes = [IsLocalAccess | HasOrganizationAPIKey | IsAuthenticated]


class QuestionViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [IsLocalAccess | HasOrganizationAPIKey | IsAuthenticated]

class AnswerViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = [IsLocalAccess | HasOrganizationAPIKey | IsAuthenticated]