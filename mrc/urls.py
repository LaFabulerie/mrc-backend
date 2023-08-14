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

urlpatterns = [
    path('', admin.site.urls),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/signup/', include('org.registration_urls')),
    path('api/', include('core.urls')),
    path('api/', include('org.urls')),
    path('api/client/', include('client.urls')),
    
    re_path(r'^api/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


print(f"\n{10*'*'} ENVIRONMENT : {settings.ENV_NAME} {10*'*'}\n")