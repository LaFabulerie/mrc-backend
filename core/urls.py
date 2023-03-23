from rest_framework import routers
from .views import RoomViewSet, DigitalUseViewSet

router = routers.SimpleRouter()
router.register(r'rooms', RoomViewSet, basename='rooms')
router.register(r'digital-uses', DigitalUseViewSet, basename='digital-uses')

urlpatterns = router.urls