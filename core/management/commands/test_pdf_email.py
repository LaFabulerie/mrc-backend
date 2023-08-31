from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from weasyprint import HTML
import time
import calendar
from django.core.management.base import BaseCommand
from core.models import DigitalService
from django.template.loader import render_to_string
from core.views.write import django_url_fetcher
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        email = "alban.tiberghien@gmail.com"
        services = DigitalService.objects.all().order_by('?')[:3]

        text_mail = render_to_string('email/cart.txt')
        html_mail = render_to_string('email/cart.html')

        msg = EmailMultiAlternatives("Maison (re)connectée - Votre liste de service",
                                     text_mail,
                                     settings.DEFAULT_FROM_EMAIL,
                                     [email])
        msg.attach_alternative(html_mail, "text/html")
        

        host = 'http://localhost:8000'
        if not settings.DEBUG:
            host = Site.objects.get_current().domain

        context = {
            'services': services,
            'host': host,
        }

        timestamp = calendar.timegm(time.gmtime())
        
        pdf_content = HTML(
            string=render_to_string("cart/pdf.html", context),
            base_url="not-used://",
            url_fetcher=django_url_fetcher,
        ).write_pdf()

        msg.attach("services.pdf", pdf_content, 'application/pdf')

        msg.send()
