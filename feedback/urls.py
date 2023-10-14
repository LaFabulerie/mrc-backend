from rest_framework import routers
from .views import *
from django.urls import path

router = routers.SimpleRouter()
router.register(r'feedbacks', FeedbackViewSet, basename='feedbacks')
router.register(r'questions', QuestionViewset, basename='questions')
router.register(r'answers', AnswerViewSet, basename='answers')
router.register(r'answerchoices', AnswerChoiceViewset, basename='answerchoices')

urlpatterns = router.urls