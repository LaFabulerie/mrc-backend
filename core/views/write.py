import csv
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from core.models import DigitalUse, DigitalService, Item, Contribution
from core.serializers import DigitalUseSerializer, DigitalServiceSerializer, ContributionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from core.permissions import IsLocalAccess
from org.permissions import HasOrganizationAPIKey
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from weasyprint import HTML
import mimetypes
from django.core.files import File
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles import finders
from weasyprint import default_url_fetcher
from core.import_export import import_services
from escpos.printer import Usb


class DigitalUseWriteViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = DigitalUse.objects.all()
    serializer_class = DigitalUseSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'uuid'
    lookup_field = 'uuid'


class DigitalServiceWriteViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = DigitalService.objects.all()
    serializer_class = DigitalServiceSerializer
    permission_classes = [IsAuthenticated]

class ContributionWriteViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['POST'])
    def validate_contribution(self, request, pk=None):
        contribution = self.get_object()
        contribution.validate()

        return Response({'message': 'Contribution validée.'})



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

        text_mail = render_to_string('email/cart.txt')
        html_mail = render_to_string('email/cart.html')

        msg = EmailMultiAlternatives("Maison (re)connectée - Votre liste de service",
                                     text_mail,
                                     settings.DEFAULT_FROM_EMAIL,
                                     [email])
        msg.attach_alternative(html_mail, "text/html")

        host = Site.objects.get_current().domain

        context = {
            'services': DigitalService.objects.filter(uuid__in=service_uuids),
            'host': host,
        }

        html_content = render_to_string("cart/pdf.html", context)

        pdf_content = HTML(
            string=html_content,
            base_url="not-used://",
            url_fetcher=django_url_fetcher,
        ).write_pdf()

        msg.attach("services.pdf", pdf_content, 'application/pdf')

        msg.send()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'])
    def pdf(self, request):
        cart = request.data.get('basket', {})
        service_uuids = [s['uuid'] for s in cart]
        if len(service_uuids) == 0:
            return Response({'status': 'error', 'message': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        host = Site.objects.get_current().domain

        context = {
            'services': DigitalService.objects.filter(uuid__in=service_uuids),
            'host': host,
        }

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f"attachment; filename=services.pdf"

        html_content = render_to_string("cart/pdf.html", context)

        HTML(
            string=html_content,
            base_url="not-used://",
            url_fetcher=django_url_fetcher,
        ).write_pdf(
            target=response,
            uncompressed_pdf=True,
        )

        return response


    @action(detail=False, methods=['post'])
    def print(self, request):
        cart = request.data.get('basket', {})
        service_uuids = [s['uuid'] for s in cart]
        if len(service_uuids) == 0:
            return Response({'status': 'error', 'message': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            printer = Usb(settings.PRINTER_VENDOR_ID, settings.PRINTER_PRODUCT_ID, profile="TM-L90")
            printer.image("core/static/core/printer_mrc.png", center=True)
            printer.set(align="center", font="a", width=2, height=2, custom_size=True)
            printer.text("Liste de vos services\n")
            printer.text("numériques\n\n")
            for service in DigitalService.objects.filter(uuid__in=service_uuids):
                printer.set(align="left", font="a", width=2, height=2, custom_size=True)
                printer.text(f"{service.title}\n")
                printer.set(align="left", font="a", width=1, height=1, custom_size=True)
                printer.text(f"{service.url}\n")
                printer.qr(service.url, size=5)
                printer.text("\n")
            printer.cut()
            printer.close()
        except Exception:
            return Response({'status': 'error', 'message': 'Printer error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class ImportDigitalServiceApiView(APIView):
    permission_classes = [IsLocalAccess | HasOrganizationAPIKey | IsAuthenticated]
    def post(self, request, format=None):
        file = request.FILES['import[]']
        return import_services(file.read().decode('utf-8').splitlines())

