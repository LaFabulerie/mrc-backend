from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from core.models import DigitalUse, DigitalService, Area
from core.serializers import DigitalUseSerializer, DigitalServiceSerializer, AreaSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from core.permissions import IsLocalAccess
from org.permissions import HasOrganizationAPIKey
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from weasyprint import HTML
import time
import calendar
import mimetypes
from django.core.files import File
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles import finders
from weasyprint import default_url_fetcher


class DigitalUseWriteViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = DigitalUse.objects.all()
    serializer_class = DigitalUseSerializer
    permission_classes = [IsAuthenticated]

class DigitalServiceWriteViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = DigitalService.objects.all()
    serializer_class = DigitalServiceSerializer
    permission_classes = [IsAuthenticated]

class AreaWriteViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]




def django_url_fetcher(url: str):
    try:
        filename = None
        data = None

        if url.startswith(settings.MEDIA_URL):
            filename = url.replace(str(settings.MEDIA_URL), str(settings.MEDIA_ROOT) + "/")
            with File(open(filename, "rb")) as f:
                data = f.read()
        elif url.startswith(staticfiles_storage.base_url):
            filename = url.replace(staticfiles_storage.base_url, "", 1)
            path = finders.find(filename)
            if path:
                with open(path, "rb") as f:
                    data = f.read()
            else:
                with staticfiles_storage.open(filename) as f:
                    data = f.read()

        if data:
            return {
                "mime_type": mimetypes.guess_type(url)[0],
                "string": data,
            }

    except Exception as e:
        print("MEDIA SHIT", e)
        pass

    return default_url_fetcher(url)

class CartViewSet(GenericViewSet):
    permission_classes = [IsLocalAccess | HasOrganizationAPIKey | IsAuthenticated]
    @action(detail=False, methods=['post'])
    def email(self, request, format=None):
        email = request.data.get('email', None)
        cart = request.data.get('basket', {})
        service_uuids = [s['uuid'] for s in cart]
        if email is None:
            return Response({'status': 'error', 'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        if len(service_uuids) == 0:
            return Response({'status': 'error', 'message': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        text_mail = render_to_string('email/cart.txt', {'cart': cart})
        html_mail = render_to_string('email/cart.html', {'cart': cart})

        msg = EmailMultiAlternatives("Maison (re)connectée - Votre liste de service",
                                     text_mail,
                                     settings.DEFAULT_FROM_EMAIL,
                                     [email])
        msg.attach_alternative(html_mail, "text/html")
        

        host = 'http://localhost:8000'
        if not settings.DEBUG:
            host = Site.objects.get_current().domain

        context = {
            'services': DigitalService.objects.filter(uuid__in=service_uuids),
            'host': host,
        }

        timestamp = calendar.timegm(time.gmtime())
        HTML(string=render_to_string('cart/pdf.html', context)).write_pdf(f"/tmp/services{hex(timestamp)[2:]}_.pdf")

        with open(f"/tmp/services{hex(timestamp)[2:]}_.pdf", 'rb') as f:
            msg.attach("services.pdf", f.read(), 'application/pdf')

        msg.send()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

    # @action(detail=False, methods=['post'])
    @action(detail=False, methods=['post'])
    def pdf(self, request):
        cart = request.data.get('basket', {})
        service_uuids = [s['uuid'] for s in cart]
        if len(service_uuids) == 0:
            return Response({'status': 'error', 'message': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        host = 'http://localhost:8000'
        if not settings.DEBUG:
            host = Site.objects.get_current().domain

        context = {
            'services': DigitalService.objects.filter(uuid__in=service_uuids),
            'host': host,
        }

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f"attachment; filename=services.pdf"

        HTML(
            string=render_to_string("cart/pdf.html", context),
            base_url="not-used://",
            url_fetcher=django_url_fetcher,
        ).write_pdf(
            target=response,
            uncompressed_pdf=True,
        )

        return response