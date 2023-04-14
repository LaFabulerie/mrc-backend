from rest_framework import routers
from .views import OrganizationViewSet, UserViewSet

router = routers.SimpleRouter()
router.register(r'orgs', OrganizationViewSet, basename='orgs')
router.register(r'user', UserViewSet, basename='user')


urlpatterns = router.urls