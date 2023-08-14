from django.conf import settings
from rest_framework import routers
from .views import RemoteAccessViewSet


router = routers.SimpleRouter()
router.register(r'remote-accesses', RemoteAccessViewSet, basename='remote-accesses')

urlpatterns = router.urls