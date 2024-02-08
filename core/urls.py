from rest_framework import routers
from .views import *
from django.urls import path

router = routers.SimpleRouter()
router.register(r'r/rooms', RoomReadOnlyViewSet, basename='ro-rooms')
router.register(r'r/digital-uses', DigitalUseReadOnlyViewSet, basename='ro-digital-uses')
router.register(r'r/digital-services', DigitalServiceReadOnlyViewSet, basename='ro-digital-services')
router.register(r'r/items', ItemReadOnlyViewSet, basename='ro-items')
router.register(r'r/contributions', ContributionReadOnlyViewSet, basename='ro-contributions')

router.register(r'w/digital-uses', DigitalUseWriteViewSet, basename='w-digital-uses')
router.register(r'w/digital-services', DigitalServiceWriteViewSet, basename='w-digital-services')
router.register(r'w/contributions', ContributionWriteViewSet, basename='w-contributions')
router.register(r'w/cart', CartViewSet, basename='ro-cart')

urlpatterns = router.urls + [
    path('r/tags/', TagApiView.as_view(), name='r-tags'),
    path('r/export/', ExportDigitalServiceApiView.as_view(), name='r-export'),
    path('w/import/', ImportDigitalServiceApiView.as_view(), name='w-import'),
]
