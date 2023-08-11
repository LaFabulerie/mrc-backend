from rest_framework.permissions import BasePermission
import urllib.parse
from django.conf import settings

class IsLocalAccess(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        origin = urllib.parse.urlparse(request.META["HTTP_ORIGIN"])
        origin = origin.netloc.split(":")[0]
        host = request.META["HTTP_HOST"].split(":")[0]
        return settings.EXECUTION_MODE == "standalone" or (origin == host or origin == "localhost")