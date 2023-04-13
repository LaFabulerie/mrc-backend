from rest_framework import routers
from .views import RoomViewSet, DigitalUseViewSet, TagApiView, DigitalServiceViewSet, AreaViewSet
from django.urls import path

router = routers.SimpleRouter()
router.register(r'rooms', RoomViewSet, basename='rooms')
router.register(r'digital-uses', DigitalUseViewSet, basename='digital-uses')
router.register(r'digital-services', DigitalServiceViewSet, basename='digital-services')
router.register(r'areas', AreaViewSet, basename='areas')

urlpatterns = router.urls + [
    path('tags/', TagApiView.as_view(), name='tags'),
]