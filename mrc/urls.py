import stat
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
      title="API Maison Reconnectées",
      default_version='v1',
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="atiberghien@numnprod.fr"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


api_urlpatterns = [
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/signup/', include('org.registration_urls')),
    path('api/client/', include('client.urls')),
    path('api/feedback/', include('feedback.urls')),
    path('api/', include('core.urls')),
    path('api/', include('org.urls')),
    path('', include('website.urls')),
]


urlpatterns = api_urlpatterns + [
    re_path(r'^api/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# print(f"\n{10*'*'} ENVIRONMENT : {settings.EXECUTION_MODE} - DEBUG : {settings.DEBUG} {10*'*'} \n".upper())