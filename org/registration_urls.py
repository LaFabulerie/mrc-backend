from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.urls import path, re_path
from django.views.generic import TemplateView, RedirectView

from dj_rest_auth.registration.views import RegisterView, VerifyEmailView, ResendEmailVerificationView
from django.conf import settings

def redirec_to_frontend_verify_email(request, key=None, *kwargs):
    url = f"{settings.FRONTEND_URL}/verify-email/{key}"
    return HttpResponsePermanentRedirect(url)


urlpatterns = [
    path('', RegisterView.as_view(), name='rest_register'),
    path('verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('resend-email/', ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', redirec_to_frontend_verify_email, name='account_confirm_email'),
    path('account-email-verification-sent/', TemplateView.as_view(), name='account_email_verification_sent'),
]