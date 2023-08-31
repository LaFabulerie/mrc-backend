from rest_framework import routers
from .views import *


router = routers.SimpleRouter()

router.register(r'scenarii', ScenarioViewSet, basename='scenarii')

urlpatterns = router.urls